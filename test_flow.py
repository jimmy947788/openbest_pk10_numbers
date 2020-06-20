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

    #numbers_answer = np.random.randint(2, size=(selection_length * numbers_length)).astype(np.float32)
    #numbers_answer = np.array(numbers[:-1]).flatten().astype(np.float32)
    print("numbers=", numbers_answer)
    print("numbers.shape=", numbers_answer.shape)

    result = np.empty(numbers_length, dtype=np.float32)

    tStart = time.time() 
    # create buffer READ/WRITE  cl.mem_flags.READ_WRITE
    buffer_selection = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=selection)
    buffer_numbers = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=numbers_answer)
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

def submit():
    title = '最佳化開獎策略'
   
    #print('request.form', request.data)
    betOn_rows = []
    with open("test_data.txt", 'r') as f:
        raw_data = f.read() # 讀取檔案內容

    logging.debug(f"row data: {raw_data}")

    jdata = json.loads(raw_data)
    total_bet_count = 0
    total_bet_amount = 0
    fo = open('odds_matrix.csv', 'w+', encoding='UTF-8')
    fb = open('beton_matrix.csv', 'w+', encoding='UTF-8')
    fb.write("DWD1_1,DWD1_2,DWD1_3,DWD1_4,DWD1_5,DWD1_6,DWD1_7,DWD1_8,DWD1_9,DWD1_10,DWD2_1,DWD2_2,DWD2_3,DWD2_4,DWD2_5,DWD2_6,DWD2_7,DWD2_8,DWD2_9,DWD2_10,DWD3_1,DWD3_2,DWD3_3,DWD3_4,DWD3_5,DWD3_6,DWD3_7,DWD3_8,DWD3_9,DWD3_10,DWD4_1,DWD4_2,DWD4_3,DWD4_4,DWD4_5,DWD4_6,DWD4_7,DWD4_8,DWD4_9,DWD4_10,DWD5_1,DWD5_2,DWD5_3,DWD5_4,DWD5_5,DWD5_6,DWD5_7,DWD5_8,DWD5_9,DWD5_10,DWD6_1,DWD6_2,DWD6_3,DWD6_4,DWD6_5,DWD6_6,DWD6_7,DWD6_8,DWD6_9,DWD6_10,DWD7_1,DWD7_2,DWD7_3,DWD7_4,DWD7_5,DWD7_6,DWD7_7,DWD7_8,DWD7_9,DWD7_10,DWD8_1,DWD8_2,DWD8_3,DWD8_4,DWD8_5,DWD8_6,DWD8_7,DWD8_8,DWD8_9,DWD8_10,DWD9_1,DWD9_2,DWD9_3,DWD9_4,DWD9_5,DWD9_6,DWD9_7,DWD9_8,DWD9_9,DWD9_10,DWD10_1,DWD10_2,DWD10_3,DWD10_4,DWD10_5,DWD10_6,DWD10_7,DWD10_8,DWD10_9,DWD10_10,TZF3_1-2-3,TZF3_1-2-4,TZF3_1-2-5,TZF3_1-2-6,TZF3_1-2-7,TZF3_1-2-8,TZF3_1-2-9,TZF3_1-2-10,TZF3_1-3-2,TZF3_1-3-4,TZF3_1-3-5,TZF3_1-3-6,TZF3_1-3-7,TZF3_1-3-8,TZF3_1-3-9,TZF3_1-3-10,TZF3_1-4-2,TZF3_1-4-3,TZF3_1-4-5,TZF3_1-4-6,TZF3_1-4-7,TZF3_1-4-8,TZF3_1-4-9,TZF3_1-4-10,TZF3_1-5-2,TZF3_1-5-3,TZF3_1-5-4,TZF3_1-5-6,TZF3_1-5-7,TZF3_1-5-8,TZF3_1-5-9,TZF3_1-5-10,TZF3_1-6-2,TZF3_1-6-3,TZF3_1-6-4,TZF3_1-6-5,TZF3_1-6-7,TZF3_1-6-8,TZF3_1-6-9,TZF3_1-6-10,TZF3_1-7-2,TZF3_1-7-3,TZF3_1-7-4,TZF3_1-7-5,TZF3_1-7-6,TZF3_1-7-8,TZF3_1-7-9,TZF3_1-7-10,TZF3_1-8-2,TZF3_1-8-3,TZF3_1-8-4,TZF3_1-8-5,TZF3_1-8-6,TZF3_1-8-7,TZF3_1-8-9,TZF3_1-8-10,TZF3_1-9-2,TZF3_1-9-3,TZF3_1-9-4,TZF3_1-9-5,TZF3_1-9-6,TZF3_1-9-7,TZF3_1-9-8,TZF3_1-9-10,TZF3_1-10-2,TZF3_1-10-3,TZF3_1-10-4,TZF3_1-10-5,TZF3_1-10-6,TZF3_1-10-7,TZF3_1-10-8,TZF3_1-10-9,TZF3_2-1-3,TZF3_2-1-4,TZF3_2-1-5,TZF3_2-1-6,TZF3_2-1-7,TZF3_2-1-8,TZF3_2-1-9,TZF3_2-1-10,TZF3_2-3-1,TZF3_2-3-4,TZF3_2-3-5,TZF3_2-3-6,TZF3_2-3-7,TZF3_2-3-8,TZF3_2-3-9,TZF3_2-3-10,TZF3_2-4-1,TZF3_2-4-3,TZF3_2-4-5,TZF3_2-4-6,TZF3_2-4-7,TZF3_2-4-8,TZF3_2-4-9,TZF3_2-4-10,TZF3_2-5-1,TZF3_2-5-3,TZF3_2-5-4,TZF3_2-5-6,TZF3_2-5-7,TZF3_2-5-8,TZF3_2-5-9,TZF3_2-5-10,TZF3_2-6-1,TZF3_2-6-3,TZF3_2-6-4,TZF3_2-6-5,TZF3_2-6-7,TZF3_2-6-8,TZF3_2-6-9,TZF3_2-6-10,TZF3_2-7-1,TZF3_2-7-3,TZF3_2-7-4,TZF3_2-7-5,TZF3_2-7-6,TZF3_2-7-8,TZF3_2-7-9,TZF3_2-7-10,TZF3_2-8-1,TZF3_2-8-3,TZF3_2-8-4,TZF3_2-8-5,TZF3_2-8-6,TZF3_2-8-7,TZF3_2-8-9,TZF3_2-8-10,TZF3_2-9-1,TZF3_2-9-3,TZF3_2-9-4,TZF3_2-9-5,TZF3_2-9-6,TZF3_2-9-7,TZF3_2-9-8,TZF3_2-9-10,TZF3_2-10-1,TZF3_2-10-3,TZF3_2-10-4,TZF3_2-10-5,TZF3_2-10-6,TZF3_2-10-7,TZF3_2-10-8,TZF3_2-10-9,TZF3_3-1-2,TZF3_3-1-4,TZF3_3-1-5,TZF3_3-1-6,TZF3_3-1-7,TZF3_3-1-8,TZF3_3-1-9,TZF3_3-1-10,TZF3_3-2-1,TZF3_3-2-4,TZF3_3-2-5,TZF3_3-2-6,TZF3_3-2-7,TZF3_3-2-8,TZF3_3-2-9,TZF3_3-2-10,TZF3_3-4-1,TZF3_3-4-2,TZF3_3-4-5,TZF3_3-4-6,TZF3_3-4-7,TZF3_3-4-8,TZF3_3-4-9,TZF3_3-4-10,TZF3_3-5-1,TZF3_3-5-2,TZF3_3-5-4,TZF3_3-5-6,TZF3_3-5-7,TZF3_3-5-8,TZF3_3-5-9,TZF3_3-5-10,TZF3_3-6-1,TZF3_3-6-2,TZF3_3-6-4,TZF3_3-6-5,TZF3_3-6-7,TZF3_3-6-8,TZF3_3-6-9,TZF3_3-6-10,TZF3_3-7-1,TZF3_3-7-2,TZF3_3-7-4,TZF3_3-7-5,TZF3_3-7-6,TZF3_3-7-8,TZF3_3-7-9,TZF3_3-7-10,TZF3_3-8-1,TZF3_3-8-2,TZF3_3-8-4,TZF3_3-8-5,TZF3_3-8-6,TZF3_3-8-7,TZF3_3-8-9,TZF3_3-8-10,TZF3_3-9-1,TZF3_3-9-2,TZF3_3-9-4,TZF3_3-9-5,TZF3_3-9-6,TZF3_3-9-7,TZF3_3-9-8,TZF3_3-9-10,TZF3_3-10-1,TZF3_3-10-2,TZF3_3-10-4,TZF3_3-10-5,TZF3_3-10-6,TZF3_3-10-7,TZF3_3-10-8,TZF3_3-10-9,TZF3_4-1-2,TZF3_4-1-3,TZF3_4-1-5,TZF3_4-1-6,TZF3_4-1-7,TZF3_4-1-8,TZF3_4-1-9,TZF3_4-1-10,TZF3_4-2-1,TZF3_4-2-3,TZF3_4-2-5,TZF3_4-2-6,TZF3_4-2-7,TZF3_4-2-8,TZF3_4-2-9,TZF3_4-2-10,TZF3_4-3-1,TZF3_4-3-2,TZF3_4-3-5,TZF3_4-3-6,TZF3_4-3-7,TZF3_4-3-8,TZF3_4-3-9,TZF3_4-3-10,TZF3_4-5-1,TZF3_4-5-2,TZF3_4-5-3,TZF3_4-5-6,TZF3_4-5-7,TZF3_4-5-8,TZF3_4-5-9,TZF3_4-5-10,TZF3_4-6-1,TZF3_4-6-2,TZF3_4-6-3,TZF3_4-6-5,TZF3_4-6-7,TZF3_4-6-8,TZF3_4-6-9,TZF3_4-6-10,TZF3_4-7-1,TZF3_4-7-2,TZF3_4-7-3,TZF3_4-7-5,TZF3_4-7-6,TZF3_4-7-8,TZF3_4-7-9,TZF3_4-7-10,TZF3_4-8-1,TZF3_4-8-2,TZF3_4-8-3,TZF3_4-8-5,TZF3_4-8-6,TZF3_4-8-7,TZF3_4-8-9,TZF3_4-8-10,TZF3_4-9-1,TZF3_4-9-2,TZF3_4-9-3,TZF3_4-9-5,TZF3_4-9-6,TZF3_4-9-7,TZF3_4-9-8,TZF3_4-9-10,TZF3_4-10-1,TZF3_4-10-2,TZF3_4-10-3,TZF3_4-10-5,TZF3_4-10-6,TZF3_4-10-7,TZF3_4-10-8,TZF3_4-10-9,TZF3_5-1-2,TZF3_5-1-3,TZF3_5-1-4,TZF3_5-1-6,TZF3_5-1-7,TZF3_5-1-8,TZF3_5-1-9,TZF3_5-1-10,TZF3_5-2-1,TZF3_5-2-3,TZF3_5-2-4,TZF3_5-2-6,TZF3_5-2-7,TZF3_5-2-8,TZF3_5-2-9,TZF3_5-2-10,TZF3_5-3-1,TZF3_5-3-2,TZF3_5-3-4,TZF3_5-3-6,TZF3_5-3-7,TZF3_5-3-8,TZF3_5-3-9,TZF3_5-3-10,TZF3_5-4-1,TZF3_5-4-2,TZF3_5-4-3,TZF3_5-4-6,TZF3_5-4-7,TZF3_5-4-8,TZF3_5-4-9,TZF3_5-4-10,TZF3_5-6-1,TZF3_5-6-2,TZF3_5-6-3,TZF3_5-6-4,TZF3_5-6-7,TZF3_5-6-8,TZF3_5-6-9,TZF3_5-6-10,TZF3_5-7-1,TZF3_5-7-2,TZF3_5-7-3,TZF3_5-7-4,TZF3_5-7-6,TZF3_5-7-8,TZF3_5-7-9,TZF3_5-7-10,TZF3_5-8-1,TZF3_5-8-2,TZF3_5-8-3,TZF3_5-8-4,TZF3_5-8-6,TZF3_5-8-7,TZF3_5-8-9,TZF3_5-8-10,TZF3_5-9-1,TZF3_5-9-2,TZF3_5-9-3,TZF3_5-9-4,TZF3_5-9-6,TZF3_5-9-7,TZF3_5-9-8,TZF3_5-9-10,TZF3_5-10-1,TZF3_5-10-2,TZF3_5-10-3,TZF3_5-10-4,TZF3_5-10-6,TZF3_5-10-7,TZF3_5-10-8,TZF3_5-10-9,TZF3_6-1-2,TZF3_6-1-3,TZF3_6-1-4,TZF3_6-1-5,TZF3_6-1-7,TZF3_6-1-8,TZF3_6-1-9,TZF3_6-1-10,TZF3_6-2-1,TZF3_6-2-3,TZF3_6-2-4,TZF3_6-2-5,TZF3_6-2-7,TZF3_6-2-8,TZF3_6-2-9,TZF3_6-2-10,TZF3_6-3-1,TZF3_6-3-2,TZF3_6-3-4,TZF3_6-3-5,TZF3_6-3-7,TZF3_6-3-8,TZF3_6-3-9,TZF3_6-3-10,TZF3_6-4-1,TZF3_6-4-2,TZF3_6-4-3,TZF3_6-4-5,TZF3_6-4-7,TZF3_6-4-8,TZF3_6-4-9,TZF3_6-4-10,TZF3_6-5-1,TZF3_6-5-2,TZF3_6-5-3,TZF3_6-5-4,TZF3_6-5-7,TZF3_6-5-8,TZF3_6-5-9,TZF3_6-5-10,TZF3_6-7-1,TZF3_6-7-2,TZF3_6-7-3,TZF3_6-7-4,TZF3_6-7-5,TZF3_6-7-8,TZF3_6-7-9,TZF3_6-7-10,TZF3_6-8-1,TZF3_6-8-2,TZF3_6-8-3,TZF3_6-8-4,TZF3_6-8-5,TZF3_6-8-7,TZF3_6-8-9,TZF3_6-8-10,TZF3_6-9-1,TZF3_6-9-2,TZF3_6-9-3,TZF3_6-9-4,TZF3_6-9-5,TZF3_6-9-7,TZF3_6-9-8,TZF3_6-9-10,TZF3_6-10-1,TZF3_6-10-2,TZF3_6-10-3,TZF3_6-10-4,TZF3_6-10-5,TZF3_6-10-7,TZF3_6-10-8,TZF3_6-10-9,TZF3_7-1-2,TZF3_7-1-3,TZF3_7-1-4,TZF3_7-1-5,TZF3_7-1-6,TZF3_7-1-8,TZF3_7-1-9,TZF3_7-1-10,TZF3_7-2-1,TZF3_7-2-3,TZF3_7-2-4,TZF3_7-2-5,TZF3_7-2-6,TZF3_7-2-8,TZF3_7-2-9,TZF3_7-2-10,TZF3_7-3-1,TZF3_7-3-2,TZF3_7-3-4,TZF3_7-3-5,TZF3_7-3-6,TZF3_7-3-8,TZF3_7-3-9,TZF3_7-3-10,TZF3_7-4-1,TZF3_7-4-2,TZF3_7-4-3,TZF3_7-4-5,TZF3_7-4-6,TZF3_7-4-8,TZF3_7-4-9,TZF3_7-4-10,TZF3_7-5-1,TZF3_7-5-2,TZF3_7-5-3,TZF3_7-5-4,TZF3_7-5-6,TZF3_7-5-8,TZF3_7-5-9,TZF3_7-5-10,TZF3_7-6-1,TZF3_7-6-2,TZF3_7-6-3,TZF3_7-6-4,TZF3_7-6-5,TZF3_7-6-8,TZF3_7-6-9,TZF3_7-6-10,TZF3_7-8-1,TZF3_7-8-2,TZF3_7-8-3,TZF3_7-8-4,TZF3_7-8-5,TZF3_7-8-6,TZF3_7-8-9,TZF3_7-8-10,TZF3_7-9-1,TZF3_7-9-2,TZF3_7-9-3,TZF3_7-9-4,TZF3_7-9-5,TZF3_7-9-6,TZF3_7-9-8,TZF3_7-9-10,TZF3_7-10-1,TZF3_7-10-2,TZF3_7-10-3,TZF3_7-10-4,TZF3_7-10-5,TZF3_7-10-6,TZF3_7-10-8,TZF3_7-10-9,TZF3_8-1-2,TZF3_8-1-3,TZF3_8-1-4,TZF3_8-1-5,TZF3_8-1-6,TZF3_8-1-7,TZF3_8-1-9,TZF3_8-1-10,TZF3_8-2-1,TZF3_8-2-3,TZF3_8-2-4,TZF3_8-2-5,TZF3_8-2-6,TZF3_8-2-7,TZF3_8-2-9,TZF3_8-2-10,TZF3_8-3-1,TZF3_8-3-2,TZF3_8-3-4,TZF3_8-3-5,TZF3_8-3-6,TZF3_8-3-7,TZF3_8-3-9,TZF3_8-3-10,TZF3_8-4-1,TZF3_8-4-2,TZF3_8-4-3,TZF3_8-4-5,TZF3_8-4-6,TZF3_8-4-7,TZF3_8-4-9,TZF3_8-4-10,TZF3_8-5-1,TZF3_8-5-2,TZF3_8-5-3,TZF3_8-5-4,TZF3_8-5-6,TZF3_8-5-7,TZF3_8-5-9,TZF3_8-5-10,TZF3_8-6-1,TZF3_8-6-2,TZF3_8-6-3,TZF3_8-6-4,TZF3_8-6-5,TZF3_8-6-7,TZF3_8-6-9,TZF3_8-6-10,TZF3_8-7-1,TZF3_8-7-2,TZF3_8-7-3,TZF3_8-7-4,TZF3_8-7-5,TZF3_8-7-6,TZF3_8-7-9,TZF3_8-7-10,TZF3_8-9-1,TZF3_8-9-2,TZF3_8-9-3,TZF3_8-9-4,TZF3_8-9-5,TZF3_8-9-6,TZF3_8-9-7,TZF3_8-9-10,TZF3_8-10-1,TZF3_8-10-2,TZF3_8-10-3,TZF3_8-10-4,TZF3_8-10-5,TZF3_8-10-6,TZF3_8-10-7,TZF3_8-10-9,TZF3_9-1-2,TZF3_9-1-3,TZF3_9-1-4,TZF3_9-1-5,TZF3_9-1-6,TZF3_9-1-7,TZF3_9-1-8,TZF3_9-1-10,TZF3_9-2-1,TZF3_9-2-3,TZF3_9-2-4,TZF3_9-2-5,TZF3_9-2-6,TZF3_9-2-7,TZF3_9-2-8,TZF3_9-2-10,TZF3_9-3-1,TZF3_9-3-2,TZF3_9-3-4,TZF3_9-3-5,TZF3_9-3-6,TZF3_9-3-7,TZF3_9-3-8,TZF3_9-3-10,TZF3_9-4-1,TZF3_9-4-2,TZF3_9-4-3,TZF3_9-4-5,TZF3_9-4-6,TZF3_9-4-7,TZF3_9-4-8,TZF3_9-4-10,TZF3_9-5-1,TZF3_9-5-2,TZF3_9-5-3,TZF3_9-5-4,TZF3_9-5-6,TZF3_9-5-7,TZF3_9-5-8,TZF3_9-5-10,TZF3_9-6-1,TZF3_9-6-2,TZF3_9-6-3,TZF3_9-6-4,TZF3_9-6-5,TZF3_9-6-7,TZF3_9-6-8,TZF3_9-6-10,TZF3_9-7-1,TZF3_9-7-2,TZF3_9-7-3,TZF3_9-7-4,TZF3_9-7-5,TZF3_9-7-6,TZF3_9-7-8,TZF3_9-7-10,TZF3_9-8-1,TZF3_9-8-2,TZF3_9-8-3,TZF3_9-8-4,TZF3_9-8-5,TZF3_9-8-6,TZF3_9-8-7,TZF3_9-8-10,TZF3_9-10-1,TZF3_9-10-2,TZF3_9-10-3,TZF3_9-10-4,TZF3_9-10-5,TZF3_9-10-6,TZF3_9-10-7,TZF3_9-10-8,TZF3_10-1-2,TZF3_10-1-3,TZF3_10-1-4,TZF3_10-1-5,TZF3_10-1-6,TZF3_10-1-7,TZF3_10-1-8,TZF3_10-1-9,TZF3_10-2-1,TZF3_10-2-3,TZF3_10-2-4,TZF3_10-2-5,TZF3_10-2-6,TZF3_10-2-7,TZF3_10-2-8,TZF3_10-2-9,TZF3_10-3-1,TZF3_10-3-2,TZF3_10-3-4,TZF3_10-3-5,TZF3_10-3-6,TZF3_10-3-7,TZF3_10-3-8,TZF3_10-3-9,TZF3_10-4-1,TZF3_10-4-2,TZF3_10-4-3,TZF3_10-4-5,TZF3_10-4-6,TZF3_10-4-7,TZF3_10-4-8,TZF3_10-4-9,TZF3_10-5-1,TZF3_10-5-2,TZF3_10-5-3,TZF3_10-5-4,TZF3_10-5-6,TZF3_10-5-7,TZF3_10-5-8,TZF3_10-5-9,TZF3_10-6-1,TZF3_10-6-2,TZF3_10-6-3,TZF3_10-6-4,TZF3_10-6-5,TZF3_10-6-7,TZF3_10-6-8,TZF3_10-6-9,TZF3_10-7-1,TZF3_10-7-2,TZF3_10-7-3,TZF3_10-7-4,TZF3_10-7-5,TZF3_10-7-6,TZF3_10-7-8,TZF3_10-7-9,TZF3_10-8-1,TZF3_10-8-2,TZF3_10-8-3,TZF3_10-8-4,TZF3_10-8-5,TZF3_10-8-6,TZF3_10-8-7,TZF3_10-8-9,TZF3_10-9-1,TZF3_10-9-2,TZF3_10-9-3,TZF3_10-9-4,TZF3_10-9-5,TZF3_10-9-6,TZF3_10-9-7,TZF3_10-9-8,TZF2_1-2,TZF2_1-3,TZF2_1-4,TZF2_1-5,TZF2_1-6,TZF2_1-7,TZF2_1-8,TZF2_1-9,TZF2_1-10,TZF2_2-1,TZF2_2-3,TZF2_2-4,TZF2_2-5,TZF2_2-6,TZF2_2-7,TZF2_2-8,TZF2_2-9,TZF2_2-10,TZF2_3-1,TZF2_3-2,TZF2_3-4,TZF2_3-5,TZF2_3-6,TZF2_3-7,TZF2_3-8,TZF2_3-9,TZF2_3-10,TZF2_4-1,TZF2_4-2,TZF2_4-3,TZF2_4-5,TZF2_4-6,TZF2_4-7,TZF2_4-8,TZF2_4-9,TZF2_4-10,TZF2_5-1,TZF2_5-2,TZF2_5-3,TZF2_5-4,TZF2_5-6,TZF2_5-7,TZF2_5-8,TZF2_5-9,TZF2_5-10,TZF2_6-1,TZF2_6-2,TZF2_6-3,TZF2_6-4,TZF2_6-5,TZF2_6-7,TZF2_6-8,TZF2_6-9,TZF2_6-10,TZF2_7-1,TZF2_7-2,TZF2_7-3,TZF2_7-4,TZF2_7-5,TZF2_7-6,TZF2_7-8,TZF2_7-9,TZF2_7-10,TZF2_8-1,TZF2_8-2,TZF2_8-3,TZF2_8-4,TZF2_8-5,TZF2_8-6,TZF2_8-7,TZF2_8-9,TZF2_8-10,TZF2_9-1,TZF2_9-2,TZF2_9-3,TZF2_9-4,TZF2_9-5,TZF2_9-6,TZF2_9-7,TZF2_9-8,TZF2_9-10,TZF2_10-1,TZF2_10-2,TZF2_10-3,TZF2_10-4,TZF2_10-5,TZF2_10-6,TZF2_10-7,TZF2_10-8,TZF2_10-9,TZF1_1,TZF1_2,TZF1_3,TZF1_4,TZF1_5,TZF1_6,TZF1_7,TZF1_8,TZF1_9,TZF1_10,B1,B2,B3,B4,B5,B6,B7,B8,B9,B10,S1,S2,S3,S4,S5,S6,S7,S8,S9,S10,O1,O2,O3,O4,O5,O6,O7,O8,O9,O10,E1,E2,E3,E4,E5,E6,E7,E8,E9,E10,P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,D1,D2,")
    fb.write("D3,D4,D5,T1,T2,T3,T4,T5,SUM3,SUM4,SUM5,SUM6,SUM7,SUM8,SUM9,SUM10,SUM11,SUM12,SUM13,SUM14,SUM15,SUM16,SUM17,SUM18,SUM19,SUMB,SUMS,SUMO,SUME,TSZF2_1-2,TSZF2_1-3,TSZF2_1-4,TSZF2_1-5,TSZF2_1-6,TSZF2_1-7,TSZF2_1-8,TSZF2_1-9,TSZF2_1-10,TSZF2_2-3,TSZF2_2-4,TSZF2_2-5,TSZF2_2-6,TSZF2_2-7,TSZF2_2-8,TSZF2_2-9,TSZF2_2-10,TSZF2_3-4,TSZF2_3-5,TSZF2_3-6,TSZF2_3-7,TSZF2_3-8,TSZF2_3-9,TSZF2_3-10,TSZF2_4-5,TSZF2_4-6,TSZF2_4-7,TSZF2_4-8,TSZF2_4-9,TSZF2_4-10,TSZF2_5-6,TSZF2_5-7,TSZF2_5-8,TSZF2_5-9,TSZF2_5-10,TSZF2_6-7,TSZF2_6-8,TSZF2_6-9,TSZF2_6-10,TSZF2_7-8,TSZF2_7-9,TSZF2_7-10,TSZF2_8-9,TSZF2_8-10,TSZF2_9-10,\n")
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
                row.append((odds[i] -1) * unitAmount )
                fb.write(str((odds[i] -1) * unitAmount) + ",")
                fo.write(str(odds[i] -1) + ",")
                i+=1
                total_bet_count += 1
                total_bet_amount += unitAmount
            else:
                row.append(0)
                fb.write("0,")
                fo.write("0,")
        #print(row)
        betOn_rows.append(row)
        fb.write("\n")
        fo.write("\n")

    fb.close()
    fo.close()
    #print(betOn_rows)
    wager_length = len(betOn_rows)
    print(f"total_bet_count={total_bet_count}, total_bet_amount={total_bet_amount}")
    
    # 計算每個beton投注總額
    #=========================================================
    column_length = len(header);
    A = np.ones(column_length).astype(np.float32)
    print("A=", A)

    max_wager_length = 20000
    for i in range(max_wager_length - len(betOn_rows)):
        betOn_rows.append(np.zeros(column_length))

    B = np.array(betOn_rows).flatten().astype(np.float32)
    #print("B=", B)
    print(f"selection_length={column_length}, wager_length={wager_length}, max_wager_length={max_wager_length}")
    total_amount_result = sum_selection_total_amount(A, B, max_wager_length)
    logging.debug(f"total_amount_result:{total_amount_result}")
    print(total_amount_result)
    #logging.debug("result length :", len(result))
    #logging.debug(sum(result))
    with  open('total_amount_result.csv', 'w+',  encoding='UTF-8') as f:
        f.write("DWD1_1,DWD1_2,DWD1_3,DWD1_4,DWD1_5,DWD1_6,DWD1_7,DWD1_8,DWD1_9,DWD1_10,DWD2_1,DWD2_2,DWD2_3,DWD2_4,DWD2_5,DWD2_6,DWD2_7,DWD2_8,DWD2_9,DWD2_10,DWD3_1,DWD3_2,DWD3_3,DWD3_4,DWD3_5,DWD3_6,DWD3_7,DWD3_8,DWD3_9,DWD3_10,DWD4_1,DWD4_2,DWD4_3,DWD4_4,DWD4_5,DWD4_6,DWD4_7,DWD4_8,DWD4_9,DWD4_10,DWD5_1,DWD5_2,DWD5_3,DWD5_4,DWD5_5,DWD5_6,DWD5_7,DWD5_8,DWD5_9,DWD5_10,DWD6_1,DWD6_2,DWD6_3,DWD6_4,DWD6_5,DWD6_6,DWD6_7,DWD6_8,DWD6_9,DWD6_10,DWD7_1,DWD7_2,DWD7_3,DWD7_4,DWD7_5,DWD7_6,DWD7_7,DWD7_8,DWD7_9,DWD7_10,DWD8_1,DWD8_2,DWD8_3,DWD8_4,DWD8_5,DWD8_6,DWD8_7,DWD8_8,DWD8_9,DWD8_10,DWD9_1,DWD9_2,DWD9_3,DWD9_4,DWD9_5,DWD9_6,DWD9_7,DWD9_8,DWD9_9,DWD9_10,DWD10_1,DWD10_2,DWD10_3,DWD10_4,DWD10_5,DWD10_6,DWD10_7,DWD10_8,DWD10_9,DWD10_10,TZF3_1-2-3,TZF3_1-2-4,TZF3_1-2-5,TZF3_1-2-6,TZF3_1-2-7,TZF3_1-2-8,TZF3_1-2-9,TZF3_1-2-10,TZF3_1-3-2,TZF3_1-3-4,TZF3_1-3-5,TZF3_1-3-6,TZF3_1-3-7,TZF3_1-3-8,TZF3_1-3-9,TZF3_1-3-10,TZF3_1-4-2,TZF3_1-4-3,TZF3_1-4-5,TZF3_1-4-6,TZF3_1-4-7,TZF3_1-4-8,TZF3_1-4-9,TZF3_1-4-10,TZF3_1-5-2,TZF3_1-5-3,TZF3_1-5-4,TZF3_1-5-6,TZF3_1-5-7,TZF3_1-5-8,TZF3_1-5-9,TZF3_1-5-10,TZF3_1-6-2,TZF3_1-6-3,TZF3_1-6-4,TZF3_1-6-5,TZF3_1-6-7,TZF3_1-6-8,TZF3_1-6-9,TZF3_1-6-10,TZF3_1-7-2,TZF3_1-7-3,TZF3_1-7-4,TZF3_1-7-5,TZF3_1-7-6,TZF3_1-7-8,TZF3_1-7-9,TZF3_1-7-10,TZF3_1-8-2,TZF3_1-8-3,TZF3_1-8-4,TZF3_1-8-5,TZF3_1-8-6,TZF3_1-8-7,TZF3_1-8-9,TZF3_1-8-10,TZF3_1-9-2,TZF3_1-9-3,TZF3_1-9-4,TZF3_1-9-5,TZF3_1-9-6,TZF3_1-9-7,TZF3_1-9-8,TZF3_1-9-10,TZF3_1-10-2,TZF3_1-10-3,TZF3_1-10-4,TZF3_1-10-5,TZF3_1-10-6,TZF3_1-10-7,TZF3_1-10-8,TZF3_1-10-9,TZF3_2-1-3,TZF3_2-1-4,TZF3_2-1-5,TZF3_2-1-6,TZF3_2-1-7,TZF3_2-1-8,TZF3_2-1-9,TZF3_2-1-10,TZF3_2-3-1,TZF3_2-3-4,TZF3_2-3-5,TZF3_2-3-6,TZF3_2-3-7,TZF3_2-3-8,TZF3_2-3-9,TZF3_2-3-10,TZF3_2-4-1,TZF3_2-4-3,TZF3_2-4-5,TZF3_2-4-6,TZF3_2-4-7,TZF3_2-4-8,TZF3_2-4-9,TZF3_2-4-10,TZF3_2-5-1,TZF3_2-5-3,TZF3_2-5-4,TZF3_2-5-6,TZF3_2-5-7,TZF3_2-5-8,TZF3_2-5-9,TZF3_2-5-10,TZF3_2-6-1,TZF3_2-6-3,TZF3_2-6-4,TZF3_2-6-5,TZF3_2-6-7,TZF3_2-6-8,TZF3_2-6-9,TZF3_2-6-10,TZF3_2-7-1,TZF3_2-7-3,TZF3_2-7-4,TZF3_2-7-5,TZF3_2-7-6,TZF3_2-7-8,TZF3_2-7-9,TZF3_2-7-10,TZF3_2-8-1,TZF3_2-8-3,TZF3_2-8-4,TZF3_2-8-5,TZF3_2-8-6,TZF3_2-8-7,TZF3_2-8-9,TZF3_2-8-10,TZF3_2-9-1,TZF3_2-9-3,TZF3_2-9-4,TZF3_2-9-5,TZF3_2-9-6,TZF3_2-9-7,TZF3_2-9-8,TZF3_2-9-10,TZF3_2-10-1,TZF3_2-10-3,TZF3_2-10-4,TZF3_2-10-5,TZF3_2-10-6,TZF3_2-10-7,TZF3_2-10-8,TZF3_2-10-9,TZF3_3-1-2,TZF3_3-1-4,TZF3_3-1-5,TZF3_3-1-6,TZF3_3-1-7,TZF3_3-1-8,TZF3_3-1-9,TZF3_3-1-10,TZF3_3-2-1,TZF3_3-2-4,TZF3_3-2-5,TZF3_3-2-6,TZF3_3-2-7,TZF3_3-2-8,TZF3_3-2-9,TZF3_3-2-10,TZF3_3-4-1,TZF3_3-4-2,TZF3_3-4-5,TZF3_3-4-6,TZF3_3-4-7,TZF3_3-4-8,TZF3_3-4-9,TZF3_3-4-10,TZF3_3-5-1,TZF3_3-5-2,TZF3_3-5-4,TZF3_3-5-6,TZF3_3-5-7,TZF3_3-5-8,TZF3_3-5-9,TZF3_3-5-10,TZF3_3-6-1,TZF3_3-6-2,TZF3_3-6-4,TZF3_3-6-5,TZF3_3-6-7,TZF3_3-6-8,TZF3_3-6-9,TZF3_3-6-10,TZF3_3-7-1,TZF3_3-7-2,TZF3_3-7-4,TZF3_3-7-5,TZF3_3-7-6,TZF3_3-7-8,TZF3_3-7-9,TZF3_3-7-10,TZF3_3-8-1,TZF3_3-8-2,TZF3_3-8-4,TZF3_3-8-5,TZF3_3-8-6,TZF3_3-8-7,TZF3_3-8-9,TZF3_3-8-10,TZF3_3-9-1,TZF3_3-9-2,TZF3_3-9-4,TZF3_3-9-5,TZF3_3-9-6,TZF3_3-9-7,TZF3_3-9-8,TZF3_3-9-10,TZF3_3-10-1,TZF3_3-10-2,TZF3_3-10-4,TZF3_3-10-5,TZF3_3-10-6,TZF3_3-10-7,TZF3_3-10-8,TZF3_3-10-9,TZF3_4-1-2,TZF3_4-1-3,TZF3_4-1-5,TZF3_4-1-6,TZF3_4-1-7,TZF3_4-1-8,TZF3_4-1-9,TZF3_4-1-10,TZF3_4-2-1,TZF3_4-2-3,TZF3_4-2-5,TZF3_4-2-6,TZF3_4-2-7,TZF3_4-2-8,TZF3_4-2-9,TZF3_4-2-10,TZF3_4-3-1,TZF3_4-3-2,TZF3_4-3-5,TZF3_4-3-6,TZF3_4-3-7,TZF3_4-3-8,TZF3_4-3-9,TZF3_4-3-10,TZF3_4-5-1,TZF3_4-5-2,TZF3_4-5-3,TZF3_4-5-6,TZF3_4-5-7,TZF3_4-5-8,TZF3_4-5-9,TZF3_4-5-10,TZF3_4-6-1,TZF3_4-6-2,TZF3_4-6-3,TZF3_4-6-5,TZF3_4-6-7,TZF3_4-6-8,TZF3_4-6-9,TZF3_4-6-10,TZF3_4-7-1,TZF3_4-7-2,TZF3_4-7-3,TZF3_4-7-5,TZF3_4-7-6,TZF3_4-7-8,TZF3_4-7-9,TZF3_4-7-10,TZF3_4-8-1,TZF3_4-8-2,TZF3_4-8-3,TZF3_4-8-5,TZF3_4-8-6,TZF3_4-8-7,TZF3_4-8-9,TZF3_4-8-10,TZF3_4-9-1,TZF3_4-9-2,TZF3_4-9-3,TZF3_4-9-5,TZF3_4-9-6,TZF3_4-9-7,TZF3_4-9-8,TZF3_4-9-10,TZF3_4-10-1,TZF3_4-10-2,TZF3_4-10-3,TZF3_4-10-5,TZF3_4-10-6,TZF3_4-10-7,TZF3_4-10-8,TZF3_4-10-9,TZF3_5-1-2,TZF3_5-1-3,TZF3_5-1-4,TZF3_5-1-6,TZF3_5-1-7,TZF3_5-1-8,TZF3_5-1-9,TZF3_5-1-10,TZF3_5-2-1,TZF3_5-2-3,TZF3_5-2-4,TZF3_5-2-6,TZF3_5-2-7,TZF3_5-2-8,TZF3_5-2-9,TZF3_5-2-10,TZF3_5-3-1,TZF3_5-3-2,TZF3_5-3-4,TZF3_5-3-6,TZF3_5-3-7,TZF3_5-3-8,TZF3_5-3-9,TZF3_5-3-10,TZF3_5-4-1,TZF3_5-4-2,TZF3_5-4-3,TZF3_5-4-6,TZF3_5-4-7,TZF3_5-4-8,TZF3_5-4-9,TZF3_5-4-10,TZF3_5-6-1,TZF3_5-6-2,TZF3_5-6-3,TZF3_5-6-4,TZF3_5-6-7,TZF3_5-6-8,TZF3_5-6-9,TZF3_5-6-10,TZF3_5-7-1,TZF3_5-7-2,TZF3_5-7-3,TZF3_5-7-4,TZF3_5-7-6,TZF3_5-7-8,TZF3_5-7-9,TZF3_5-7-10,TZF3_5-8-1,TZF3_5-8-2,TZF3_5-8-3,TZF3_5-8-4,TZF3_5-8-6,TZF3_5-8-7,TZF3_5-8-9,TZF3_5-8-10,TZF3_5-9-1,TZF3_5-9-2,TZF3_5-9-3,TZF3_5-9-4,TZF3_5-9-6,TZF3_5-9-7,TZF3_5-9-8,TZF3_5-9-10,TZF3_5-10-1,TZF3_5-10-2,TZF3_5-10-3,TZF3_5-10-4,TZF3_5-10-6,TZF3_5-10-7,TZF3_5-10-8,TZF3_5-10-9,TZF3_6-1-2,TZF3_6-1-3,TZF3_6-1-4,TZF3_6-1-5,TZF3_6-1-7,TZF3_6-1-8,TZF3_6-1-9,TZF3_6-1-10,TZF3_6-2-1,TZF3_6-2-3,TZF3_6-2-4,TZF3_6-2-5,TZF3_6-2-7,TZF3_6-2-8,TZF3_6-2-9,TZF3_6-2-10,TZF3_6-3-1,TZF3_6-3-2,TZF3_6-3-4,TZF3_6-3-5,TZF3_6-3-7,TZF3_6-3-8,TZF3_6-3-9,TZF3_6-3-10,TZF3_6-4-1,TZF3_6-4-2,TZF3_6-4-3,TZF3_6-4-5,TZF3_6-4-7,TZF3_6-4-8,TZF3_6-4-9,TZF3_6-4-10,TZF3_6-5-1,TZF3_6-5-2,TZF3_6-5-3,TZF3_6-5-4,TZF3_6-5-7,TZF3_6-5-8,TZF3_6-5-9,TZF3_6-5-10,TZF3_6-7-1,TZF3_6-7-2,TZF3_6-7-3,TZF3_6-7-4,TZF3_6-7-5,TZF3_6-7-8,TZF3_6-7-9,TZF3_6-7-10,TZF3_6-8-1,TZF3_6-8-2,TZF3_6-8-3,TZF3_6-8-4,TZF3_6-8-5,TZF3_6-8-7,TZF3_6-8-9,TZF3_6-8-10,TZF3_6-9-1,TZF3_6-9-2,TZF3_6-9-3,TZF3_6-9-4,TZF3_6-9-5,TZF3_6-9-7,TZF3_6-9-8,TZF3_6-9-10,TZF3_6-10-1,TZF3_6-10-2,TZF3_6-10-3,TZF3_6-10-4,TZF3_6-10-5,TZF3_6-10-7,TZF3_6-10-8,TZF3_6-10-9,TZF3_7-1-2,TZF3_7-1-3,TZF3_7-1-4,TZF3_7-1-5,TZF3_7-1-6,TZF3_7-1-8,TZF3_7-1-9,TZF3_7-1-10,TZF3_7-2-1,TZF3_7-2-3,TZF3_7-2-4,TZF3_7-2-5,TZF3_7-2-6,TZF3_7-2-8,TZF3_7-2-9,TZF3_7-2-10,TZF3_7-3-1,TZF3_7-3-2,TZF3_7-3-4,TZF3_7-3-5,TZF3_7-3-6,TZF3_7-3-8,TZF3_7-3-9,TZF3_7-3-10,TZF3_7-4-1,TZF3_7-4-2,TZF3_7-4-3,TZF3_7-4-5,TZF3_7-4-6,TZF3_7-4-8,TZF3_7-4-9,TZF3_7-4-10,TZF3_7-5-1,TZF3_7-5-2,TZF3_7-5-3,TZF3_7-5-4,TZF3_7-5-6,TZF3_7-5-8,TZF3_7-5-9,TZF3_7-5-10,TZF3_7-6-1,TZF3_7-6-2,TZF3_7-6-3,TZF3_7-6-4,TZF3_7-6-5,TZF3_7-6-8,TZF3_7-6-9,TZF3_7-6-10,TZF3_7-8-1,TZF3_7-8-2,TZF3_7-8-3,TZF3_7-8-4,TZF3_7-8-5,TZF3_7-8-6,TZF3_7-8-9,TZF3_7-8-10,TZF3_7-9-1,TZF3_7-9-2,TZF3_7-9-3,TZF3_7-9-4,TZF3_7-9-5,TZF3_7-9-6,TZF3_7-9-8,TZF3_7-9-10,TZF3_7-10-1,TZF3_7-10-2,TZF3_7-10-3,TZF3_7-10-4,TZF3_7-10-5,TZF3_7-10-6,TZF3_7-10-8,TZF3_7-10-9,TZF3_8-1-2,TZF3_8-1-3,TZF3_8-1-4,TZF3_8-1-5,TZF3_8-1-6,TZF3_8-1-7,TZF3_8-1-9,TZF3_8-1-10,TZF3_8-2-1,TZF3_8-2-3,TZF3_8-2-4,TZF3_8-2-5,TZF3_8-2-6,TZF3_8-2-7,TZF3_8-2-9,TZF3_8-2-10,TZF3_8-3-1,TZF3_8-3-2,TZF3_8-3-4,TZF3_8-3-5,TZF3_8-3-6,TZF3_8-3-7,TZF3_8-3-9,TZF3_8-3-10,TZF3_8-4-1,TZF3_8-4-2,TZF3_8-4-3,TZF3_8-4-5,TZF3_8-4-6,TZF3_8-4-7,TZF3_8-4-9,TZF3_8-4-10,TZF3_8-5-1,TZF3_8-5-2,TZF3_8-5-3,TZF3_8-5-4,TZF3_8-5-6,TZF3_8-5-7,TZF3_8-5-9,TZF3_8-5-10,TZF3_8-6-1,TZF3_8-6-2,TZF3_8-6-3,TZF3_8-6-4,TZF3_8-6-5,TZF3_8-6-7,TZF3_8-6-9,TZF3_8-6-10,TZF3_8-7-1,TZF3_8-7-2,TZF3_8-7-3,TZF3_8-7-4,TZF3_8-7-5,TZF3_8-7-6,TZF3_8-7-9,TZF3_8-7-10,TZF3_8-9-1,TZF3_8-9-2,TZF3_8-9-3,TZF3_8-9-4,TZF3_8-9-5,TZF3_8-9-6,TZF3_8-9-7,TZF3_8-9-10,TZF3_8-10-1,TZF3_8-10-2,TZF3_8-10-3,TZF3_8-10-4,TZF3_8-10-5,TZF3_8-10-6,TZF3_8-10-7,TZF3_8-10-9,TZF3_9-1-2,TZF3_9-1-3,TZF3_9-1-4,TZF3_9-1-5,TZF3_9-1-6,TZF3_9-1-7,TZF3_9-1-8,TZF3_9-1-10,TZF3_9-2-1,TZF3_9-2-3,TZF3_9-2-4,TZF3_9-2-5,TZF3_9-2-6,TZF3_9-2-7,TZF3_9-2-8,TZF3_9-2-10,TZF3_9-3-1,TZF3_9-3-2,TZF3_9-3-4,TZF3_9-3-5,TZF3_9-3-6,TZF3_9-3-7,TZF3_9-3-8,TZF3_9-3-10,TZF3_9-4-1,TZF3_9-4-2,TZF3_9-4-3,TZF3_9-4-5,TZF3_9-4-6,TZF3_9-4-7,TZF3_9-4-8,TZF3_9-4-10,TZF3_9-5-1,TZF3_9-5-2,TZF3_9-5-3,TZF3_9-5-4,TZF3_9-5-6,TZF3_9-5-7,TZF3_9-5-8,TZF3_9-5-10,TZF3_9-6-1,TZF3_9-6-2,TZF3_9-6-3,TZF3_9-6-4,TZF3_9-6-5,TZF3_9-6-7,TZF3_9-6-8,TZF3_9-6-10,TZF3_9-7-1,TZF3_9-7-2,TZF3_9-7-3,TZF3_9-7-4,TZF3_9-7-5,TZF3_9-7-6,TZF3_9-7-8,TZF3_9-7-10,TZF3_9-8-1,TZF3_9-8-2,TZF3_9-8-3,TZF3_9-8-4,TZF3_9-8-5,TZF3_9-8-6,TZF3_9-8-7,TZF3_9-8-10,TZF3_9-10-1,TZF3_9-10-2,TZF3_9-10-3,TZF3_9-10-4,TZF3_9-10-5,TZF3_9-10-6,TZF3_9-10-7,TZF3_9-10-8,TZF3_10-1-2,TZF3_10-1-3,TZF3_10-1-4,TZF3_10-1-5,TZF3_10-1-6,TZF3_10-1-7,TZF3_10-1-8,TZF3_10-1-9,TZF3_10-2-1,TZF3_10-2-3,TZF3_10-2-4,TZF3_10-2-5,TZF3_10-2-6,TZF3_10-2-7,TZF3_10-2-8,TZF3_10-2-9,TZF3_10-3-1,TZF3_10-3-2,TZF3_10-3-4,TZF3_10-3-5,TZF3_10-3-6,TZF3_10-3-7,TZF3_10-3-8,TZF3_10-3-9,TZF3_10-4-1,TZF3_10-4-2,TZF3_10-4-3,TZF3_10-4-5,TZF3_10-4-6,TZF3_10-4-7,TZF3_10-4-8,TZF3_10-4-9,TZF3_10-5-1,TZF3_10-5-2,TZF3_10-5-3,TZF3_10-5-4,TZF3_10-5-6,TZF3_10-5-7,TZF3_10-5-8,TZF3_10-5-9,TZF3_10-6-1,TZF3_10-6-2,TZF3_10-6-3,TZF3_10-6-4,TZF3_10-6-5,TZF3_10-6-7,TZF3_10-6-8,TZF3_10-6-9,TZF3_10-7-1,TZF3_10-7-2,TZF3_10-7-3,TZF3_10-7-4,TZF3_10-7-5,TZF3_10-7-6,TZF3_10-7-8,TZF3_10-7-9,TZF3_10-8-1,TZF3_10-8-2,TZF3_10-8-3,TZF3_10-8-4,TZF3_10-8-5,TZF3_10-8-6,TZF3_10-8-7,TZF3_10-8-9,TZF3_10-9-1,TZF3_10-9-2,TZF3_10-9-3,TZF3_10-9-4,TZF3_10-9-5,TZF3_10-9-6,TZF3_10-9-7,TZF3_10-9-8,TZF2_1-2,TZF2_1-3,TZF2_1-4,TZF2_1-5,TZF2_1-6,TZF2_1-7,TZF2_1-8,TZF2_1-9,TZF2_1-10,TZF2_2-1,TZF2_2-3,TZF2_2-4,TZF2_2-5,TZF2_2-6,TZF2_2-7,TZF2_2-8,TZF2_2-9,TZF2_2-10,TZF2_3-1,TZF2_3-2,TZF2_3-4,TZF2_3-5,TZF2_3-6,TZF2_3-7,TZF2_3-8,TZF2_3-9,TZF2_3-10,TZF2_4-1,TZF2_4-2,TZF2_4-3,TZF2_4-5,TZF2_4-6,TZF2_4-7,TZF2_4-8,TZF2_4-9,TZF2_4-10,TZF2_5-1,TZF2_5-2,TZF2_5-3,TZF2_5-4,TZF2_5-6,TZF2_5-7,TZF2_5-8,TZF2_5-9,TZF2_5-10,TZF2_6-1,TZF2_6-2,TZF2_6-3,TZF2_6-4,TZF2_6-5,TZF2_6-7,TZF2_6-8,TZF2_6-9,TZF2_6-10,TZF2_7-1,TZF2_7-2,TZF2_7-3,TZF2_7-4,TZF2_7-5,TZF2_7-6,TZF2_7-8,TZF2_7-9,TZF2_7-10,TZF2_8-1,TZF2_8-2,TZF2_8-3,TZF2_8-4,TZF2_8-5,TZF2_8-6,TZF2_8-7,TZF2_8-9,TZF2_8-10,TZF2_9-1,TZF2_9-2,TZF2_9-3,TZF2_9-4,TZF2_9-5,TZF2_9-6,TZF2_9-7,TZF2_9-8,TZF2_9-10,TZF2_10-1,TZF2_10-2,TZF2_10-3,TZF2_10-4,TZF2_10-5,TZF2_10-6,TZF2_10-7,TZF2_10-8,TZF2_10-9,TZF1_1,TZF1_2,TZF1_3,TZF1_4,TZF1_5,TZF1_6,TZF1_7,TZF1_8,TZF1_9,TZF1_10,B1,B2,B3,B4,B5,B6,B7,B8,B9,B10,S1,S2,S3,S4,S5,S6,S7,S8,S9,S10,O1,O2,O3,O4,O5,O6,O7,O8,O9,O10,E1,E2,E3,E4,E5,E6,E7,E8,E9,E10,P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,D1,D2,")
        f.write("D3,D4,D5,T1,T2,T3,T4,T5,SUM3,SUM4,SUM5,SUM6,SUM7,SUM8,SUM9,SUM10,SUM11,SUM12,SUM13,SUM14,SUM15,SUM16,SUM17,SUM18,SUM19,SUMB,SUMS,SUMO,SUME,TSZF2_1-2,TSZF2_1-3,TSZF2_1-4,TSZF2_1-5,TSZF2_1-6,TSZF2_1-7,TSZF2_1-8,TSZF2_1-9,TSZF2_1-10,TSZF2_2-3,TSZF2_2-4,TSZF2_2-5,TSZF2_2-6,TSZF2_2-7,TSZF2_2-8,TSZF2_2-9,TSZF2_2-10,TSZF2_3-4,TSZF2_3-5,TSZF2_3-6,TSZF2_3-7,TSZF2_3-8,TSZF2_3-9,TSZF2_3-10,TSZF2_4-5,TSZF2_4-6,TSZF2_4-7,TSZF2_4-8,TSZF2_4-9,TSZF2_4-10,TSZF2_5-6,TSZF2_5-7,TSZF2_5-8,TSZF2_5-9,TSZF2_5-10,TSZF2_6-7,TSZF2_6-8,TSZF2_6-9,TSZF2_6-10,TSZF2_7-8,TSZF2_7-9,TSZF2_7-10,TSZF2_8-9,TSZF2_8-10,TSZF2_9-10,\n")
        for t in total_amount_result:
            f.write(str(t)+",")
        f.write("\n")

    # 計算輸贏
    #=========================================================
    risk_result = calc_numbers_risk(total_amount_result)
    logging.debug(f"risk_result:{risk_result}")
    print(f"risk_result_length: { len(risk_result)}, numbers_length:{numbers_length}")
    
    response = { }
    response["code"] = 0
    response["msg"] = "success"
    rows = []
    print(f"risk_result[{numbers_length-1}]", risk_result[numbers_length-1])
    print(f"numbers[{numbers_length-1}]", numbers[numbers_length-1])

    with  open('opencode_answer.csv', 'w+',  encoding='UTF-8') as f:
        for i in range(numbers_length):
            f.write( str(numbers[i])+", "+ str(risk_result[i])+ "\n")
        """
        try:
            rows.append(
                {
                    "TotalAmountSum": risk_result[i],
                    "WinAmountSum": risk_result[i],
                    "BetCount" : 0,
                    "OpenCode": numbers[i]
                }
            )
        except :
            pass 
        """ 

if __name__ == "__main__":
    global header
    global program
    global context
    global numbers_answer
    global numbers_length
    global selection_length
    global numbers


    logging.debug("current path : " + os.path.abspath(__file__))
     # Create context and command queue
    platform = cl.get_platforms()[0]
    devices = platform.get_devices()
    context = cl.Context(devices)
    program = program_build()

    logging.info("load opencode table....")
    opencode_table = pd.read_csv('opencode_table.csv')
    header = opencode_table.columns[1:].tolist()
    logging.info(f"header count : {len(header)}")

    numbers = opencode_table["opencode"].tolist()
    print("numbers:", numbers)
    opencode_answer = opencode_table[opencode_table.columns[1:]]
    print("opencode_answer:", opencode_answer)
    numbers_length = opencode_answer.shape[0]
    print("numbers_length:", numbers_length)
    numbers_answer = np.array(opencode_answer).flatten().astype(np.float32)
    selection_length = str(len(header))
    logging.info(f"selection size={selection_length}, numbers={numbers_length}")

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
    
    submit()