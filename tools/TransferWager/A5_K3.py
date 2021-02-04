import os
import sys
import json
import logging
import itertools
import time

# 轉換betOn格式
# =================================================
def OSumK_Beton(beton = "3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18"):
    result = []
    for a in beton.split(" "):
        result.append(f"O_Sum_K_{a}")
    return (result, len(result))

def OSumBSOEK_Beton(beton = "B S O E"):
    result = []
    for a in beton.split(" "):
        result.append(f"O_Sum_BSOE_K_{a}")
    return (result, len(result))

def OSame3B_Beton():
    result = []
    result.append(f"O_Same3B_SAME3B")
    return (result, len(result))

def OSame3A_Beton(beton="1 2 3 4 5 6"):
    result = []
    for a in beton.split(' '):
        result.append(f"O_Same3A_{a}")
    return (result, len(result))

def ODiff3_Beton(beton="1 2 3 4 5 6"):
    result = []
    for (a, b, c,) in  itertools.combinations(beton.split(' '), 3):
        if a !=b and b!=c and a!= c: 
            result.append(f"O_Diff3_{a}-{b}-{c}")
    return (result, len(result))

def OCtn3B_Beton():
    result = []
    result.append(f"O_Ctn3B_CTN3B")
    return (result, len(result))

def OSame2B_Beton(beton="1 2 3 4 5 6"):
    result = []
    for a in beton.split(' '):
        result.append(f"O_Same2B_{a}")
    return (result, len(result))

def OSame2A_Beton(beton="1 2 3 4 5 6,1 2 3 4 5 6"):
    result = []
    for a in beton.split(",")[0].split(" "):
        for b in  beton.split(",")[1].split(" "):
                if a != b:
                    result.append(f"O_Same2A_{a}-{b}")
    return (result, len(result))

def ODfif2_Beton(beton="1 2 3 4 5 6"):
    result = []
    for (a, b) in  itertools.combinations(beton.split(' '),  2):
        if a !=b: 
            result.append(f"O_Diff2_{a}-{b}")
    return (result, len(result))

def OKUADU_Beton(beton="1 2 3 4 5"):
    result = []
    for a in beton.split(' '):
        result.append(f"O_KUADU_{a}")
    return (result, len(result))

def OSIX_Beton(beton="HALF SIX"):
    result = []
    for a in beton.split(' '):
        result.append(f"O_SIX_{a}")
    return (result, len(result))

def O3_Beton(beton="1 2 3 4 5 6"):
    result = []
    for a in beton.split(' '):
        result.append(f"O_3_{a}")
    return (result, len(result))

def K3SUM03_Beton():
    result = []
    result.append(f"K3_SUM_03")
    return (result, len(result))

def K3SUM04_Beton():
    result = []
    result.append(f"K3_SUM_04")
    return (result, len(result))

def K3SUM05_Beton():
    result = []
    result.append(f"K3_SUM_05")
    return (result, len(result))

def K3SUM06_Beton():
    result = []
    result.append(f"K3_SUM_06")
    return (result, len(result))

def K3SUM07_Beton():
    result = []
    result.append(f"K3_SUM_07")
    return (result, len(result))

def K3SUM08_Beton():
    result = []
    result.append(f"K3_SUM_08")
    return (result, len(result))

def K3SUM09_Beton():
    result = []
    result.append(f"K3_SUM_09")
    return (result, len(result))

def K3SUM10_Beton():
    result = []
    result.append(f"K3_SUM_10")
    return (result, len(result))

def K3SUM11_Beton():
    result = []
    result.append(f"K3_SUM_11")
    return (result, len(result))

def K3SUM12_Beton():
    result = []
    result.append(f"K3_SUM_12")
    return (result, len(result))

def K3SUM13_Beton():
    result = []
    result.append(f"K3_SUM_13")
    return (result, len(result))

def K3SUM14_Beton():
    result = []
    result.append(f"K3_SUM_14")
    return (result, len(result))

def K3SUM15_Beton():
    result = []
    result.append(f"K3_SUM_15")
    return (result, len(result))

def K3SUM16_Beton():
    result = []
    result.append(f"K3_SUM_16")
    return (result, len(result))

def K3SUM17_Beton():
    result = []
    result.append(f"K3_SUM_17")
    return (result, len(result))

def K3SUM18_Beton():
    result = []
    result.append(f"K3_SUM_18")
    return (result, len(result))

def K3SUMBS_Beton(beton="B S"):
    result = []
    for a in beton.split(' '):
        result.append(f"K3_SUMBS_{a}")
    return (result, len(result))

def K3SUMOE_Beton(beton="O E"):
    result = []
    for a in beton.split(' '):
        result.append(f"K3_SUMOE_{a}")
    return (result, len(result))

def K3OBS_Beton(beton="OS OB"):
    result = []
    for a in beton.split(' '):
        result.append(f"K3_OBS_{a}")
    return (result, len(result))

def K3EBS_Beton(beton="ES EB"):
    result = []
    for a in beton.split(' '):
        result.append(f"K3_EBS_{a}")
    return (result, len(result))

def K3SAME3A_Beton(beton="111 222 333 444 555 666"):
    result = []
    for a in beton.split(' '):
        result.append(f"K3_SAME3A_{a}")
    return (result, len(result))

def K3SAME3B_Beton():
    result = []
    result.append(f"K3_SAME3B_111_666")
    return (result, len(result))

def K3CTN3A_Beton(beton="123 234 345 456"):
    result = []
    for a in beton.split(' '):
        result.append(f"K3_CTN3A_{a}")
    return (result, len(result))

def K3CTN3B_Beton():
    result = []
    result.append(f"K3_CTN3B_123_456")
    return (result, len(result))

def K3DIFF3_Beton(beton="123 124 125 126 134 135 136 145 146 156 234 235 236 245 246 256 345 346 356 456"):
    result = []
    for a in beton.split(' '):
        result.append(f"K3_DIFF3_{a}")
    return (result, len(result))

def K3SAME2A_Beton(beton="112 113 114 115 116 122 133 144 155 166 223 224 225 226 233 244 255 266 334 335 336 344 355 366 445 446 455 466 556 566"):
    result = []
    for a in beton.split(' '):
        result.append(f"K3_SAME2A_{a}")
    return (result, len(result))

def K3SAME2B_Beton(beton="11 22 33 44 55 66"):
    result = []
    for a in beton.split(' '):
        result.append(f"K3_SAME2B_{a}")
    return (result, len(result))

def K3DIFF2_Beton(beton="12 13 14 15 16 23 24 25 26 34 35 36 45 46 56"):
    result = []
    for a in beton.split(' '):
        result.append(f"K3_DIFF2_{a}")
    return (result, len(result))

def K33_Beton(beton="1 2 3 4 5 6"):
    result = []
    for a in beton.split(' '):
        result.append(f"K3_3_{a}")
    return (result, len(result))

def K3SIX_Beton(beton="HALF SIX"):
    result = []
    for a in beton.split(' '):
        result.append(f"K3_SIX_{a}")
    return (result, len(result))

def K3KUADU_Beton(beton="1 2 3 4 5"):
    result = []
    for a in beton.split(' '):
        result.append(f"K3_KUADU_{a}")
    return (result, len(result))

def K3BLACKOE_Beton(beton="B S O E"):
    result = []
    for a in beton.split(' '):
        result.append(f"K3_BLACKOE_{a}")
    return (result, len(result))

def K3REDOE_Beton(beton="O E"):
    result = []
    for a in beton.split(' '):
        result.append(f"K3_REDOE_{a}")
    return (result, len(result))

def K3REDBS_Beton(beton="B S"):
    result = []
    for a in beton.split(' '):
        result.append(f"K3_REDBS_{a}")
    return (result, len(result))

def K3BLACKRED_Beton(beton="RED BLACK"):
    result = []
    for a in beton.split(' '):
        result.append(f"K3_BLACKRED_{a}")
    return (result, len(result))

def transferWager(logging, jBets):
    
    betTypePlayCodeWithBetOnDic = []
    betTypePlayCode = jBets['BetTypePlayCode']
    unitAmount = jBets["UnitAmount"]
    rawBetOn = jBets["BetOn"]
    betOnCount  = int(jBets["BetOnCount"])
    extraData = json.loads(jBets["ExtraData"])
    length = 0

    if betTypePlayCode == "O_Sum_K":
        (betTypePlayCodeWithBetOnDic, length) = OSumK_Beton(rawBetOn)
    elif betTypePlayCode == "O_Same3B":
        (betTypePlayCodeWithBetOnDic, length) = OSame3B_Beton()
    elif betTypePlayCode == "O_Same3A":
        (betTypePlayCodeWithBetOnDic, length) = OSame3A_Beton(rawBetOn)
    elif betTypePlayCode == "O_Diff3":
        (betTypePlayCodeWithBetOnDic, length) = ODiff3_Beton(rawBetOn)
    elif betTypePlayCode == "O_Ctn3B":
        (betTypePlayCodeWithBetOnDic, length) = OCtn3B_Beton()
    elif betTypePlayCode == "O_Same2B":
        (betTypePlayCodeWithBetOnDic, length) = OSame2B_Beton(rawBetOn)
    elif betTypePlayCode == "O_Same2A":
        (betTypePlayCodeWithBetOnDic, length) = OSame2A_Beton(rawBetOn)
   
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