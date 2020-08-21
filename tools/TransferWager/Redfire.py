#!/usr/bin/python
 
import os
import sys
import json
import logging
import itertools

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
    
def transferWager(logging, headers, jdata):
    beton_amount_table = []
    beton_amount_odds_table = []
    total_bet_count = 0
    total_bet_amount = 0
    
    expectId = jdata["ExpectID"]
    opencodeCount = int(jdata["OpenCodeCount"])
    killRate =  float(jdata["KillRate"])
    tolerance = float(jdata["Tolerance"]) 
    lotteryCode = jdata["LotteryCode"]
    logging.debug(f"expectId={expectId}, opencodeCount={opencodeCount}, lotteryCode={lotteryCode}, killRate={killRate}, tolerance={tolerance}")

    for bet in jdata["Bets"]:
        betTypePlayCode = bet['BetTypePlayCode']
        unitAmount = bet["UnitAmount"]
        rawBetOn = bet["BetOn"]
        betOnCount  = bet["BetOnCount"]
        extraData = json.loads(bet["ExtraData"])
        odds = []
        betOn = []
        for i in range(betOnCount):
            if len(extraData["ExtraBets"]) == 1:
                odds.append(extraData["ExtraBets"][0]["Odds"])
            else:
                odds.append(extraData["ExtraBets"][i]["Odds"])

        # betTypePlayCode 轉換成解答表格式
        if betTypePlayCode == "PK10_A":
            betOn=["DWD1_" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_ABS" or betTypePlayCode == "PK10_ADRAGONTIGER" or  betTypePlayCode == "PK10_AOE" or betTypePlayCode == "PK10_APC":
            betOn=[rawBetOn + "1"]
        elif betTypePlayCode == "PK10_B":
            betOn=["DWD2_" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_BBS" or betTypePlayCode == "PK10_BDRAGONTIGER" or  betTypePlayCode == "PK10_BOE" or betTypePlayCode == "PK10_BPC":
            betOn=[rawBetOn + "2"]
        elif betTypePlayCode == "PK10_C":
            betOn=["DWD3_" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_CBS" or betTypePlayCode == "PK10_CDRAGONTIGER" or  betTypePlayCode == "PK10_COE" or betTypePlayCode == "PK10_CPC":
            betOn=[rawBetOn + "3"]
        elif betTypePlayCode == "PK10_D":
            betOn=["DWD4_" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_DBS" or betTypePlayCode == "PK10_DDRAGONTIGER" or  betTypePlayCode == "PK10_DOE" or betTypePlayCode == "PK10_DPC":
            betOn=[rawBetOn + "4"]
        elif betTypePlayCode == "PK10_E":
            betOn=["DWD5_" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_EBS" or betTypePlayCode == "PK10_EDRAGONTIGER" or  betTypePlayCode == "PK10_EOE" or betTypePlayCode == "PK10_EPC":
            betOn=[rawBetOn + "5"]
        elif betTypePlayCode == "PK10_F":
            betOn=["DWD6_" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_FBS" or  betTypePlayCode == "PK10_FOE" or betTypePlayCode == "PK10_FPC":
            betOn=[rawBetOn + "6"]
        elif betTypePlayCode == "PK10_G":
            betOn=["DWD7_" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_GBS" or  betTypePlayCode == "PK10_GOE" or betTypePlayCode == "PK10_GPC":
            betOn=[rawBetOn + "7"]
        elif betTypePlayCode == "PK10_H":
            betOn=["DWD8_" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_HBS" or  betTypePlayCode == "PK10_HOE" or betTypePlayCode == "PK10_HPC":
            betOn=[rawBetOn + "8"]
        elif betTypePlayCode == "PK10_I":
            betOn=["DWD9_" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_IBS" or  betTypePlayCode == "PK10_IOE" or betTypePlayCode == "PK10_IPC":
            betOn=[rawBetOn + "9"]
        elif betTypePlayCode == "PK10_J":
            betOn=["DWD10_" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_JBS" or  betTypePlayCode == "PK10_JOE" or betTypePlayCode == "PK10_JPC":
            betOn=[rawBetOn + "10"]
        elif "PK10_SUM" == betTypePlayCode:
            betOn=["SUM" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_SUMBS" or  betTypePlayCode == "PK10_SUMOE":
            betOn=["SUM" + rawBetOn + "11"]
        elif betTypePlayCode == "PK10_SUMBS11" or  betTypePlayCode == "PK10_SUMOE11":
            betOn=["SUM" + rawBetOn]

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

    target_amount = total_bet_amount * killRate #* -1
    logging.info(f"total_bet_count={total_bet_count}, total_bet_amount={total_bet_amount}")
    return (beton_amount_table, beton_amount_odds_table, total_bet_count, expectId, target_amount, tolerance, opencodeCount)