#!/usr/bin/python
 
import os
import sys
import json
import logging
import datetime
from pathlib import Path
import numpy as np
import pandas as pd
import itertools
import pyopencl as cl
import time
from itertools import islice
import socket
import random
import subprocess
import TransferWager.A5 as A5
import TransferWager.Redfire as Redfire
import traceback
import test
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


def program_build(kernel_file): 
     # Open program file and build
    program_file = open(kernel_file, 'r') # Scale x Matrx
    program_text = program_file.read()
    program_file.close()
    program = cl.Program(context, program_text)
    try:
        program.build()
    except:
        print("Build log:")
        print(program.get_build_info(devices[0], 
                cl.program_build_info.LOG))
        raise
    return program

def sum_beton_total_amount(one_vector_mask, amount_matrix, wager_length=10000):
    tStart = time.time()#計時開始
    queue = cl.CommandQueue(context)
    selection_length = len(one_vector_mask)    
    result = np.empty(selection_length, dtype=np.float32)

    # create buffer READ/WRITE  cl.mem_flags.READ_WRITE
    buffer_mask = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=one_vector_mask)
    buffer_matrix = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=amount_matrix)
    buffer_result = cl.Buffer(context, cl.mem_flags.WRITE_ONLY,  size=result.nbytes) 
   
    event = program.sum_beton_total_amount(
                    queue, (selection_length, ), (1, ),
                    buffer_mask, 
                    buffer_matrix,
                    buffer_result,
                    np.int32(wager_length))
    event.wait()

    # Read data back from buffer
    result = np.empty(selection_length, dtype=np.float32)
    cl.enqueue_copy(queue, result, buffer_result)
    queue.flush()

    tEnd = time.time()#計時結束
    logging.info("It cost %f sec" % (tEnd - tStart))#會自動做近位
    return result

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
    logfiles.remove("calc_opencode_amount.log")
    logfiles.sort(reverse=True, key=logfile_sort)
    logfiles.insert(0,"calc_opencode_amount.log")
    logfilelength = len(logfiles)
    return render_template(f'index.html', CPU=cpu_usage, MEM=mem_usage, SSD=ssd_usage, GPU0=gpu0_info, GPU1=gpu1_info, 
        logfilelength=10, logfiles = logfiles[:10], timestamp=timeStr)

@app.route("/bestopen", methods=['GET', 'POST'])
def submit():
    title = '最佳化開獎策略'
    if request.method == 'POST':
        #print('request.form', request.data)
        betOn_rows = []
        raw_data = request.get_data().decode("utf-8")
        logging.info(f"[Request] row data: {raw_data}")
        jdata = json.loads(raw_data)
        buId = jdata["BuID"]
        if buId == "RedFire":
            (beton_amount_table, beton_amount_odds_table, total_bet_count, expectId, target_amount, tolerance, opencodeCount) = Redfire.transferWager(logging, headers, jdata)    
        else:
            (beton_amount_table, beton_amount_odds_table, total_bet_count, expectId, target_amount, tolerance, opencodeCount) = A5.transferWager(logging, headers, jdata)

        wager_length = len(beton_amount_table)
        logging.info(f"wager_length={wager_length}")
        logging.info(f"total_bet_count={total_bet_count}, expectId={expectId}, target_amount={target_amount}, tolerance={tolerance}")
        
        start = time.time()
        with open(f"{currentPath}/data/beton_amount_{expectId}.csv", "w+") as f:
            for amount in beton_amount_table:
                strAmountWithComma = ','.join(str(e) for e in amount)
                f.write(strAmountWithComma+"\n")

        with open(f"{currentPath}/data/beton_amount_with_odds_{expectId}.csv", "w+") as f:
            for amount in beton_amount_odds_table:
                strAmountWithComma = ','.join(str(e) for e in amount)
                f.write(strAmountWithComma+"\n")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect(("127.0.0.1", 8700))
            #sendData = str(expectId)
            sendData = f"{currentPath}/data/beton_amount_{expectId}.csv,"
            sendData += f"{currentPath}/data/beton_amount_with_odds_{expectId}.csv,"
            sendData += f"{wager_length},"
            sendData += f"{expectId},"
            sendData += f"{target_amount},"
            sendData += f"{tolerance},"
            sendData += f"{opencodeCount},"
            client.sendall(sendData.encode())
            
            serverMessage = client.recv(1048576).decode("UTF-8").replace('\0', '')
            #logging.debug('Server:', serverMessage)
        
        response = { }
        response["code"] = 0
        response["msg"] = "success"
        rows = [] 
    
        try:
            # print("=================")
            for row in serverMessage.split("\n"):
                if len(row) > 0:
                    logging.debug(row)
                    opencode = row.split(',')[0]
                    amount = row.split(',')[1]
                    if not checkOpencodeExists(rows, opencode):
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
        
        try:
            if os.path.exists(f"{currentPath}/data/beton_amount_{expectId}.csv"):
                os.remove(f"{currentPath}/data/beton_amount_{expectId}.csv")
            if os.path.exists(f"{currentPath}/data/beton_amount_with_odds_{expectId}.csv"):
                os.remove(f"{currentPath}/data/beton_amount_with_odds_{expectId}.csv") 
            if os.path.exists(f"{currentPath}/data/opencode_amount_result_{expectId}.csv"):
                os.remove(f"{currentPath}/data/opencode_amount_result_{expectId}.csv") 
        except:
            logging.error("delete temp csv failed!!!")

        return Response(json.dumps(response, cls=NumpyEncoder), mimetype='application/json')
   
    return render_template('bestopen.html', title=title)

if __name__ == "__main__":
    global headers
    global program
    global context
    global opencodes
    global currentPath
    global opencode_answer_table

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

    with open(f"{currentPath}/data/beton_list.txt") as f:
        headers = f.read().split(',')
    #print(headers)

    # Create context and command queue
    platform = cl.get_platforms()[0]
    devices = platform.get_devices()
    context = cl.Context(devices)
    program = program_build( f"{currentPath}/kernels/kernel_program.cl")

    app.config["DEBUG"] = True
    app.run(host='0.0.0.0', port=5000)