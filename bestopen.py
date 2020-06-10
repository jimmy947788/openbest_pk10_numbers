#!/usr/bin/python
 
import os
import sys
import json
import logging
import datetime
from pathlib import Path
from flask import Flask, request, render_template  
import numpy as np
import pandas as pd
import itertools

app = Flask(__name__)

# 轉換betOn格式
# =================================================
def SUM(rawBetOn):
    betOn=[]
    for b in rawBetOn.split(' '):
        str1 = '-'.join(str(e) for e in b)
        betOn.append("SUM" + str1)
    return betOn

def SUM_BSOE(rawBetOn):
    betOn=[]
    for b in rawBetOn.split(' '):
        betOn.append("SUM" + b)
    return betOn

def BSOE(rawBetOn):
    betOn=[]
    for i in range(10):
        b = rawBetOn.split(',')[i]
        pos = str(i+1)
        betOn.append(b+pos)
    return betOn

def DWD(rawBetOn):
    betOn=[]
    for i in range(10):
        b = rawBetOn.split(',')[i]
        pos = str(i+1)
        betOn.append("DWD"+pos+"_"+b)
    return betOn

def DT(rawBetOn):
    betOn=[]
    for i in range(5):
        b = rawBetOn.split(',')[i]
        pos = str(i+1)
        betOn.append(b+pos)
    return betOn

def TZF1(rawBetOn):
    betOn=[]
    for b in rawBetOn.split(' '):
        betOn.append("TZF1_" + b)
    return betOn

def TZF2(rawBetOn):
    betOn=[]
    f1 = rawBetOn.split(',')[0]
    f2 = rawBetOn.split(',')[1]
    for fb1 in f1.split(' '):
        for fb2 in f2.split(' '):
            betOn.append("TZF2_" +fb1 + "-" + fb2)
    return betOn

def TZF3(rawBetOn):
    betOn=[]
    f1 = rawBetOn.split(',')[0]
    f2 = rawBetOn.split(',')[1]
    f3 = rawBetOn.split(',')[2]
    for fb1 in f1.split(' '):
        for fb2 in f2.split(' '):
            for fb3 in f3.split(' '):
                betOn.append("TZF3_" +fb1 + "-" + fb2 + "-" + fb3)
    return betOn

def TSZF2(rawBetOn):
    betOn=[]
    for b in  list(itertools.combinations(rawBetOn.split(' '), 2)):
        str1 = '-'.join(str(e) for e in b)
        betOn.append("TSZF2_" + str1)
    return betOn
# =================================================

@app.route('/', methods=['GET'])
def home():
    return "<h1>最佳化開獎策略!</h1>"

@app.route("/bestopen", methods=['GET', 'POST'])
def submit():
    title = '最佳化開獎策略'
    if request.method == 'POST':
        #print('request.form', request.data)
        rows = []
        row_data = request.get_data().decode("utf-8")
        logging.debug(f"row data: {row_data}")
        jdata = json.loads(row_data)
        #print(jdata["Bets"])
        for bet in jdata["Bets"]:
            betTypePlayCode = bet['BetTypePlayCode']
            unitAmount = bet["UnitAmount"]
            rawBetOn = bet["BetOn"]
            betOnCount = int(bet["BetOnCount"])
            logging.debug(f"BetTypePlayCode={betTypePlayCode}, BetOn={rawBetOn}, UnitAmount={unitAmount}, betOnCount={betOnCount}")
            extraData = json.loads(bet["ExtraData"])
            #print(extraData)
            #print(extraData["ExtraBets"])
            #for beat in extraData["ExtraBets"]:
            #    odds = beat["Odds"]
            #    print(odds)
            odds = []
            for i in range(betOnCount):
                if len(extraData["ExtraBets"]) == 1:
                    odds.append(extraData["ExtraBets"][0]["Odds"])
                else:
                    odds.append(extraData["ExtraBets"][i]["Odds"])
            logging.debug(odds)

            if betTypePlayCode == "O_12Sum":
                betOn=SUM(rawBetOn)
            elif betTypePlayCode == "O_12Sum_BSOE":
                betOn=SUM_BSOE(rawBetOn)
            elif betTypePlayCode == "O_BSOE":
                betOn=BSOE(rawBetOn)
            elif betTypePlayCode == "O_DingWeiDan":
                betOn=DWD(rawBetOn)
            elif betTypePlayCode == "O_DragonTiger":
                betOn=DT(rawBetOn)
            elif betTypePlayCode == "O_ThreeStar_Zhi_Front1":
                betOn=TZF1(rawBetOn)
            elif betTypePlayCode == "O_ThreeStar_Zhi_Front2":
                betOn=TZF2(rawBetOn)
            elif betTypePlayCode == "O_ThreeStar_Zhi_Front3":
                betOn=TZF3(rawBetOn)
            elif betTypePlayCode == "O_TwoStar_Zu_Front2":
                betOn=TSZF2(rawBetOn)
            elif betTypePlayCode == "PK10_1":
                betOn=["DWD1_" + str(int(rawBetOn))]
            elif betTypePlayCode == "PK10_1BS" or betTypePlayCode == "PK10_1DT" or  betTypePlayCode == "PK10_1OE" or betTypePlayCode == "PK10_1PC":
                betOn=[rawBetOn + "1"]
            elif betTypePlayCode == "PK10_2":
                betOn=["DWD2_" + str(int(rawBetOn))]
            elif betTypePlayCode == "PK10_2BS" or betTypePlayCode == "PK10_2DT" or  betTypePlayCode == "PK10_2OE" or betTypePlayCode == "PK10_2PC":
                betOn=[rawBetOn + "2"]
            elif betTypePlayCode == "PK10_3":
                betOn=["DWD3_" + str(int(rawBetOn))]
            elif betTypePlayCode == "PK10_3BS" or betTypePlayCode == "PK10_3DT" or  betTypePlayCode == "PK10_3OE" or betTypePlayCode == "PK10_3PC":
                betOn=[rawBetOn + "3"]
            elif betTypePlayCode == "PK10_4":
                betOn=["DWD4_" + str(int(rawBetOn))]
            elif betTypePlayCode == "PK10_4BS" or betTypePlayCode == "PK10_4DT" or  betTypePlayCode == "PK10_4OE" or betTypePlayCode == "PK10_4PC":
                betOn=[rawBetOn + "4"]
            elif betTypePlayCode == "PK10_5":
                betOn=["DWD5_" + str(int(rawBetOn))]
            elif betTypePlayCode == "PK10_5BS" or betTypePlayCode == "PK10_5DT" or  betTypePlayCode == "PK10_5OE" or betTypePlayCode == "PK10_5PC":
                betOn=[rawBetOn + "5"]
            elif betTypePlayCode == "PK10_6":
                betOn=["DWD6_" + str(int(rawBetOn))]
            elif betTypePlayCode == "PK10_6BS" or  betTypePlayCode == "PK10_6OE" or betTypePlayCode == "PK10_6PC":
                betOn=[rawBetOn + "6"]
            elif betTypePlayCode == "PK10_7":
                betOn=["DWD7_" + str(int(rawBetOn))]
            elif betTypePlayCode == "PK10_7BS" or  betTypePlayCode == "PK10_7OE" or betTypePlayCode == "PK10_7PC":
                betOn=[rawBetOn + "7"]
            elif betTypePlayCode == "PK10_8":
                betOn=["DWD8_" + str(int(rawBetOn))]
            elif betTypePlayCode == "PK10_8BS" or  betTypePlayCode == "PK10_8OE" or betTypePlayCode == "PK10_8PC":
                betOn=[rawBetOn + "8"]
            elif betTypePlayCode == "PK10_9":
                betOn=["DWD9_" + str(int(rawBetOn))]
            elif betTypePlayCode == "PK10_9BS" or  betTypePlayCode == "PK10_9OE" or betTypePlayCode == "PK10_9PC":
                betOn=[rawBetOn + "9"]
            elif betTypePlayCode == "PK10_10":
                betOn=["DWD10_" + str(int(rawBetOn))]
            elif betTypePlayCode == "PK10_10BS" or  betTypePlayCode == "PK10_10OE" or betTypePlayCode == "PK10_10PC":
                betOn=[rawBetOn + "10"]
            elif "PK10_SUM_" in betTypePlayCode:
                betOn=["SUM" + str(int(rawBetOn))]
            elif betTypePlayCode == "PK10_SUMBS" or  betTypePlayCode == "PK10_SUMOE":
                betOn=["SUM" +rawBetOn]

            #print(betOn)
            row = []
            i=0
            for h in header:
                if h in betOn:
                    row.append(odds[i] * unitAmount )
                    i+=1
                else:
                    row.append(0)
              
            #print(row)
            rows.append(row)
        
        print(rows)
        
        response = { }
        response["code"] = 0
        response["msg"] = "success"
        response["result"] = {
            "rows":[
                {
                    "TotalAmountSum": 99999.24,
                    "WinAmountSum":55485,
                    "BetCount" : 555,
                    "OpenCode": "3,3,2"
                }
            ]
        }
        return response
    return render_template('bestopen.html', title=title)

header = []
if __name__ == "__main__":

    data = pd.read_csv("opencode_table.csv", nrows=0)
    header = data.columns[1:-1]
    print("column count : " +str(len(header)))

    if not os.path.exists("log"):
        os.mkdir("log")
    home_path = str(Path.home())
    log_fliename = datetime.datetime.now().strftime(f"log/opencode-%Y-%m-%d.log")
    print(f"log filename formate = {log_fliename}")
    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            datefmt='%m-%d %H:%M:%S',
            filename=log_fliename)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    app.config["DEBUG"] = True
    app.run(host='0.0.0.0', port=5000)