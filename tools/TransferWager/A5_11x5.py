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
def OThreeStarZhiFront3X_Beton(beton = "1 2 3 4 5 6 7 8 9 10 11,1 2 3 4 5 6 7 8 9 10 11,1 2 3 4 5 6 7 8 9 10 11"):
    result = []
    a = []
    for p in beton.split(","):
        a.append(p.split(" "))
    b = list(itertools.product(*a))
    for c in b:
        result.append("O_ThreeStar_Zhi_Front3_X_" + "".join(c))
    return (result, len(result))



def transferWager(logging, jBets):
    
    betTypePlayCodeWithBetOnDic = []
    betTypePlayCode = jBets['BetTypePlayCode']
    unitAmount = jBets["UnitAmount"]
    rawBetOn = jBets["BetOn"]
    betOnCount  = int(jBets["BetOnCount"])
    extraData = json.loads(jBets["ExtraData"])
    length = 0

    if betTypePlayCode == "O_ThreeStar_Zhi_Front3_X":
        (betTypePlayCodeWithBetOnDic, length) = OThreeStarZhiFront3X_Beton(rawBetOn)
  


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