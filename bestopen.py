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
import pyopencl as cl
import time

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

def program_build(kernel_file = 'kernels/kernel_program.cl'): 
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

def sum_selection_total_amount(selection, wagers, wager_length=10000):
    queue = cl.CommandQueue(context)
    tStart = time.time()#計時開始

    # create buffer READ/WRITE  cl.mem_flags.READ_WRITE
    buffer_selection = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=selection)
    buffer_wagers = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=wagers)
    buffer_result = cl.Buffer(context, cl.mem_flags.WRITE_ONLY,  size = selection.nbytes) 
 
    selection_length = len(selection)
    event = program.sum_selection_total_amount(
                    queue, (selection_length, ), (1, ),
                    buffer_selection, 
                    buffer_wagers,
                    buffer_result,
                    np.int32(wager_length))
    event.wait()

    # Read data back from buffer
    result = np.array(selection, dtype=np.float32)
    cl.enqueue_copy(queue, result, buffer_result)
    queue.flush()

    tEnd = time.time()#計時結束
    print("It cost %f sec" % (tEnd - tStart))#會自動做近位
    return result

def calc_numbers_risk(selection):
    queue = cl.CommandQueue(context)
    print("selection=", selection)
    print("selection.shape=", selection.shape)

    #numbers = np.random.randint(2, size=(selection_length * numbers_length)).astype(np.float32)
    #numbers = np.array(numbers[:-1]).flatten().astype(np.float32)
    print("numbers=", numbers)
    print("numbers.shape=", numbers.shape)

    result = np.empty(numbers_length, dtype=np.float32)

    tStart = time.time() 
    # create buffer READ/WRITE  cl.mem_flags.READ_WRITE
    buffer_selection = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=selection)
    buffer_numbers = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=numbers)
    buffer_result = cl.Buffer(context, cl.mem_flags.READ_WRITE,  result.nbytes)

    # Create, configure, and execute kernel (Seems too easy, doesn't it?)
    global_work_offset = (0, )
    global_work_size = (numbers_length, )
    local_work_size = (1, )
    kernel = program.calc_numbers_risk
    kernel.set_arg(0, buffer_selection)
    kernel.set_arg(1, buffer_numbers)
    kernel.set_arg(2, buffer_result)
    kernel.set_arg(3, np.int32(selection_length))

    ev = cl.enqueue_nd_range_kernel(queue, kernel, global_work_size, local_work_size, global_work_offset)

    # Read data back from buffer
    result = np.empty(numbers_length, dtype=np.float32)
    cl.enqueue_copy(queue, result, buffer_result)
    queue.flush()
    #print("result=", result)

    tEnd = time.time( )
    print("It cost %f sec" % (tEnd - tStart)) 
    return result
# =================================================

@app.route('/', methods=['GET'])
def home():
    return "<h1>最佳化開獎策略!</h1>"

@app.route("/bestopen", methods=['GET', 'POST'])
def submit():
    title = '最佳化開獎策略'
    if request.method == 'POST':
        #print('request.form', request.data)
        betOn_rows = []
        raw_data = request.get_data().decode("utf-8")
        logging.debug(f"row data: {raw_data}")
        jdata = json.loads(raw_data)
        #print(jdata["Bets"])
        for bet in jdata["Bets"]:
            betTypePlayCode = bet['BetTypePlayCode']
            unitAmount = bet["UnitAmount"]
            rawBetOn = bet["BetOn"]
            betOnCount = int(bet["BetOnCount"])
            #logging.debug(f"BetTypePlayCode={betTypePlayCode}, BetOn={rawBetOn}, UnitAmount={unitAmount}, betOnCount={betOnCount}")
            extraData = json.loads(bet["ExtraData"])
            odds = []
            for i in range(betOnCount):
                if len(extraData["ExtraBets"]) == 1:
                    odds.append(extraData["ExtraBets"][0]["Odds"])
                else:
                    odds.append(extraData["ExtraBets"][i]["Odds"])
            #logging.debug(odds)

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
            betOn_rows.append(row)

        #print(betOn_rows)
        wager_length = len(betOn_rows)
        logging.debug(f"get {len(betOn_rows)} rows.")
        #=========================================================
        column_length = len(header);
        A = np.ones(column_length).astype(np.float32)
        #print("A=", A)

        max_wager_length = 20000
        for i in range(max_wager_length - len(betOn_rows)):
            betOn_rows.append(np.zeros(column_length))

        B = np.array(betOn_rows).flatten().astype(np.float32)
        #print("B=", B)
        print(f"selection_length={column_length}, wager_length={wager_length}, max_wager_length={max_wager_length}")
        result = sum_selection_total_amount(A, B, max_wager_length)
        logging.debug(f"result:{result}")
        #logging.debug("result length :", len(result))
        #logging.debug(sum(result))

        result2 = calc_numbers_risk(result)
        logging.debug(f"result2:{result2}")

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

if __name__ == "__main__":
    global header
    global program
    global context
    global numbers
    global numbers_length
    global selection_length

    data = pd.read_csv("opencode_table.csv", nrows=0)
    header = data.columns[1:-1]
    print("column count : " +str(len(header)))

    print("current path:", os.path.abspath(__file__))
     # Create context and command queue
    platform = cl.get_platforms()[0]
    devices = platform.get_devices()
    context = cl.Context(devices)
    program = program_build()

    print("load opencode table....")
    row_numbers = pd.read_csv('opencode_table_1.csv')
    row_numbers = row_numbers[row_numbers.columns[:-1]]
    numbers_length = row_numbers.shape[0]
    numbers = np.array(row_numbers[:-1]).flatten().astype(np.float32)
    selection_length = 1056
    print("selection size=", selection_length, ", numbers=",  numbers_length)

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
    app.config["DEBUG"] = False
    app.run(host='0.0.0.0', port=5000)