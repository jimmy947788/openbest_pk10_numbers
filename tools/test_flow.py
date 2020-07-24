#!/usr/bin/python
 
import os
import sys
import json
import logging
import datetime
from pathlib import Path
from flask import Flask, request, render_template , Response
import numpy as np
import pandas as pd
import itertools
import pyopencl as cl
import time
from itertools import islice
import socket

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

# 轉換betOn格式
# =================================================
def SUM(rawBetOn):
    betOn=[]
    for b in rawBetOn.split(' '):
        betOn.append(f"SUM{b}")
    return betOn

def SUM_BSOE(rawBetOn):
    betOn=[]
    for b in rawBetOn.split(' '):
        betOn.append("SUM" + b)
    return betOn

def BSOE(rawBetOn):
    betOn=[]
    pos = 1
    for beton_pos in rawBetOn.split(','):
        for beton in beton_pos.split(' '):
            betOn.append(f"{beton}{pos}")
        pos+=1
    return betOn

def DWD(rawBetOn):
    betOn=[]
    pos = 1
    for num_pos in rawBetOn.split(','):
        for num in num_pos.split(' '):
            betOn.append(f"DWD{pos}_{num}")
        pos+=1
    return betOn

def DT(rawBetOn):
    betOn=[]
    pos = 1
    for beton_pos in rawBetOn.split(','):
        for beton in beton_pos.split(' '):
            betOn.append(f"{beton}{pos}")
        pos+=1
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
            if fb1 != fb2:
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
                betOnName = "TZF3_" +fb1 + "-" + fb2 + "-" + fb3
                if fb1 != fb2 and  fb1 != fb3 and fb2 != fb1 and fb2 != fb3:
                    betOn.append(betOnName)
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

def transferWager(raw_data):
    beton_amount_table = []
    beton_amount_odds_table = []
    jdata = json.loads(raw_data)
    total_bet_count = 0
    total_bet_amount = 0
    
    expectId = jdata["ExpectID"]
    for bet in jdata["Bets"]:
        betTypePlayCode = bet['BetTypePlayCode']
        unitAmount = bet["UnitAmount"]
        rawBetOn = bet["BetOn"]
        betOnCount = int(bet["BetOnCount"])
        killRate =  0.2 #bet["KillRate"]
        tolerance = 25 #bet["Tolerance"] 
        opencodeCount = 50

        #logging.debug(f"BetTypePlayCode={betTypePlayCode}, BetOn={rawBetOn}, UnitAmount={unitAmount}, betOnCount={betOnCount}")
        extraData = json.loads(bet["ExtraData"])
        odds = []
        betOn = []
        for i in range(betOnCount):
            if len(extraData["ExtraBets"]) == 1:
                odds.append(extraData["ExtraBets"][0]["Odds"])
            else:
                odds.append(extraData["ExtraBets"][i]["Odds"])

        # betTypePlayCode 轉換成解答表格式
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

        row_by_amount = []
        row_by_amount_odds = []
        i=0
        for h in headers:
            if h in betOn:
                row_by_amount.append(unitAmount)
                row_by_amount_odds.append((odds[i]-1) * unitAmount) #此處賠率要扣掉1（本金）
                total_bet_count += 1
                total_bet_amount += unitAmount
                i+=1
            else:
                row_by_amount.append(0)
                row_by_amount_odds.append(0)

        beton_amount_table.append(row_by_amount)
        beton_amount_odds_table.append(row_by_amount_odds)

    target_amount = total_bet_amount * killRate * -1
    logging.info(f"total_bet_count={total_bet_count}, total_bet_amount={total_bet_amount}")
    return (beton_amount_table, beton_amount_odds_table, total_bet_count, expectId, target_amount, tolerance, opencodeCount)



def submit():
    
    #print('request.form', request.data)
    betOn_rows = []
    #raw_data = request.get_data().decode("utf-8")
    with open(f"{currentPath}/data/test_wager_data.txt") as f:
        raw_data = f.read()
    logging.debug(f"row data: {raw_data}")
    
    (beton_amount_table, beton_amount_odds_table, total_bet_count, expectId, target_amount, tolerance, opencodeCount)= transferWager(raw_data)
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
        
        serverMessage = client.recv(1048576).decode("UTF-8")
        print('Server:', serverMessage)
    
    end = time.time()
    print(end - start)

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
    program = program_build()

    submit()