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

def beton_total_amount(one_vector_mask, amount_matrix, wager_length=10000):
    tStart = time.time()#計時開始
    queue = cl.CommandQueue(context)
    result = np.empty(len(one_vector_mask), dtype=np.float32)
    # create buffer READ/WRITE  cl.mem_flags.READ_WRITE
    buffer_mask = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=one_vector_mask)
    buffer_matrix = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=amount_matrix)
    buffer_result = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, size = result.nbytes) 
 
    selection_length = len(one_vector_mask)
    event = program.sum_beton_total_amount(
                    queue, (selection_length, ), (1, ),
                    buffer_mask, 
                    buffer_matrix,
                    buffer_result,
                    np.int32(wager_length))
    event.wait()

    # Read data back from buffer
    cl.enqueue_copy(queue, result, buffer_result)
    queue.flush()

    tEnd = time.time()#計時結束
    logging.info("It cost %f sec" % (tEnd - tStart))#會自動做近位
    return result

def calc_numbers_risk(total_amount_vector, total_amount_odds_vector):
    queue = cl.CommandQueue(context)
    numbers_length = len(opencodes)
    beton_length = len(headers);
    result = np.empty(numbers_length, dtype=np.float32)

    # opencode_table 降維
    opencode_answer = np.array(opencode_answer_table).flatten().astype(np.float32)
    logging.info(f"answer_table.shape={opencode_answer.shape}")

    tStart = time.time() 
    # create buffer READ/WRITE  cl.mem_flags.READ_WRITE
    buffer_total_amount = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=total_amount_vector)
    buffer_total_amount_odds = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=total_amount_odds_vector)
    buffer_answers = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=opencode_answer)
    buffer_result = cl.Buffer(context, cl.mem_flags.READ_WRITE,  result.nbytes)

    # Create, configure, and execute kernel (Seems too easy, doesn't it?)
    global_work_offset = (0, )
    global_work_size = (numbers_length, )
    local_work_size = (1, )
    kernel = program.calc_numbers_risk
    kernel.set_arg(0, buffer_total_amount)
    kernel.set_arg(1, buffer_total_amount_odds)
    kernel.set_arg(2, buffer_answers)
    kernel.set_arg(3, buffer_result)
    kernel.set_arg(4, np.int32(beton_length))

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
    return (beton_amount_table, beton_amount_odds_table, total_bet_count, expectId, target_amount, tolerance)

if __name__ == "__main__":

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

    logging.info(f"headers count : {len(headers)}")
    # Create context and command queue
    platform = cl.get_platforms()[0]
    devices = platform.get_devices()
    context = cl.Context(devices)
    program = program_build()
    
    with open(f"{currentPath}/data/test_wager_data.txt") as f:
        raw_data = f.read()
    # logging.debug(f"row data: {raw_data}")
    
    (beton_amount_table, beton_amount_odds_table, total_bet_count, expectId, target_amount, tolerance)= transferWager(raw_data)

    wager_length = len(beton_amount_table)
    logging.info(f"wager_length={wager_length}")
        
    # 計算每個beton投注總額
    #=========================================================
    column_length = len(headers);

    # 建立A= [ 1, 1, 1, 1, 1, ... ,1 ,1 ,1 ]
    one_vector_mask = np.ones(column_length).astype(np.ushort)
    logging.debug(f"one_vector_mask={one_vector_mask}, length={len(one_vector_mask)}")

    # 降維
    # 本金矩陣（只有本金）
    amount_matrix = np.array(beton_amount_table).flatten().astype(np.float32)
    logging.debug(f"amount_matrix={amount_matrix}, length={len(amount_matrix)}")
    
    # 獎金矩陣（本金*賠率-本金）
    amount_odds_matrix = np.array(beton_amount_odds_table).flatten().astype(np.float32)
    logging.debug(f"amount_odds_matrix={amount_odds_matrix}, length={len(amount_odds_matrix)}")
    
    # 本金矩陣（各beton加總）
    total_amount_result = beton_total_amount(one_vector_mask, amount_matrix, wager_length)
    logging.debug(f"total_amount_result:{total_amount_result}")
    
    # 獎金矩陣（各beton加總）
    total_amount_odds_result = beton_total_amount(one_vector_mask, amount_odds_matrix, wager_length)
    logging.debug(f"total_amount_odds_result:{total_amount_odds_result}")

    with open(f"{currentPath}/data/opencode_table_test.csv") as f:
        columns = f.read().splitlines()[0].split(',')
        answer = columns[1:]
        opencode = columns[0]
        print(answer)
    
    print("answer len:", len(answer))
    print("total_amount_odds_result len:", len(total_amount_odds_result))
    print("total_amount_result len:", len(total_amount_result))

    sum = 0
    for i in range(1056):
        if int(answer[i]) > 0:
            sum += total_amount_odds_result[i] 
        else:
            sum += total_amount_result[i] * -1
    print(f"opencode={opencode}, amount={sum}")