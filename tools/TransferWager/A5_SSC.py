#!/usr/bin/python
 
from argparse import ArgumentError
import os
import sys
import json
import logging
import itertools

# 轉換betOn格式
# =================================================
def OFiveStarZhiFu_Beton(beton = "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a = []
    for p in beton.split(","):
        a.append(p.split(" "))
    b = list(itertools.product(*a))
    for c in b:
        result.append("O_FiveStar_ZhiFu_" + "".join(c))
    return (result, len(result))

def OFiveStarZhiDan_Beton(beton):
    if beton == "":
        raise ArgumentError ("beton was not be null...")
    result = []
    for b in beton.split(","):
        result.append(f"O_FiveStar_ZhiFu_{b}")
    return (result, len(result))

def OFiveStarZu120_Beton(beton = "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for beton in itertools.combinations(beton.split(' '), 5):
        result.append("O_FiveStar_Zu120_" + "".join(beton))
    return (result, len(result))

def OFiveStarZu60_Beton(beton = "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a0 = beton.split(',')[0]
    a1 = beton.split(',')[1]
    for i in a0.split(' '):
        for (a, b, c) in itertools.combinations(a1.split(' '), 3):
            if i != a and i != b and i != c: 
                result.append(f"O_FiveStar_Zu60_{i}{i}{a}{b}{c}")
    return (result, len(result))

def OFiveStarZu30_Beton(beton = "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a0 = beton.split(',')[0]
    a1 = beton.split(',')[1]
    for (a, b) in itertools.combinations(a0.split(' '), 2):
        for c in a1.split(' '):
            w = [a,a,b,b]
            if c not in w:
                result.append(f"O_FiveStar_Zu30_{a}{a}{b}{b}{c}")
    return (result, len(result))

def OFiveStarZu20_Beton(beton = "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a0 = beton.split(',')[0]
    a1 = beton.split(',')[1]
    for (a, b) in itertools.combinations(a0.split(' '), 2):
        for c in a1.split(' '):
            if c != a and c != b:
                result.append(f"O_FiveStar_Zu20_{c}{c}{c}{a}{b}")
    return (result, len(result))

def OFiveStarZu10_Beton(beton = "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a0 = beton.split(',')[0]
    a1 = beton.split(',')[1]
    for a in a0.split(' '):
            for b in a1.split(' '):
                if a != b:
                    result.append(f"O_FiveStar_Zu10_{a}{a}{a}{b}{b}")
    return (result, len(result))

def OFiveStarZu5_Beton(beton = "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a0 = beton.split(',')[0]
    a1 = beton.split(',')[1]
    for a in a0.split(' '):
            for b in a1.split(' '):
                if a != b:
                    result.append(f"O_FiveStar_Zu5_{a}{a}{a}{a}{b}")
    return (result, len(result))
    
def OFiveStarSpecialOne_Beton(beton = "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for a in beton.split(' '):
        result.append(f"O_FiveStar_SpecialOne_{a}")
    return (result, len(result))

def OFiveStarSpecialTwo_Beton(beton = "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for a in beton.split(' '):
        result.append(f"O_FiveStar_SpecialTwo_{a}")
    return (result, len(result))

def OFiveStarSpecialThree_Beton(beton = "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for a in beton.split(' '):
        result.append(f"O_FiveStar_SpecialThree_{a}")
    return (result, len(result))

def OFiveStarSpecialFour_Beton(beton = "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for a in beton.split(' '):
        result.append(f"O_FiveStar_SpecialFour_{a}")
    return (result, len(result))

def OFourStarZhiFu_Beton(beton = "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a = []
    for p in beton.split(","):
        a.append(p.split(" "))
    b = list(itertools.product(*a))
    for c in b:
        result.append("O_FourStar_ZhiFu_" + "".join(c))
    return (result, len(result))

def OFourStarZhiDan_Beton(beton):
    if beton == "":
        raise ArgumentError ("beton was not be null...")
    result = []
    for b in beton.split(","):
        result.append(f"O_FourStar_ZhiFu_{b}")
    return (result, len(result))

def OFourStarZu24_Beton(beton = "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for beton in itertools.combinations(beton.split(' '), 4):
        result.append("O_FourStar_Zu24_" + "".join(beton))
    return (result, len(result))

def OFourStarZu12_Beton(beton= "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a0 = beton.split(',')[0]
    a1 = beton.split(',')[1]
    for i in a0.split(' '):
        for (a, b) in itertools.combinations(a1.split(' '), 2):
            if i != a and i != b: 
                result.append(f"O_FourStar_Zu12_{i}{i}{a}{b}")
    return (result, len(result))

def OFourStarZu6_Beton(beton = "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for (a, b) in itertools.combinations(beton.split(' '), 2):
            if a != b: 
                result.append(f"O_FourStar_Zu6_{a}{a}{b}{b}")
    return (result, len(result))

def OFourStarZu4_Beton(beton = "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a0 = beton.split(',')[0]
    a1 = beton.split(',')[1]
    for a in a0.split(' '):
        for b in a1.split(' '):
            if a != b: 
                result.append(f"O_FourStar_Zu4_{a}{a}{a}{b}")
    return (result, len(result))

def OThreeStarZhiFront3S_Beton(beton="0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a = []
    for p in beton.split(","):
        a.append(p.split(" "))
    b = list(itertools.product(*a))
    for c in b:
       result.append(f"O_ThreeStar_Zhi_Front3_S_" + "".join(c))
    return (result, len(result))

def OThreeStarZhiMiddle3S_Beton(beton = "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a = []
    for p in beton.split(","):
        a.append(p.split(" "))
    b = list(itertools.product(*a))
    for c in b:
       result.append(f"O_ThreeStar_Zhi_Middle3_S_" + "".join(c))
    return (result, len(result))

def OThreeStarZhiLast3S_Beton(beton = "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a = []
    for p in beton.split(","):
        a.append(p.split(" "))
    b = list(itertools.product(*a))
    for c in b:
       result.append(f"O_ThreeStar_Zhi_Last3_S_" + "".join(c))
    return (result, len(result))

def OThreeStarZuFront3S_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for c in itertools.combinations(beton.split(' '), 3):
        result.append(f"O_ThreeStar_Zu_Front3_S_" + "".join(c))
    return (result, len(result))

def OThreeStarZuMiddle3S_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for c in itertools.combinations(beton.split(' '), 3):
        result.append(f"O_ThreeStar_Zu_Middle3_S_" + "".join(c))
    return (result, len(result))


def OThreeStarZuLast3S_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for c in itertools.combinations(beton.split(' '), 3):
        result.append(f"O_ThreeStar_Zu_Last3_S_" + "".join(c))
    return (result, len(result))


def OThreeStarSpecialFront3_Beton(beton= "LEOPARD CTN PAIR HALF SIX"):
    result = []
    for c in beton.split(' '):
       result.append(f"O_ThreeStar_Special_Front3_{c}")
    return (result, len(result))

def OThreeStarSpecialMiddle3_Beton(beton = "LEOPARD CTN PAIR HALF SIX"):
    result = []
    for c in beton.split(' '):
       result.append(f"O_ThreeStar_Special_Middle3_{c}")
    return (result, len(result))

def OThreeStarSpecialLast3_Beton(beton = "LEOPARD CTN PAIR HALF SIX"):
    result = []
    for c in beton.split(' '):
       result.append(f"O_ThreeStar_Special_Last3_{c}")
    return (result, len(result))

def OTwoStarZhiWQ_Beton(beton = "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a = []
    for p in beton.split(","):
        a.append(p.split(" "))
    b = list(itertools.product(*a))
    for c in b:
        result.append("O_TwoStar_Zhi_wq_" + "".join(c))
    return (result, len(result))

def OTwoStarZhiWB_Beton(beton = "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a = []
    for p in beton.split(","):
        a.append(p.split(" "))
    b = list(itertools.product(*a))
    for c in b:
        result.append("O_TwoStar_Zhi_wb_" + "".join(c))
    return (result, len(result))

def OTwoStarZhiWS_Beton(beton = "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a = []
    for p in beton.split(","):
        a.append(p.split(" "))
    b = list(itertools.product(*a))
    for c in b:
        result.append("O_TwoStar_Zhi_ws_" + "".join(c))
    return (result, len(result))
    
def OTwoStarZhiWG_Beton(beton = "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a = []
    for p in beton.split(","):
        a.append(p.split(" "))
    b = list(itertools.product(*a))
    for c in b:
        result.append("O_TwoStar_Zhi_wg_" + "".join(c))
    return (result, len(result))

def OTwoStarZhiQB_Beton(beton= "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a = []
    for p in beton.split(","):
        a.append(p.split(" "))
    b = list(itertools.product(*a))
    for c in b:
        result.append("O_TwoStar_Zhi_qb_" + "".join(c))
    return (result, len(result))

def OTwoStarZhiQS_Beton(beton= "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a = []
    for p in beton.split(","):
        a.append(p.split(" "))
    b = list(itertools.product(*a))
    for c in b:
        result.append("O_TwoStar_Zhi_qs_" + "".join(c))
    return (result, len(result))

def OTwoStarZhiQG_Beton(beton= "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a = []
    for p in beton.split(","):
        a.append(p.split(" "))
    b = list(itertools.product(*a))
    for c in b:
        result.append("O_TwoStar_Zhi_qg_" + "".join(c))
    return (result, len(result))

def OTwoStarZhiBS_Beton(beton= "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a = []
    for p in beton.split(","):
        a.append(p.split(" "))
    b = list(itertools.product(*a))
    for c in b:
        result.append("O_TwoStar_Zhi_bs_" + "".join(c))
    return (result, len(result))

def OTwoStarZhiBG_Beton(beton= "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a = []
    for p in beton.split(","):
        a.append(p.split(" "))
    b = list(itertools.product(*a))
    for c in b:
        result.append("O_TwoStar_Zhi_bg_" + "".join(c))
    return (result, len(result))

def OTwoStarZhiSG_Beton(beton= "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a = []
    for p in beton.split(","):
        a.append(p.split(" "))
    b = list(itertools.product(*a))
    for c in b:
        result.append("O_TwoStar_Zhi_sg_" + "".join(c))
    return (result, len(result))

def OTwoStarZuWQ_Beton(beton = "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for (a, b) in itertools.combinations(beton.split(' '), 2):
        result.append(f"O_TwoStar_Zu_wq_{a}{b}")
    return (result, len(result))

def OTwoStarZuWB_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for (a, b) in itertools.combinations(beton.split(' '), 2):
        result.append(f"O_TwoStar_Zu_wb_{a}{b}")
    return (result, len(result))

def OTwoStarZuWS_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for (a, b) in itertools.combinations(beton.split(' '), 2):
        result.append(f"O_TwoStar_Zu_ws_{a}{b}")
    return (result, len(result))

def OTwoStarZuWG_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for (a, b) in itertools.combinations(beton.split(' '), 2):
        result.append(f"O_TwoStar_Zu_wg_{a}{b}")
    return (result, len(result))

def OTwoStarZuQB_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for (a, b) in itertools.combinations(beton.split(' '), 2):
        result.append(f"O_TwoStar_Zu_qb_{a}{b}")
    return (result, len(result))

def OTwoStarZuQS_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for (a, b) in itertools.combinations(beton.split(' '), 2):
        result.append(f"O_TwoStar_Zu_qs_{a}{b}")
    return (result, len(result))

def OTwoStarZuQG_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for (a, b) in itertools.combinations(beton.split(' '), 2):
        result.append(f"O_TwoStar_Zu_qg_{a}{b}")
    return (result, len(result))

def OTwoStarZuBS_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for (a, b) in itertools.combinations(beton.split(' '), 2):
        result.append(f"O_TwoStar_Zu_bs_{a}{b}")
    return (result, len(result))

def OTwoStarZuBG_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for (a, b) in itertools.combinations(beton.split(' '), 2):
        result.append(f"O_TwoStar_Zu_bg_{a}{b}")
    return (result, len(result))

def OTwoStarZuSG_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for (a, b) in itertools.combinations(beton.split(' '), 2):
        result.append(f"O_TwoStar_Zu_sg_{a}{b}")
    return (result, len(result))

def ODingWeiDanS_Beton(beton = "0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9,0 1 2 3 4 5 6 7 8 9"):
    result = []
    a0 = beton.split(',')[0]
    a1 = beton.split(',')[1]
    a2 = beton.split(',')[2]
    a3 = beton.split(',')[3]
    a4 = beton.split(',')[4]
    for c in a0.split(' '):
        if c:
            result.append(f"O_DingWeiDan_S_W{c}")
    for c in a1.split(' '):
        if c:
            result.append(f"O_DingWeiDan_S_Q{c}")
    for c in a2.split(' '):
        if c:
            result.append(f"O_DingWeiDan_S_B{c}")
    for c in a3.split(' '):
        if c:
            result.append(f"O_DingWeiDan_S_S{c}")
    for c in a4.split(' '):
        if c:
            result.append(f"O_DingWeiDan_S_G{c}")
    return (result, len(result))

def OBSOES_Beton(beton = "B S O E,B S O E,B S O E,B S O E,B S O E"):
    result = []
    a0 = beton.split(',')[0]
    a1 = beton.split(',')[1]
    a2 = beton.split(',')[2]
    a3 = beton.split(',')[3]
    a4 = beton.split(',')[4]
    for c in a0.split(' '):
        if c:
            result.append(f"O_BSOE_S_W{c}")
    for c in a1.split(' '):
        if c:
            result.append(f"O_BSOE_S_Q{c}")
    for c in a2.split(' '):
        if c:
            result.append(f"O_BSOE_S_B{c}")
    for c in a3.split(' '):
        if c:
            result.append(f"O_BSOE_S_S{c}")
    for c in a4.split(' '):
        if c:
            result.append(f"O_BSOE_S_G{c}")
    return (result, len(result))


def ODragonTigerWQ_Beton(beton = "D T TT"):
    result = []
    for c in beton.split(' '):
        result.append(f"O_DragonTiger_wq_{c}")
    return (result, len(result))

def ODragonTigerWB_Beton(beton = "D T TT"):
    result = []
    for c in beton.split(' '):
        result.append(f"O_DragonTiger_wb_{c}")
    return (result, len(result))

def ODragonTigerWS_Beton(beton = "D T TT"):
    result = []
    for c in beton.split(' '):
        result.append(f"O_DragonTiger_ws_{c}")
    return (result, len(result))

def ODragonTigerWG_Beton(beton = "D T TT"):
    result = []
    for c in beton.split(' '):
        result.append(f"O_DragonTiger_wg_{c}")
    return (result, len(result))

def ODragonTigerQB_Beton(beton = "D T TT"):
    result = []
    for c in beton.split(' '):
        result.append(f"O_DragonTiger_qb_{c}")
    return (result, len(result))

def ODragonTigerQS_Beton(beton= "D T TT"):
    result = []
    for c in beton.split(' '):
        result.append(f"O_DragonTiger_qs_{c}")
    return (result, len(result))

def ODragonTigerQG_Beton(beton= "D T TT"):
    result = []
    for c in beton.split(' '):
        result.append(f"O_DragonTiger_qg_{c}")
    return (result, len(result))

def ODragonTigerBS_Beton(beton= "D T TT"):
    result = []
    for c in beton.split(' '):
        result.append(f"O_DragonTiger_bs_{c}")
    return (result, len(result))

def ODragonTigerBG_Beton(beton= "D T TT"):
    result = []
    for c in beton.split(' '):
        result.append(f"O_DragonTiger_bg_{c}")
    return (result, len(result))

def ODragonTigerSG_Beton(beton= "D T TT"):
    result = []
    for c in beton.split(' '):
        result.append(f"O_DragonTiger_sg_{c}")
    return (result, len(result))

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
        betOnCount  = int(bet["BetOnCount"])
        extraData = json.loads(bet["ExtraData"])
        betOn = []
        odds = []
        for extraBet in extraData["ExtraBets"]:
            odd = float(extraBet["Odds"])
            odds.append(round(odd, 4))

        row_by_amount = []
        row_by_amount_odds = []
        betTypePlayCodeWithBetOnDic = []

        if betTypePlayCode == "O_FiveStar_ZhiFu":
            (betTypePlayCodeWithBetOnDic, length) = OFiveStarZhiFu_Beton(rawBetOn)
        elif betTypePlayCode == "O_FiveStar_ZhiDan":
           (betTypePlayCodeWithBetOnDic, length) = OFiveStarZhiDan_Beton(rawBetOn)
        elif betTypePlayCode == "O_FiveStar_Zu120":
            (betTypePlayCodeWithBetOnDic, length) = OFiveStarZu120_Beton(rawBetOn)
        elif betTypePlayCode == "O_FiveStar_Zu60":
            (betTypePlayCodeWithBetOnDic, length) = OFiveStarZu60_Beton(rawBetOn)
        elif betTypePlayCode == "O_FiveStar_Zu30":
            (betTypePlayCodeWithBetOnDic, length) = OFiveStarZu30_Beton(rawBetOn)
        elif betTypePlayCode == "O_FiveStar_Zu20":
            (betTypePlayCodeWithBetOnDic, length) = OFiveStarZu20_Beton(rawBetOn)
        elif betTypePlayCode == "O_FiveStar_Zu10":
            (betTypePlayCodeWithBetOnDic, length) = OFiveStarZu10_Beton(rawBetOn)
        elif betTypePlayCode == "O_FiveStar_Zu5":
            (betTypePlayCodeWithBetOnDic, length) = OFiveStarZu5_Beton(rawBetOn)
        elif betTypePlayCode == "O_FiveStar_SpecialOne":
            (betTypePlayCodeWithBetOnDic, length) = OFiveStarSpecialOne_Beton(rawBetOn)
        elif betTypePlayCode == "O_FiveStar_SpecialTwo":
            (betTypePlayCodeWithBetOnDic, length) = OFiveStarSpecialTwo_Beton(rawBetOn)
        elif betTypePlayCode == "O_FiveStar_SpecialThree":
            (betTypePlayCodeWithBetOnDic, length) = OFiveStarSpecialThree_Beton(rawBetOn)
        elif betTypePlayCode == "O_FiveStar_SpecialFour":
            (betTypePlayCodeWithBetOnDic, length) = OFiveStarSpecialFour_Beton(rawBetOn)
        elif betTypePlayCode == "O_FourStar_ZhiFu":
            (betTypePlayCodeWithBetOnDic, length) = OFourStarZhiFu_Beton(rawBetOn)
        elif betTypePlayCode == "O_FourStar_ZhiDan":
            (betTypePlayCodeWithBetOnDic, length) = OFourStarZhiDan_Beton(rawBetOn)
        elif betTypePlayCode == "O_FourStar_Zu24":
            (betTypePlayCodeWithBetOnDic, length) = OFourStarZu24_Beton(rawBetOn)
        elif betTypePlayCode == "O_FourStar_Zu12":
            (betTypePlayCodeWithBetOnDic, length) = OFourStarZu12_Beton(rawBetOn)
        elif betTypePlayCode == "O_FourStar_Zu6":
            (betTypePlayCodeWithBetOnDic, length) = OFourStarZu6_Beton(rawBetOn)
        elif betTypePlayCode == "O_FourStar_Zu4":
            (betTypePlayCodeWithBetOnDic, length) = OFourStarZu4_Beton(rawBetOn)
        elif betTypePlayCode == "O_ThreeStar_Zhi_Front3_S":
            (betTypePlayCodeWithBetOnDic, length) = OThreeStarZhiFront3S_Beton(rawBetOn)
        elif betTypePlayCode == "O_ThreeStar_Zhi_Middle3_S":
            (betTypePlayCodeWithBetOnDic, length) = OThreeStarZhiMiddle3S_Beton(rawBetOn)
        elif betTypePlayCode == "O_ThreeStar_Zhi_Last3_S":
            (betTypePlayCodeWithBetOnDic, length) = OThreeStarZhiLast3S_Beton(rawBetOn)
        elif betTypePlayCode == "O_ThreeStar_Zu_Front3_S":
            (betTypePlayCodeWithBetOnDic, length) = OThreeStarZuFront3S_Beton(rawBetOn)
        elif betTypePlayCode == "O_ThreeStar_Zu_Middle3_S":
            (betTypePlayCodeWithBetOnDic, length) = OThreeStarZuMiddle3S_Beton(rawBetOn)
        elif betTypePlayCode == "O_ThreeStar_Zu_Last3_S":
            (betTypePlayCodeWithBetOnDic, length) = OThreeStarZuLast3S_Beton(rawBetOn)
        elif betTypePlayCode == "O_ThreeStar_Special_Front3":
            (betTypePlayCodeWithBetOnDic, length) = OThreeStarSpecialFront3_Beton(rawBetOn)
        elif betTypePlayCode == "O_ThreeStar_Special_Middle3":
            (betTypePlayCodeWithBetOnDic, length) = OThreeStarSpecialMiddle3_Beton(rawBetOn)
        elif betTypePlayCode == "O_ThreeStar_Special_Last3":
            (betTypePlayCodeWithBetOnDic, length) = OThreeStarSpecialLast3_Beton(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zhi_wq":
            (betTypePlayCodeWithBetOnDic, length) = OTwoStarZhiWQ_Beton(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zhi_wb":
            (betTypePlayCodeWithBetOnDic, length) = OTwoStarZhiWB_Beton(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zhi_ws":
            (betTypePlayCodeWithBetOnDic, length) = OTwoStarZhiWS_Beton(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zhi_wg":
            (betTypePlayCodeWithBetOnDic, length) = OTwoStarZhiWG_Beton(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zhi_qb":
            (betTypePlayCodeWithBetOnDic, length) = OTwoStarZhiQB_Beton(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zhi_qs":
            (betTypePlayCodeWithBetOnDic, length) = OTwoStarZhiQS_Beton(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zhi_qg":
            (betTypePlayCodeWithBetOnDic, length) = OTwoStarZhiQG_Beton(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zhi_bs":
            (betTypePlayCodeWithBetOnDic, length) = OTwoStarZhiBS_Beton(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zhi_bg":
            (betTypePlayCodeWithBetOnDic, length) = OTwoStarZhiBG_Beton(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zhi_sg":
            (betTypePlayCodeWithBetOnDic, length) = OTwoStarZhiSG_Beton(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zu_wq":
            (betTypePlayCodeWithBetOnDic, length) = OTwoStarZuWQ_Beton(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zu_wb":
            (betTypePlayCodeWithBetOnDic, length) = OTwoStarZuWB_Beton(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zu_ws":
            (betTypePlayCodeWithBetOnDic, length) = OTwoStarZuWS_Beton(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zu_wg":
            (betTypePlayCodeWithBetOnDic, length) = OTwoStarZuWG_Beton(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zu_qb":
            (betTypePlayCodeWithBetOnDic, length) = OTwoStarZuQB_Beton(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zu_qs":
            (betTypePlayCodeWithBetOnDic, length) = OTwoStarZuQS_Beton(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zu_qg":
            (betTypePlayCodeWithBetOnDic, length) = OTwoStarZuQG_Beton(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zu_bs":
            (betTypePlayCodeWithBetOnDic, length) = OTwoStarZuBS_Beton(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zu_bg":
            (betTypePlayCodeWithBetOnDic, length) = OTwoStarZuBG_Beton(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zu_sg":
            (betTypePlayCodeWithBetOnDic, length) = OTwoStarZuSG_Beton(rawBetOn)
        elif betTypePlayCode == "O_DingWeiDan_S":
            (betTypePlayCodeWithBetOnDic, length) = ODingWeiDanS_Beton(rawBetOn)
        elif betTypePlayCode == "O_BSOE_S":
            (betTypePlayCodeWithBetOnDic, length) = OBSOES_Beton(rawBetOn)
        elif betTypePlayCode == "O_DragonTiger_wq":
            (betTypePlayCodeWithBetOnDic, length) = ODragonTigerWQ_Beton(rawBetOn)
        elif betTypePlayCode == "O_DragonTiger_wb":
            (betTypePlayCodeWithBetOnDic, length) = ODragonTigerWB_Beton(rawBetOn)
        elif betTypePlayCode == "O_DragonTiger_ws":
            (betTypePlayCodeWithBetOnDic, length) = ODragonTigerWS_Beton(rawBetOn)
        elif betTypePlayCode == "O_DragonTiger_wg":
            (betTypePlayCodeWithBetOnDic, length) = ODragonTigerWG_Beton(rawBetOn)
        elif betTypePlayCode == "O_DragonTiger_qb":
            (betTypePlayCodeWithBetOnDic, length) = ODragonTigerQB_Beton(rawBetOn)
        elif betTypePlayCode == "O_DragonTiger_qs":
            (betTypePlayCodeWithBetOnDic, length) = ODragonTigerQS_Beton(rawBetOn)
        elif betTypePlayCode == "O_DragonTiger_qg":
            (betTypePlayCodeWithBetOnDic, length) = ODragonTigerQG_Beton(rawBetOn)
        elif betTypePlayCode == "O_DragonTiger_bs":
            (betTypePlayCodeWithBetOnDic, length) = ODragonTigerBS_Beton(rawBetOn)
        elif betTypePlayCode == "O_DragonTiger_bg":
            (betTypePlayCodeWithBetOnDic, length) = ODragonTigerBG_Beton(rawBetOn)
        elif betTypePlayCode == "O_DragonTiger_sg":
            (betTypePlayCodeWithBetOnDic, length) = ODragonTigerSG_Beton(rawBetOn)

        odd_index = 0
        for header in  headers:
            if header in betTypePlayCodeWithBetOnDic:
                #print(f"header={header}, odds={odds}")
                row_by_amount.append(unitAmount) #本金
                if len(odds) > 1:
                    row_by_amount_odds.append((odds[odd_index]-1) * unitAmount) #此處賠率要扣掉1（本金）
                else:
                    row_by_amount_odds.append((odds[0]-1) * unitAmount) #此處賠率要扣掉1（本金）
                total_bet_count += 1
                total_bet_amount += unitAmount
                odd_index += 1
            else:
                row_by_amount.append(0)
                row_by_amount_odds.append(0)

        beton_amount_table.append(row_by_amount)
        beton_amount_odds_table.append(row_by_amount_odds)

    target_amount = total_bet_amount * killRate #* -1
    logging.info(f"total_bet_count={total_bet_count}, total_bet_amount={total_bet_amount}")
    return (beton_amount_table, beton_amount_odds_table, total_bet_count, expectId, target_amount, tolerance, opencodeCount)