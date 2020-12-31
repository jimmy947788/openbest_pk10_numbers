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
    a0 = beton.split(',')[0] #３重號
    a1 = beton.split(',')[1] # 2 位
    for a in a0.split(' '):
         for (b, c) in itertools.combinations(a1.split(' '), 2):
             if a != b and a != c:
                    result.append(f"O_FiveStar_Zu20_{a}{a}{a}{b}{c}")
    """
    for (a, b) in itertools.combinations(a0.split(' '), 2):
        for c in a1.split(' '):
            if c != a and c != b:
                result.append(f"O_FiveStar_Zu20_{c}{c}{c}{a}{b}")
    """
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

#信用
#=========================================
def SSC1_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_1_{a}")
    return (result, len(result))

def SSC2_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_2_{a}")
    return (result, len(result))

def SSC3_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_3_{a}")
    return (result, len(result))

def SSC4_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_4_{a}")
    return (result, len(result))

def SSC5_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_5_{a}")
    return (result, len(result))

def SSCD1T2_Beton(beton= "D T"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_D1T2_{a}")
    return (result, len(result))

def SSCD1T3_Beton(beton= "D T"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_D1T3_{a}")
    return (result, len(result))

def SSCD1T4_Beton(beton= "D T"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_D1T4_{a}")
    return (result, len(result))

def SSCD1T5_Beton(beton= "D T"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_D1T5_{a}")
    return (result, len(result))

def SSCD2T3_Beton(beton= "D T"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_D2T3_{a}")
    return (result, len(result))

def SSCD2T4_Beton(beton= "D T"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_D2T4_{a}")
    return (result, len(result))

def SSCD2T5_Beton(beton= "D T"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_D2T5_{a}")
    return (result, len(result))

def SSCD3T4_Beton(beton= "D T"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_D3T4_{a}")
    return (result, len(result))

def SSCD3T5_Beton(beton= "D T"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_D3T5_{a}")
    return (result, len(result))

def SSCD4T5_Beton(beton= "D T"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_D4T5_{a}")
    return (result, len(result))

def SSCTIE12_Beton():
    result = []
    result.append(f"SSC_TIE12_TT")
    return (result, len(result))

def SSCTIE13_Beton():
    result = []
    result.append(f"SSC_TIE13_TT")
    return (result, len(result))

def SSCTIE14_Beton():
    result = []
    result.append(f"SSC_TIE14_TT")
    return (result, len(result))

def SSCTIE15_Beton():
    result = []
    result.append(f"SSC_TIE15_TT")
    return (result, len(result))

def SSCTIE23_Beton():
    result = []
    result.append(f"SSC_TIE23_TT")
    return (result, len(result))

def SSCTIE24_Beton():
    result = []
    result.append(f"SSC_TIE24_TT")
    return (result, len(result))

def SSCTIE25_Beton():
    result = []
    result.append(f"SSC_TIE25_TT")
    return (result, len(result))

def SSCTIE34_Beton():
    result = []
    result.append(f"SSC_TIE34_TT")
    return (result, len(result))

def SSCTIE35_Beton():
    result = []
    result.append(f"SSC_TIE35_TT")
    return (result, len(result))

def SSCTIE45_Beton():
    result = []
    result.append(f"SSC_TIE45_TT")
    return (result, len(result))

def SSC1BS_Beton(beton= "B S"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_1BS_{a}")
    return (result, len(result))

def SSC2BS_Beton(beton= "B S"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_2BS_{a}")
    return (result, len(result))

def SSC3BS_Beton(beton= "B S"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_3BS_{a}")
    return (result, len(result))

def SSC4BS_Beton(beton= "B S"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_4BS_{a}")
    return (result, len(result))

def SSC5BS_Beton(beton= "B S"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_5BS_{a}")
    return (result, len(result))

def SSC1OE_Beton(beton= "O E"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_1OE_{a}")
    return (result, len(result))

def SSC2OE_Beton(beton= "O E"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_2OE_{a}")
    return (result, len(result))

def SSC3OE_Beton(beton= "O E"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_3OE_{a}")
    return (result, len(result))

def SSC4OE_Beton(beton= "O E"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_4OE_{a}")
    return (result, len(result))

def SSC5OE_Beton(beton= "O E"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_5OE_{a}")
    return (result, len(result))

def SSCF3CTN_Beton():
    result = []
    result.append(f"SSC_F3_CTN")
    return (result, len(result))

def SSCF3HALF_Beton():
    result = []
    result.append(f"SSC_F3_HALF")
    return (result, len(result))

def SSCF3LEOPARD_Beton():
    result = []
    result.append(f"SSC_F3_LEOPARD")
    return (result, len(result))

def SSCF3PAIR_Beton():
    result = []
    result.append(f"SSC_F3_PAIR")
    return (result, len(result))

def SSCF3SIX_Beton():
    result = []
    result.append(f"SSC_F3_SIX")
    return (result, len(result))

#
def SSCM3CTN_Beton():
    result = []
    result.append(f"SSC_M3_CTN")
    return (result, len(result))

def SSCM3HALF_Beton():
    result = []
    result.append(f"SSC_M3_HALF")
    return (result, len(result))

def SSCM3LEOPARD_Beton():
    result = []
    result.append(f"SSC_M3_LEOPARD")
    return (result, len(result))

def SSCM3PAIR_Beton():
    result = []
    result.append(f"SSC_M3_PAIR")
    return (result, len(result))

def SSCM3SIX_Beton():
    result = []
    result.append(f"SSC_M3_SIX")
    return (result, len(result))

#
def SSCL3CTN_Beton():
    result = []
    result.append(f"SSC_L3_CTN")
    return (result, len(result))

def SSCL3HALF_Beton():
    result = []
    result.append(f"SSC_L3_HALF")
    return (result, len(result))

def SSCL3LEOPARD_Beton():
    result = []
    result.append(f"SSC_L3_LEOPARD")
    return (result, len(result))

def SSCL3PAIR_Beton():
    result = []
    result.append(f"SSC_L3_PAIR")
    return (result, len(result))

def SSCL3SIX_Beton():
    result = []
    result.append(f"SSC_L3_SIX")
    return (result, len(result))

def SSCSINGLE_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_SINGLE_{a}")
    return (result, len(result))

def SSCPAIR_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_PAIR_{a}")
    return (result, len(result))

def SSCTHREE_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_THREE_{a}")
    return (result, len(result))

def SSCFOUR_Beton(beton= "0 1 2 3 4 5 6 7 8 9"):
    result = []
    for a in beton.split(' '):
        result.append(f"SSC_FOUR_{a}")
    return (result, len(result))

def transferWager(logging, jBets):
    
    betTypePlayCodeWithBetOnDic = []
    betTypePlayCode = jBets['BetTypePlayCode']
    unitAmount = jBets["UnitAmount"]
    rawBetOn = jBets["BetOn"]
    betOnCount  = int(jBets["BetOnCount"])
    extraData = json.loads(jBets["ExtraData"])
    length = 0

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
    elif betTypePlayCode == "SSC_1":
        (betTypePlayCodeWithBetOnDic, length) = SSC1_Beton(rawBetOn)
    elif betTypePlayCode == "SSC_2":
        (betTypePlayCodeWithBetOnDic, length) = SSC2_Beton(rawBetOn)
    elif betTypePlayCode == "SSC_3":
        (betTypePlayCodeWithBetOnDic, length) = SSC3_Beton(rawBetOn)
    elif betTypePlayCode == "SSC_4":
        (betTypePlayCodeWithBetOnDic, length) = SSC4_Beton(rawBetOn)
    elif betTypePlayCode == "SSC_5":
        (betTypePlayCodeWithBetOnDic, length) = SSC5_Beton(rawBetOn)
    elif betTypePlayCode == "SSC_D1T2":
        (betTypePlayCodeWithBetOnDic, length) = SSCD1T2_Beton(rawBetOn)
    elif betTypePlayCode == "SSC_D1T3":
        (betTypePlayCodeWithBetOnDic, length) = SSCD1T3_Beton(rawBetOn)
    elif betTypePlayCode == "SSC_D1T4":
        (betTypePlayCodeWithBetOnDic, length) = SSCD1T4_Beton(rawBetOn)
    elif betTypePlayCode == "SSC_D1T5":
        (betTypePlayCodeWithBetOnDic, length) = SSCD1T5_Beton(rawBetOn)
    elif betTypePlayCode == "SSC_D2T3":
        (betTypePlayCodeWithBetOnDic, length) = SSCD2T3_Beton(rawBetOn)
    elif betTypePlayCode == "SSC_D2T4":
        (betTypePlayCodeWithBetOnDic, length) = SSCD2T4_Beton(rawBetOn)    
    elif betTypePlayCode == "SSC_D2T5":
        (betTypePlayCodeWithBetOnDic, length) = SSCD2T5_Beton(rawBetOn)    
    elif betTypePlayCode == "SSC_D3T4":
        (betTypePlayCodeWithBetOnDic, length) = SSCD3T4_Beton(rawBetOn)    
    elif betTypePlayCode == "SSC_D3T5":
        (betTypePlayCodeWithBetOnDic, length) = SSCD3T5_Beton(rawBetOn)   
    elif betTypePlayCode == "SSC_D4T5":
        (betTypePlayCodeWithBetOnDic, length) = SSCD4T5_Beton(rawBetOn)     
    elif betTypePlayCode == "SSC_TIE12":
        (betTypePlayCodeWithBetOnDic, length) = SSCTIE12_Beton(rawBetOn)   
    elif betTypePlayCode == "SSC_TIE13":
        (betTypePlayCodeWithBetOnDic, length) = SSCTIE13_Beton(rawBetOn)     
    elif betTypePlayCode == "SSC_TIE14":
        (betTypePlayCodeWithBetOnDic, length) = SSCTIE14_Beton(rawBetOn)   
    elif betTypePlayCode == "SSC_TIE15":
        (betTypePlayCodeWithBetOnDic, length) = SSCTIE15_Beton(rawBetOn)   
    elif betTypePlayCode == "SSC_TIE23":
        (betTypePlayCodeWithBetOnDic, length) = SSCTIE23_Beton(rawBetOn)   
    elif betTypePlayCode == "SSC_TIE24":
        (betTypePlayCodeWithBetOnDic, length) = SSCTIE24_Beton(rawBetOn)   
    elif betTypePlayCode == "SSC_TIE25":
        (betTypePlayCodeWithBetOnDic, length) = SSCTIE25_Beton(rawBetOn)   
    elif betTypePlayCode == "SSC_TIE34":
        (betTypePlayCodeWithBetOnDic, length) = SSCTIE34_Beton(rawBetOn)   
    elif betTypePlayCode == "SSC_TIE35":
        (betTypePlayCodeWithBetOnDic, length) = SSCTIE35_Beton(rawBetOn)   
    elif betTypePlayCode == "SSC_TIE45":
        (betTypePlayCodeWithBetOnDic, length) = SSCTIE45_Beton(rawBetOn)   
    elif betTypePlayCode == "SSC_1BS":
        (betTypePlayCodeWithBetOnDic, length) = SSC1BS_Beton(rawBetOn)   
    elif betTypePlayCode == "SSC_2BS":
        (betTypePlayCodeWithBetOnDic, length) = SSC2BS_Beton(rawBetOn)   
    elif betTypePlayCode == "SSC_3BS":
        (betTypePlayCodeWithBetOnDic, length) = SSC3BS_Beton(rawBetOn)   
    elif betTypePlayCode == "SSC_4BS":
        (betTypePlayCodeWithBetOnDic, length) = SSC4BS_Beton(rawBetOn)   
    elif betTypePlayCode == "SSC_5BS":
        (betTypePlayCodeWithBetOnDic, length) = SSC5BS_Beton(rawBetOn)   
    elif betTypePlayCode == "SSC_1OE":
        (betTypePlayCodeWithBetOnDic, length) = SSC1OE_Beton(rawBetOn)   
    elif betTypePlayCode == "SSC_2OE":
        (betTypePlayCodeWithBetOnDic, length) = SSC2OE_Beton(rawBetOn)   
    elif betTypePlayCode == "SSC_3OE":
        (betTypePlayCodeWithBetOnDic, length) = SSC3OE_Beton(rawBetOn)   
    elif betTypePlayCode == "SSC_4OE":
        (betTypePlayCodeWithBetOnDic, length) = SSC4OE_Beton(rawBetOn)   
    elif betTypePlayCode == "SSC_5OE":
        (betTypePlayCodeWithBetOnDic, length) = SSC5OE_Beton(rawBetOn)   
    elif betTypePlayCode == "SSC_1OE":
        (betTypePlayCodeWithBetOnDic, length) = SSC1OE_Beton(rawBetOn)   

    elif betTypePlayCode == "SSC_F3_CTN":
        (betTypePlayCodeWithBetOnDic, length) = SSCF3CTN_Beton(rawBetOn)  
    elif betTypePlayCode == "SSC_F3_HALF":
        (betTypePlayCodeWithBetOnDic, length) = SSCF3HALF_Beton(rawBetOn)  
    elif betTypePlayCode == "SSC_F3_LEOPARD":
        (betTypePlayCodeWithBetOnDic, length) = SSCF3LEOPARD_Beton(rawBetOn)  
    elif betTypePlayCode == "SSC_F3_PAIR":
        (betTypePlayCodeWithBetOnDic, length) = SSCF3PAIR_Beton(rawBetOn)  
    elif betTypePlayCode == "SSC_F3_SIX":
        (betTypePlayCodeWithBetOnDic, length) = SSCF3PAIR_Beton(rawBetOn)  

    elif betTypePlayCode == "SSC_M3_CTN":
        (betTypePlayCodeWithBetOnDic, length) = SSCF3CTN_Beton(rawBetOn)  
    elif betTypePlayCode == "SSC_M3_HALF":
        (betTypePlayCodeWithBetOnDic, length) = SSCF3HALF_Beton(rawBetOn)  
    elif betTypePlayCode == "SSC_M3_LEOPARD":
        (betTypePlayCodeWithBetOnDic, length) = SSCF3LEOPARD_Beton(rawBetOn)  
    elif betTypePlayCode == "SSC_M3_PAIR":
        (betTypePlayCodeWithBetOnDic, length) = SSCF3PAIR_Beton(rawBetOn)  
    elif betTypePlayCode == "SSC_M3_SIX":
        (betTypePlayCodeWithBetOnDic, length) = SSCF3PAIR_Beton(rawBetOn)  
    
    elif betTypePlayCode == "SSC_L3_CTN":
            (betTypePlayCodeWithBetOnDic, length) = SSCF3CTN_Beton(rawBetOn)  
    elif betTypePlayCode == "SSC_L3_HALF":
        (betTypePlayCodeWithBetOnDic, length) = SSCF3HALF_Beton(rawBetOn)  
    elif betTypePlayCode == "SSC_L3_LEOPARD":
        (betTypePlayCodeWithBetOnDic, length) = SSCF3LEOPARD_Beton(rawBetOn)  
    elif betTypePlayCode == "SSC_L3_PAIR":
        (betTypePlayCodeWithBetOnDic, length) = SSCF3PAIR_Beton(rawBetOn)  
    elif betTypePlayCode == "SSC_L3_SIX":
        (betTypePlayCodeWithBetOnDic, length) = SSCF3PAIR_Beton(rawBetOn) 

    elif betTypePlayCode == "SSC_SINGLE":
        (betTypePlayCodeWithBetOnDic, length) = SSCSINGLE_Beton(rawBetOn) 
    elif betTypePlayCode == "SSC_PAIR":
        (betTypePlayCodeWithBetOnDic, length) = SSCPAIR_Beton(rawBetOn) 
    elif betTypePlayCode == "SSC_THREE":
        (betTypePlayCodeWithBetOnDic, length) = SSCTHREE_Beton(rawBetOn) 
    elif betTypePlayCode == "SSC_FOUR":
        (betTypePlayCodeWithBetOnDic, length) = SSCFOUR_Beton(rawBetOn) 


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