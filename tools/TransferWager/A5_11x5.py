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
    for a in beton.split(",")[0].split(" "):
        for b in  beton.split(",")[1].split(" "):
            for c in  beton.split(",")[2].split(" "):
                if a != b and b!= c and c!= a:
                    result.append(f"O_ThreeStar_Zhi_Front3_X_{a}-{b}-{c}")
    return (result, len(result))

def OThreeStarZhiMiddle3X_Beton(beton = "1 2 3 4 5 6 7 8 9 10 11,1 2 3 4 5 6 7 8 9 10 11,1 2 3 4 5 6 7 8 9 10 11"):
    result = []
    for a in beton.split(",")[0].split(" "):
        for b in  beton.split(",")[1].split(" "):
            for c in  beton.split(",")[2].split(" "):
                if a != b and b!= c and c!= a:
                    result.append(f"O_ThreeStar_Zhi_Middle3_X_{a}-{b}-{c}")
    return (result, len(result))

def OThreeStarZhiLast3X_Beton(beton = "1 2 3 4 5 6 7 8 9 10 11,1 2 3 4 5 6 7 8 9 10 11,1 2 3 4 5 6 7 8 9 10 11"):
    result = []
    for a in beton.split(",")[0].split(" "):
        for b in  beton.split(",")[1].split(" "):
            for c in  beton.split(",")[2].split(" "):
                if a != b and b!= c and c!= a:
                    result.append(f"O_ThreeStar_Zhi_Last3_X_{a}-{b}-{c}")
    return (result, len(result))

def OThreeStarZuFront3X_Beton(beton = "1 2 3 4 5 6 7 8 9 10 11"):
    result = []
    for (a, b, c) in itertools.combinations(beton.split(' '), 3):
        result.append(f"O_ThreeStar_Zu_Front3_X_{a}-{b}-{c}")
    return (result, len(result))

def OThreeStarZuMiddle3X_Beton(beton = "1 2 3 4 5 6 7 8 9 10 11"):
    result = []
    for (a, b, c) in itertools.combinations(beton.split(' '), 3):
        result.append(f"O_ThreeStar_Zu_Middle3_X_{a}-{b}-{c}")
    return (result, len(result))

def OThreeStarZuLast3X_Beton(beton = "1 2 3 4 5 6 7 8 9 10 11"):
    result = []
    for (a, b, c) in itertools.combinations(beton.split(' '), 3):
        result.append(f"O_ThreeStar_Zu_Last3_X_{a}-{b}-{c}")
    return (result, len(result))

def OTwoStarZhi12_Beton(beton = "1 2 3 4 5 6 7 8 9 10 11,1 2 3 4 5 6 7 8 9 10 11"):
    result = []
    for a in beton.split(",")[0].split(" "):
        for b in  beton.split(",")[1].split(" "):
                if a != b:
                    result.append(f"O_TwoStar_Zhi_12_{a}-{b}")
    return (result, len(result))

def OTwoStarZu12_Beton(beton = "1 2 3 4 5 6 7 8 9 10 11"):
    result = []
    for (a, b) in itertools.combinations(beton.split(' '), 2):
        result.append(f"O_TwoStar_Zu_12_{a}-{b}")
    return (result, len(result))

def OTwoStarAny1_Beton(beton = "1 2 3 4 5 6 7 8 9 10 11"):
    result = []
    for a in beton.split(" "):
        result.append(f"O_TwoStar_Any_1_{a}")
    return (result, len(result))

def OTwoStarAny2_Beton(beton = "1 2 3 4 5 6 7 8 9 10 11"):
    result = []
    for (a, b) in itertools.combinations(beton.split(' '), 2):
        result.append(f"O_TwoStar_Any_2_{a}-{b}")
    return (result, len(result))

def OTwoStarAny3_Beton(beton = "1 2 3 4 5 6 7 8 9 10 11"):
    result = []
    for (a, b, c) in itertools.combinations(beton.split(' '), 3):
        result.append(f"O_TwoStar_Any_3_{a}-{b}-{c}")
    return (result, len(result))

def OTwoStarAny4_Beton(beton = "1 2 3 4 5 6 7 8 9 10 11"):
    result = []
    for (a, b, c, d) in itertools.combinations(beton.split(' '), 4):
        result.append(f"O_TwoStar_Any_4_{a}-{b}-{c}-{d}")
    return (result, len(result))

def OTwoStarAny5_Beton(beton = "1 2 3 4 5 6 7 8 9 10 11"):
    result = []
    for (a, b, c, d, e) in itertools.combinations(beton.split(' '), 5):
        result.append(f"O_TwoStar_Any_5_{a}-{b}-{c}-{d}-{e}")
    return (result, len(result))

def OTwoStarAny6_Beton(beton = "1 2 3 4 5 6 7 8 9 10 11"):
    result = []
    for (a, b, c, d, e, f) in itertools.combinations(beton.split(' '), 6):
        result.append(f"O_TwoStar_Any_6_{a}-{b}-{c}-{d}-{e}-{f}")
    return (result, len(result))

def OTwoStarAny7_Beton(beton = "1 2 3 4 5 6 7 8 9 10 11"):
    result = []
    for (a, b, c, d, e, f, g) in itertools.combinations(beton.split(' '), 7):
        result.append(f"O_TwoStar_Any_7_{a}-{b}-{c}-{d}-{e}-{f}-{g}")
    return (result, len(result))

def OTwoStarAny8_Beton(beton = "1 2 3 4 5 6 7 8 9 10 11"):
    result = []
    for (a, b, c, d, e, f, g, h) in itertools.combinations(beton.split(' '), 8):
        result.append(f"O_TwoStar_Any_8_{a}-{b}-{c}-{d}-{e}-{f}-{g}-{h}")
    return (result, len(result))

def ODingWeiDanX_Beton(beton = "1 2 3 4 5 6 7 8 9 10 11,1 2 3 4 5 6 7 8 9 10 11,1 2 3 4 5 6 7 8 9 10 11,1 2 3 4 5 6 7 8 9 10 11,1 2 3 4 5 6 7 8 9 10 11"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"O_DingWeiDan_X_a{a}")
    for b in  beton.split(",")[1].split(" "):
        result.append(f"O_DingWeiDan_X_b{b}")
    for c in  beton.split(",")[2].split(" "):
        result.append(f"O_DingWeiDan_X_c{c}")
    for d in  beton.split(",")[3].split(" "):
        result.append(f"O_DingWeiDan_X_d{d}")
    for e in  beton.split(",")[4].split(" "):
        result.append(f"O_DingWeiDan_X_e{e}")
    return (result, len(result))

def OBSOEX_Beton(beton = "B S O E,B S O E,B S O E,B S O E,B S O E"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"O_BSOE_X_a{a}")
    for b in  beton.split(",")[1].split(" "):
        result.append(f"O_BSOE_X_b{b}")
    for c in  beton.split(",")[2].split(" "):
        result.append(f"O_BSOE_X_c{c}")
    for d in  beton.split(",")[3].split(" "):
        result.append(f"O_BSOE_X_d{d}")
    for e in  beton.split(",")[4].split(" "):
        result.append(f"O_BSOE_X_e{e}")
    return (result, len(result))

def OSumBSOEX_Beton(beton="B S O E,TB TS"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"O_Sum_BSOE_X_{a}")
    for b in  beton.split(",")[1].split(" "):
        result.append(f"O_Sum_BSOE_X_{b}")
    return (result, len(result))

def X11X55_Beton(beton="01 02 03 04 05 06 07 08 09 10 11"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"X11X5_5_{a}")
    return (result, len(result))

def X11X54_Beton(beton="01 02 03 04 05 06 07 08 09 10 11"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"X11X5_4_{a}")
    return (result, len(result))

def X11X53_Beton(beton="01 02 03 04 05 06 07 08 09 10 11"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"X11X5_3_{a}")
    return (result, len(result))

def X11X52_Beton(beton="01 02 03 04 05 06 07 08 09 10 11"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"X11X5_2_{a}")
    return (result, len(result))

def X11X51_Beton(beton="01 02 03 04 05 06 07 08 09 10 11"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"X11X5_1_{a}")
    return (result, len(result))

def X11X51ON1_Beton(beton="01 02 03 04 05 06 07 08 09 10 11"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"X11X5_1ON1_{a}")
    return (result, len(result))

def X11X5SUMBS_Beton(beton="B S"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"X11X5_SUMBS_{a}")
    return (result, len(result))

def X11X5SUMOE_Beton(beton="O E"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"X11X5_SUMOE_{a}")
    return (result, len(result))

def X11X5TAILBS_Beton(beton="B S"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"X11X5_TAILBS_{a}")
    return (result, len(result))

def X11X5DT_Beton(beton="D T"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"X11X5_DT_{a}")
    return (result, len(result))

def X11X51BS_Beton(beton="B S"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"X11X5_1BS_{a}")
    return (result, len(result))

def X11X51OE_Beton(beton="O E"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"X11X5_1OE_{a}")
    return (result, len(result))

def X11X52BS_Beton(beton="B S"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"X11X5_2BS_{a}")
    return (result, len(result))

def X11X52OE_Beton(beton="O E"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"X11X5_2OE_{a}")
    return (result, len(result))

def X11X53BS_Beton(beton="B S"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"X11X5_3BS_{a}")
    return (result, len(result))

def X11X53OE_Beton(beton="O E"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"X11X5_3OE_{a}")
    return (result, len(result))

def X11X54BS_Beton(beton="B S"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"X11X5_4BS_{a}")
    return (result, len(result))

def X11X54OE_Beton(beton="O E"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"X11X5_4OE_{a}")
    return (result, len(result))

def X11X55BS_Beton(beton="B S"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"X11X5_5BS_{a}")
    return (result, len(result))

def X11X55OE_Beton(beton="O E"):
    result = []
    for a in beton.split(",")[0].split(" "):
        result.append(f"X11X5_5OE_{a}")
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
    elif betTypePlayCode == "O_ThreeStar_Zhi_Middle3_X":
        (betTypePlayCodeWithBetOnDic, length) = OThreeStarZhiMiddle3X_Beton(rawBetOn)
    elif betTypePlayCode == "O_ThreeStar_Zhi_Last3_X":
        (betTypePlayCodeWithBetOnDic, length) = OThreeStarZhiLast3X_Beton(rawBetOn)
    elif betTypePlayCode == "O_ThreeStar_Zu_Front3_X":
        (betTypePlayCodeWithBetOnDic, length) = OThreeStarZuFront3X_Beton(rawBetOn)
    elif betTypePlayCode == "O_ThreeStar_Zu_Middle3_X":
        (betTypePlayCodeWithBetOnDic, length) = OThreeStarZuMiddle3X_Beton(rawBetOn)
    elif betTypePlayCode == "O_ThreeStar_Zu_Last3_X":
        (betTypePlayCodeWithBetOnDic, length) = OThreeStarZuLast3X_Beton(rawBetOn)
    elif betTypePlayCode == "O_TwoStar_Zhi_12":
        (betTypePlayCodeWithBetOnDic, length) = OTwoStarZhi12_Beton(rawBetOn)
    elif betTypePlayCode == "O_TwoStar_Zu_12":
        (betTypePlayCodeWithBetOnDic, length) = OTwoStarZu12_Beton(rawBetOn)
    elif betTypePlayCode == "O_TwoStar_Any_1":
        (betTypePlayCodeWithBetOnDic, length) = OTwoStarAny1_Beton(rawBetOn)
    elif betTypePlayCode == "O_TwoStar_Any_2":
        (betTypePlayCodeWithBetOnDic, length) = OTwoStarAny2_Beton(rawBetOn)
    elif betTypePlayCode == "O_TwoStar_Any_3":
        (betTypePlayCodeWithBetOnDic, length) = OTwoStarAny3_Beton(rawBetOn)
    elif betTypePlayCode == "O_TwoStar_Any_4":
        (betTypePlayCodeWithBetOnDic, length) = OTwoStarAny4_Beton(rawBetOn)
    elif betTypePlayCode == "O_TwoStar_Any_5":
        (betTypePlayCodeWithBetOnDic, length) = OTwoStarAny5_Beton(rawBetOn)
    elif betTypePlayCode == "O_TwoStar_Any_6":
        (betTypePlayCodeWithBetOnDic, length) = OTwoStarAny6_Beton(rawBetOn)
    elif betTypePlayCode == "O_TwoStar_Any_7":
        (betTypePlayCodeWithBetOnDic, length) = OTwoStarAny7_Beton(rawBetOn)
    elif betTypePlayCode == "O_TwoStar_Any_8":
        (betTypePlayCodeWithBetOnDic, length) = OTwoStarAny8_Beton(rawBetOn)
    elif betTypePlayCode == "O_DingWeiDan_X":
        (betTypePlayCodeWithBetOnDic, length) = ODingWeiDanX_Beton(rawBetOn)
    elif betTypePlayCode == "O_BSOE_X":
        (betTypePlayCodeWithBetOnDic, length) = OBSOEX_Beton(rawBetOn)
    elif betTypePlayCode == "O_Sum_BSOE_X":
        (betTypePlayCodeWithBetOnDic, length) = OSumBSOEX_Beton(rawBetOn)
    elif betTypePlayCode == "X11X5_5":
        (betTypePlayCodeWithBetOnDic, length) = X11X55_Beton(rawBetOn)
    elif betTypePlayCode == "X11X5_4":
        (betTypePlayCodeWithBetOnDic, length) = X11X54_Beton(rawBetOn)
    elif betTypePlayCode == "X11X5_3":
        (betTypePlayCodeWithBetOnDic, length) = X11X53_Beton(rawBetOn)
    elif betTypePlayCode == "X11X5_2":
        (betTypePlayCodeWithBetOnDic, length) = X11X52_Beton(rawBetOn)
    elif betTypePlayCode == "X11X5_1":
        (betTypePlayCodeWithBetOnDic, length) = X11X51_Beton(rawBetOn)
    elif betTypePlayCode == "X11X5_1ON1":
        (betTypePlayCodeWithBetOnDic, length) = X11X51ON1_Beton(rawBetOn)
    elif betTypePlayCode == "X11X5_SUMBS":
        (betTypePlayCodeWithBetOnDic, length) = X11X5SUMBS_Beton(rawBetOn)
    elif betTypePlayCode == "X11X5_SUMOE":
        (betTypePlayCodeWithBetOnDic, length) = X11X5SUMOE_Beton(rawBetOn)
    elif betTypePlayCode == "X11X5_TAILBS":
        (betTypePlayCodeWithBetOnDic, length) = X11X5TAILBS_Beton(rawBetOn)
    elif betTypePlayCode == "X11X5_DT":
        (betTypePlayCodeWithBetOnDic, length) = X11X5DT_Beton(rawBetOn)
    elif betTypePlayCode == "X11X5_1BS":
        (betTypePlayCodeWithBetOnDic, length) = X11X51BS_Beton(rawBetOn)
    elif betTypePlayCode == "X11X5_1OE":
        (betTypePlayCodeWithBetOnDic, length) = X11X51OE_Beton(rawBetOn)
    elif betTypePlayCode == "X11X5_2BS":
        (betTypePlayCodeWithBetOnDic, length) = X11X52BS_Beton(rawBetOn)
    elif betTypePlayCode == "X11X5_2OE":
        (betTypePlayCodeWithBetOnDic, length) = X11X52OE_Beton(rawBetOn)
    elif betTypePlayCode == "X11X5_3BS":
        (betTypePlayCodeWithBetOnDic, length) = X11X53BS_Beton(rawBetOn)
    elif betTypePlayCode == "X11X5_3OE":
        (betTypePlayCodeWithBetOnDic, length) = X11X53OE_Beton(rawBetOn)
    elif betTypePlayCode == "X11X5_4BS":
        (betTypePlayCodeWithBetOnDic, length) = X11X54BS_Beton(rawBetOn)
    elif betTypePlayCode == "X11X5_4OE":
        (betTypePlayCodeWithBetOnDic, length) = X11X54OE_Beton(rawBetOn)
    elif betTypePlayCode == "X11X5_5BS":
        (betTypePlayCodeWithBetOnDic, length) = X11X55BS_Beton(rawBetOn)
    elif betTypePlayCode == "X11X5_5OE":
        (betTypePlayCodeWithBetOnDic, length) = X11X55OE_Beton(rawBetOn)


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