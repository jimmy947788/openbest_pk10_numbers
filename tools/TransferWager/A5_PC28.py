#!/usr/bin/python
 
from argparse import ArgumentError
import os
import sys
import json
import logging
import itertools
import time

# 轉換betOn格式
# =================================================
def OSumP_Beton(beton = "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27"):
    result = []
    for a in beton.split(" "):
        result.append(f"O_Sum_P_{a}")
    return (result, len(result))

def OSumBSOEP_Beton(beton = "B S O E"):
    result = []
    for a in beton.split(" "):
        result.append(f"O_Sum_BSOE_P_{a}")
    return (result, len(result))

def OSumSpecial_Beton(beton = "BO BE SO SE"):
    result = []
    for a in beton.split(" "):
        result.append(f"O_Sum_Special_{a}")
    return (result, len(result))

def OSpecial_Beton(beton = "LEOPARD CTN PAIR MAX MIN"):
    result = []
    for a in beton.split(" "):
        result.append(f"O_Special_{a}")
    return (result, len(result))

def ODragonTigerP_Beton(beton = "D T TT"):
    result = []
    for a in beton.split(" "):
        result.append(f"O_DragonTiger_P_{a}")
    return (result, len(result))

def OCOLORPC28_Beton(beton = "GREEN BLUE RED"):
    result = []
    for a in beton.split(" "):
        result.append(f"O_COLOR_PC28_{a}")
    return (result, len(result))

def PC28SUM00_Beton():
    result = []
    result.append(f"PC28_SUM_00")
    return (result, len(result))

def PC28SUM01_Beton():
    result = []
    result.append(f"PC28_SUM_01")
    return (result, len(result))

def PC28SUM02_Beton():
    result = []
    result.append(f"PC28_SUM_02")
    return (result, len(result))

def PC28SUM03_Beton():
    result = []
    result.append(f"PC28_SUM_03")
    return (result, len(result))

def PC28SUM04_Beton():
    result = []
    result.append(f"PC28_SUM_04")
    return (result, len(result))

def PC28SUM05_Beton():
    result = []
    result.append(f"PC28_SUM_05")
    return (result, len(result))

def PC28SUM06_Beton():
    result = []
    result.append(f"PC28_SUM_06")
    return (result, len(result))

def PC28SUM07_Beton():
    result = []
    result.append(f"PC28_SUM_07")
    return (result, len(result))

def PC28SUM08_Beton():
    result = []
    result.append(f"PC28_SUM_08")
    return (result, len(result))

def PC28SUM09_Beton():
    result = []
    result.append(f"PC28_SUM_09")
    return (result, len(result))

def PC28SUM10_Beton():
    result = []
    result.append(f"PC28_SUM_10")
    return (result, len(result))

def PC28SUM11_Beton():
    result = []
    result.append(f"PC28_SUM_11")
    return (result, len(result))

def PC28SUM12_Beton():
    result = []
    result.append(f"PC28_SUM_12")
    return (result, len(result))

def PC28SUM13_Beton():
    result = []
    result.append(f"PC28_SUM_13")
    return (result, len(result))

def PC28SUM14_Beton():
    result = []
    result.append(f"PC28_SUM_14")
    return (result, len(result))

def PC28SUM15_Beton():
    result = []
    result.append(f"PC28_SUM_15")
    return (result, len(result))

def PC28SUM16_Beton():
    result = []
    result.append(f"PC28_SUM_16")
    return (result, len(result))

def PC28SUM17_Beton():
    result = []
    result.append(f"PC28_SUM_17")
    return (result, len(result))

def PC28SUM18_Beton():
    result = []
    result.append(f"PC28_SUM_18")
    return (result, len(result))

def PC28SUM19_Beton():
    result = []
    result.append(f"PC28_SUM_19")
    return (result, len(result))

def PC28SUM20_Beton():
    result = []
    result.append(f"PC28_SUM_20")
    return (result, len(result))

def PC28SUM21_Beton():
    result = []
    result.append(f"PC28_SUM_21")
    return (result, len(result))

def PC28SUM22_Beton():
    result = []
    result.append(f"PC28_SUM_22")
    return (result, len(result))

def PC28SUM23_Beton():
    result = []
    result.append(f"PC28_SUM_23")
    return (result, len(result))

def PC28SUM24_Beton():
    result = []
    result.append(f"PC28_SUM_24")
    return (result, len(result))

def PC28SUM25_Beton():
    result = []
    result.append(f"PC28_SUM_25")
    return (result, len(result))

def PC28SUM26_Beton():
    result = []
    result.append(f"PC28_SUM_26")
    return (result, len(result))

def PC28SUM27_Beton():
    result = []
    result.append(f"PC28_SUM_27")
    return (result, len(result))

def transferWager(logging, jBets):
    
    betTypePlayCodeWithBetOnDic = []
    betTypePlayCode = jBets['BetTypePlayCode']
    unitAmount = jBets["UnitAmount"]
    rawBetOn = jBets["BetOn"]
    betOnCount  = int(jBets["BetOnCount"])
    extraData = json.loads(jBets["ExtraData"])
    length = 0

    if betTypePlayCode == "O_Sum_P":
        (betTypePlayCodeWithBetOnDic, length) = OSumP_Beton(rawBetOn)
   
    odds = []
    if len(extraData["ExtraBets"]) >1:
        for extraBet in extraData["ExtraBets"]:
            odd = str(extraBet["Odds"])
            odds.append(odd)
    else:
        for i in range(length):
            odd = str(extraData["ExtraBets"][0]["Odds"])
            odds.append(odd)

    return (betTypePlayCodeWithBetOnDic, odds, unitAmount, betOnCount)
    #$target_amount = total_bet_amount * killRate #* -1
    #logging.info(f"total_bet_count={total_bet_count}, total_bet_amount={total_bet_amount}")
    #return (result, total_bet_count, expectId, target_amount, tolerance, opencodeCount)