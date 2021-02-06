#!/usr/bin/python
 
import os
from posix import PRIO_USER
import sys
import json
import logging
import datetime
from pathlib import Path
import numpy as np
import time
from itertools import islice
import socket

import subprocess
import TransferWager.A5 as A5
import TransferWager.Redfire as Redfire
import TransferWager.A5_11x5 as A5_11x5
import TransferWager.A5_K3 as A5_K3
import traceback
from os import listdir
from os.path import isfile, isdir, join
from flask import send_from_directory
from flask import Flask, request, render_template , Response

app = Flask(__name__)

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def logfile_sort(e):
    trm = e.replace("opencode", "")
    trm = trm.replace("-", "")
    trm = trm.replace(".log", "")
    return int(trm)

def checkOpencodeExists(dict, opencode): 
    for d in dict:
        if d["OpenCode"] == opencode:
            return True
    return False


@app.route('/log/<path:filename>', methods=['GET'])
def download(filename):
    fullpath = f"{currentPath}/log/"
    whitelist = [
        "114.34.170.104", #Doway
        "122.116.29.74" #AsiaEastern
    ]
    logging.info(f"download logfile {filename} from remote ip :{request.remote_addr}")
    if  request.remote_addr in whitelist:
        if os.path.isfile(fullpath + filename ):
            return send_from_directory(directory=fullpath, filename=filename)
        else:
            return Response(f"file not exist...")
    else:
        logging.info(f"remote ip {request.remote_addr} not in white list")
        return Response(f"remote ip {request.remote_addr} not in white list")

@app.route('/mem', methods=['GET'])
def mem():
    path = f"{currentPath}/tools/systemInfo.sh"
    out, err = subprocess.Popen(['bash', path], stdout=subprocess.PIPE).communicate() 
    out = out.decode(encoding='UTF-8').splitlines()
    mem_usage = out[1].replace('%', '')
    return Response(mem_usage, mimetype='text/plain')

@app.route('/', methods=['GET'])
def home():
    path = f"{currentPath}/tools/systemInfo.sh"
    out, err = subprocess.Popen(['bash', path], stdout=subprocess.PIPE).communicate() 
    out = out.decode(encoding='UTF-8').splitlines()
    cpu_usage = out[0]
    mem_usage = out[1]
    ssd_usage = out[2]
    gpu0_info = out[3].split(",")
    gpu1_info = out[4].split(",")

    dateTimeObj = datetime.datetime.now()
    timeStr = dateTimeObj.strftime("%H%M%S%f")
    print('Current Timestamp : ', timeStr)

    # 取得所有檔案與子目錄名稱
    logfiles = listdir(f"{currentPath}/log")
    #logfiles.remove("calc_opencode_amount.log")
    #logfiles.sort(reverse=True, key=logfile_sort)
    #logfiles.insert(0,"calc_opencode_amount.log")
    logfilelength = len(logfiles)
    return render_template(f'index.html', CPU=cpu_usage, MEM=mem_usage, SSD=ssd_usage, GPU0=gpu0_info, GPU1=gpu1_info, 
        logfilelength=10, logfiles = logfiles[:10], timestamp=timeStr)

@app.route("/bestopen", methods=['GET', 'POST'])
def submit():
    title = '最佳化開獎策略'
    if request.method == 'POST':
        start = time.time()
        #print('request.form', request.data)
        betOn_rows = []
        raw_data = request.get_data().decode("utf-8")
        logging.info(f"[Request] row data: {raw_data}")
        jdata = json.loads(raw_data)
        buId = jdata["BuID"]    
        expectId = jdata["ExpectID"]
        wager_length = len(jdata["Bets"])
        opencodeCount = jdata["OpenCodeCount"]
        tolerance = jdata["Tolerance"]
        killRate = jdata["KillRate"]
        lotteryCode = jdata["LotteryCode"]
    
        jObj = {}
        jObj["wager_length"] = wager_length
        jObj["expectId"] = expectId;
        if tolerance > 0:
            jObj["direction"] = 1
        else:
            jObj["direction"] = -1
        jObj["killRate"] = killRate;
        jObj["opencodeCount"] = opencodeCount;
        jObj["Bets"] = []
        
        for jBet in jdata["Bets"]:
            if "11x5" in lotteryCode :
                (betons, odds, unitAmount, betOnCount) = A5_11x5.transferWager(logging, jBet)
                jObj["Bets"].append({
                    "betons" : betons,
                    "odds" : odds,
                    "unitAmount" : unitAmount,
                }) 
            elif "k3" in lotteryCode :
                (betons, odds, unitAmount, betOnCount) = A5_K3.transferWager(logging, jBet) 
                jObj["Bets"].append({
                    "betons" : betons,
                    "odds" : odds,
                    "unitAmount" : unitAmount,
                }) 
            else:
                response = { }
                response["code"] = 999
                response["msg"] = f"not support {lotteryCode}"
                rows = [] 
                return Response(json.dumps(response, cls=NumpyEncoder), mimetype='application/json')
        
        jsonfile =f'{currentPath}/data/{lotteryCode}_bets_{expectId}.json' 
        logging.info(f"path={jsonfile}")
        with open(jsonfile, 'w') as outfile:
            json.dump(jObj, outfile)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            if "11x5" in lotteryCode :
                client.connect(("127.0.0.1", 8700))
            elif "k3" in lotteryCode :
                client.connect(("127.0.0.1", 8701))

            client.sendall(jsonfile.encode())
            recv_msg = client.recv(32767).decode("UTF-8").replace('\0', '')
            logging.debug(f"Server:{recv_msg}")
        
        response = { }
        response["code"] = 0
        response["msg"] = "success"
        rows = [] 

        try:
            # print("=================")
            for row in recv_msg.split("\n"):
                if len(row) > 0:
                    #logging.debug(row)
                    opencode = row.split(',')[0]
                    amount = row.split(',')[1]
                    # if not checkOpencodeExists(rows, opencode): 把檢查重複丟給C語言
                    rows.append({
                        "TotalAmountSum": amount,
                        "OpenCode": opencode
                    }) 
        except Exception as e:
            error_class = e.__class__.__name__ #取得錯誤類型
            detail = e.args[0] #取得詳細內容
            cl, exc, tb = sys.exc_info() #取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
            fileName = lastCallStack[0] #取得發生的檔案名稱
            lineNum = lastCallStack[1] #取得發生的行號
            funcName = lastCallStack[2] #取得發生的函數名稱
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            logging.error(errMsg)

        response["result"] = { "rows" : rows }
        #print(json.dumps(response, cls=NumpyEncoder))
        end = time.time()
        #logging.debug(response)
        logging.info(f"[Response] buId:{buId}, expectId:{expectId}, spend time: {end - start} s, row length:{ len(rows) }")
        return Response(json.dumps(response, cls=NumpyEncoder), mimetype='application/json')
   
    return render_template('bestopen.html', title=title)

if __name__ == "__main__":
    global currentPath

    currentPath = os.path.dirname(os.path.abspath(__file__))
    currentPath = currentPath.replace("/tools", "")
    
    if not os.path.exists(f"{currentPath}/log"):
        os.mkdir(f"{currentPath}/log")
    home_path = str(Path.home())
    log_fliename = datetime.datetime.now().strftime(f"{currentPath}/log/opencode-%Y-%m-%d.log")
    print(f"log filename formate = {log_fliename}")
    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            datefmt='%m-%d %H:%M:%S',
            filename=log_fliename)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logging.debug("current path : " + currentPath)
    
    app.config["DEBUG"] = True
    app.run(host='0.0.0.0', port=5000)