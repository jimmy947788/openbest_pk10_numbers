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
import tools.TransferWager.A5 as A5

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

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

def submit():
    
    #print('request.form', request.data)
    betOn_rows = []
    #raw_data = request.get_data().decode("utf-8")
    with open(f"{currentPath}/data/test_wager_data.txt") as f:
        raw_data = f.read()
    logging.debug(f"row data: {raw_data}")
    
    (beton_amount_table, beton_amount_odds_table, total_bet_count, expectId, target_amount, tolerance, opencodeCount) = A5.transferWager(jdata)
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