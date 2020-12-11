import itertools
from logging import fatal
import pandas as pd
from argparse import ArgumentParser
import re
import os
from collections import Counter

def OFiveStarZhiFu_Beton():
    result = []
    for beton in itertools.product('0123456789', repeat = 5):
        result.append((beton[0], beton[1], beton[2], beton[3], beton[4]))
    return (result, len(result))

def OFiveStarZhiFu_Check(opencode, beton):
    return 1 if opencode == beton else -1

def OFiveStarZu120_Beton():
    result = []
    for beton in itertools.combinations('0123456789', 5):
        result.append( beton)
    return (result, len(result))

def OFiveStarZu120_Check(opencode, beton):
    counter = Counter(list(opencode))
    for (num, count) in counter.most_common():
        if count >=2:
            return -1
    ret = 0
    if  opencode[0] in beton:
        ret += 1
    if opencode[1] in beton:
        ret += 1
    if opencode[2] in beton:
        ret += 1
    if opencode[3] in beton:
        ret += 1
    if opencode[4] in beton:
        ret += 1
    return 1 if ret == 5 else -1

def OFiveStarZu60_Beton():
    result = []
    for i in ["00", "11", "22", "33", "44", "55", "66", "77", "88", "99"]:
        for (a, b, c) in itertools.combinations('0123456789', 3):
            if i[0] != a and i[0] != b and i[0] != c: 
                result.append( (i[0],i[1],a,b,c))
    return (result, len(result))

def OFiveStarZu60_Check(opencode, beton):
    d = beton[0]
    s = [beton[2], beton[3], beton[4]]
    d_counter = 0
    s0_counter = 0
    s1_counter = 0
    s2_counter = 0
    for num in opencode:
        if d == num:
            d_counter += 1
        if  s[0] == num:
            s0_counter += 1
        if  s[1] == num:
            s1_counter += 1
        if  s[2] == num:
            s2_counter += 1
    if d_counter == 2 and s0_counter==1 and s1_counter == 1 and s2_counter == 1:
        return 1
    else:
        return -1

def OFiveStarZu30_Beton():
    result = []
    for (a, b) in itertools.combinations('0123456789', 2):
            for c in [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                w = [a,a,b,b]
                if c not in w:
                    result.append( (w[0], w[1], w[2], w[3], c))
    return (result, len(result))


def OFiveStarZu30_Check(opencode, beton):
    d1 = beton[0]
    d2 = beton[2]
    s = beton[4]
    d1_counter = 0
    d2_counter = 0
    s_counter = 0
    for num in opencode:
        if d1 == num:
            d1_counter += 1
        if d2 == num:
            d2_counter += 1
        if  s == num:
            s_counter += 1
    if d1_counter == 2 and d2_counter ==2 and s_counter == 1:
        return 1
    else:
        return -1

def OFiveStarZu20_Beton():
    result = []
    for (a, b) in itertools.combinations('0123456789', 2):
            for c in [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                if c != a and c != b:
                    result.append( (c, c, c, a, b))
    return (result, len(result))

def OFiveStarZu20_Check(opencode, beton):
    t = beton[0]
    s1 = beton[3]
    s2 = beton[4]
    t_counter = 0
    s1_counter = 0
    s2_counter = 0
    for num in opencode:
        if t == num:
            t_counter += 1
        if  s1 == num:
            s1_counter += 1
        if  s2 == num:
            s2_counter += 1
    if t_counter == 3 and s1_counter == 1 and s2_counter == 1:
        return 1
    else:
        return -1

def OFiveStarZu10_Beton():
    result = []
    for a in [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            for b in [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                if a != b:
                    result.append( (a, a, a, b, b))
    return (result, len(result))

def OFiveStarZu10_Check(opencode, beton):
    t = beton[0] #triple
    d = beton[3]
    t_counter = 0
    d_counter = 0
    for num in opencode:
        if t == num:
            t_counter += 1
        if  d == num:
            d_counter += 1
    if t_counter == 3 and d_counter == 2:
        return 1
    else:
        return -1

def OFiveStarZu5_Beton():
    result = []
    for a in [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            for b in [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                if a != b:
                    result.append( (a, a, a, a, b))
    return (result, len(result))

def OFiveStarZu5_Check(opencode, beton):
    q = beton[0] #quadruple
    s = beton[4]
    q_counter = 0
    s_counter = 0
    for num in opencode:
        if q == num:
            q_counter += 1
        if  s == num:
            s_counter += 1
    if q_counter == 4 and s_counter == 1:
        return 1
    else:
        return -1
    
def OFiveStarSpecialOne_Beton():
    return ([ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 10)

def OFiveStarSpecialOne_Check(opencode, beton):
    s = beton
    s_counter = 0
    for num in opencode:
        if s == num:
            s_counter += 1
    
    if s_counter == 1:
            return 1
    else:
        return -1    

def OFiveStarSpecialTwo_Beton():
    return ([ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 10)

def OFiveStarSpecialTwo_Check(opencode, beton):
    s = beton
    s_counter = 0
    for num in opencode:
        if s == num:
            s_counter += 1
    
    if s_counter == 2:
            return 1
    else:
        return -1    

def OFiveStarSpecialTwo_Beton():
    return ([ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 10)

def OFiveStarSpecialTwo_Check(opencode, beton):
    s = beton
    s_counter = 0
    for num in opencode:
        if s == num:
            s_counter += 1
    
    if s_counter == 2:
        return 1
    else:
        return -1    

def OFiveStarSpecialThree_Beton():
    return ([ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 10)

def OFiveStarSpecialThree_Check(opencode, beton):
    s = beton
    s_counter = 0
    for num in opencode:
        if s == num:
            s_counter += 1
    
    if s_counter == 3:
            return 1
    else:
        return -1  

def OFiveStarSpecialFour_Beton():
    return ([ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 10)

def OFiveStarSpecialFour_Check(opencode, beton):
    s = beton
    s_counter = 0
    for num in opencode:
        if s == num:
            s_counter += 1
    
    if s_counter == 4:
            return 1
    else:
        return -1  

def OFourStarZhiFu_Beton():
    result = []
    for beton in itertools.product('0123456789', repeat = 4):
        result.append((beton[0], beton[1], beton[2], beton[3]))
    return (result, len(result))

def OFourStarZhiFu_Check(opencode, beton):
    if  opencode[1] == beton[0] and opencode[2] == beton[1] and opencode[3] == beton[2] and opencode[4] == beton[3]:
        return 1
    else:
        return -1 

def OFourStarZu24_Beton():
    result = []
    for beton in itertools.combinations('0123456789', 4):
        result.append( beton)
    return (result, len(result))

def OFourStarZu24_Check(opencode, beton):
    s = beton
    s0_counter = 0
    s1_counter = 0
    s2_counter = 0
    s3_counter = 0
    for num in opencode[1:]:
        if int(s[0]) == int(num):
            s0_counter += 1
        if int(s[1]) == int(num):
            s1_counter += 1
        if int(s[2]) == int(num):
            s2_counter += 1
        if int(s[3]) == int(num):
            s3_counter += 1

    if s0_counter==1 and s1_counter == 1 and s2_counter == 1 and s3_counter == 1:
        return 1
    else:
        return -1

def OFourStarZu12_Beton():
    result = []
    for i in ["00", "11", "22", "33", "44", "55", "66", "77", "88", "99"]:
        for (a, b) in itertools.combinations('0123456789', 2):
            if i[0] != a and i[0] != b: 
                result.append( (i[0],i[1],a,b))
    return (result, len(result))

def OFourStarZu12_Check(opencode, beton):
    d = beton[0]
    s = [beton[2], beton[3]]
    d_counter = 0
    s0_counter = 0
    s1_counter = 0
    for num in opencode[1:]:
        if d == num:
            d_counter += 1
        if  s[0] == num:
            s0_counter += 1
        if  s[1] == num:
            s1_counter += 1
    if d_counter == 2 and s0_counter==1 and s1_counter == 1:
        return 1
    else:
        return -1

def OFourStarZu6_Beton():
    result = []
    for i in ["00", "11", "22", "33", "44", "55", "66", "77", "88", "99"]:
        for j in ["00", "11", "22", "33", "44", "55", "66", "77", "88", "99"]:
            if i[0] != j[0]: 
                result.append( (i[0],i[1],j[0],j[1]))
    return (result, len(result))

def OFourStarZu6_Check(opencode, beton):
    d0 = beton[0]
    d1 = beton[2]
    d0_counter = 0
    d1_counter = 0
    for num in opencode[1:]:
        if d0 == num:
            d0_counter += 1
        if d1 == num:
            d1_counter += 1
    if d0_counter == 2 and d1_counter==2:
        return 1
    else:
        return -1

def OFourStarZu4_Beton():
    result = []
    for a in [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        for b in [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            if a != b: 
                result.append((a,a,a,b))
    return (result, len(result))

def OFourStarZu4_Check(opencode, beton):
    w = beton[0]
    s = beton[3]
    w_counter = 0
    s_counter = 0
    for num in opencode[1:]:
        if w == num:
            w_counter += 1
        if s == num:
            s_counter += 1
    if w_counter == 3 and s_counter==1:
        return 1
    else:
        return -1

def OThreeStarZhiFront3S_Beton():
    result = []
    for beton in itertools.product('0123456789', repeat = 3):
        result.append((beton[0], beton[1], beton[2]))
    return (result, len(result))

def OThreeStarZhiFront3S_Check(opencode, beton):
    if  opencode[0] == beton[0] and opencode[1] == beton[1] and opencode[2] == beton[2]:
        return 1
    else:
        return -1 

def OThreeStarZhiMiddle3S_Beton():
    result = []
    for beton in itertools.product('0123456789', repeat = 3):
        result.append((beton[0], beton[1], beton[2]))
    return (result, len(result))

def OThreeStarZhiMiddle3S_Check(opencode, beton):
    if  opencode[1] == beton[0] and opencode[2] == beton[1] and opencode[3] == beton[2]:
        return 1
    else:
        return -1 

def OThreeStarZhiLast3S_Beton():
    result = []
    for beton in itertools.product('0123456789', repeat = 3):
        result.append((beton[0], beton[1], beton[2]))
    return (result, len(result))

def OThreeStarZhiLast3S_Check(opencode, beton):
    if  opencode[2] == beton[0] and opencode[3] == beton[1] and opencode[4] == beton[2]:
        return 1
    else:
        return -1 

def OThreeStarZuFront3S_Beton():
    result = []
    for beton in itertools.product('0123456789', repeat = 3):
        result.append((beton[0], beton[1], beton[2]))
    return (result, len(result))

def OThreeStarZuFront3S_Check(opencode, beton):
    s0 = beton[0]
    s1 = beton[1]
    s2 = beton[2]
    s0_counter = 0
    s1_counter = 0
    s2_counter = 0
    for num in opencode[:3]: # 前三
        if s0 == num:
            s0_counter += 1
        if s1 == num:
            s1_counter += 1
        if s2 == num:
            s2_counter += 1
    if s0_counter == 1 and s1_counter == 1 and s2_counter == 1:
        return 1
    else:
        return -1

def OThreeStarZuMiddle3S_Beton():
    result = []
    for beton in itertools.product('0123456789', repeat = 3):
        result.append((beton[0], beton[1], beton[2]))
    return (result, len(result))

def OThreeStarZuMiddle3S_Check(opencode, beton):
    s0 = beton[0]
    s1 = beton[1]
    s2 = beton[2]
    s0_counter = 0
    s1_counter = 0
    s2_counter = 0
    for num in (opencode[1],opencode[2],opencode[3]): # 中三
        if s0 == num:
            s0_counter += 1
        if s1 == num:
            s1_counter += 1
        if s2 == num:
            s2_counter += 1
    if s0_counter == 1 and s1_counter == 1 and s2_counter == 1:
        return 1
    else:
        return -1

def OThreeStarZuLast3S_Beton():
    result = []
    for beton in itertools.product('0123456789', repeat = 3):
        result.append((beton[0], beton[1], beton[2]))
    return (result, len(result))

def OThreeStarZuLast3S_Check(opencode, beton):
    s0 = beton[0]
    s1 = beton[1]
    s2 = beton[2]
    s0_counter = 0
    s1_counter = 0
    s2_counter = 0
    for num in (opencode[2:]): # 後三
        if s0 == num:
            s0_counter += 1
        if s1 == num:
            s1_counter += 1
        if s2 == num:
            s2_counter += 1
    if s0_counter == 1 and s1_counter == 1 and s2_counter == 1:
        return 1
    else:
        return -1

def OThreeStarSpecial3_Beton():
    result = { 
        "LEOPARD" : [],
        "CTN" : [],
        "PAIR" : [],
        "HALF" : [],
        "SIX" : [] 
    }
    for (a, b, c) in itertools.product([0,1,2,3,4,5,6,7,8,9], repeat=3):
        if a == b and b == c:
            result["LEOPARD"].append((a, b, c)) # LEOPARD
        elif (a - b ==1 and b - c ==1) or (a - c ==1 and c - b ==1) or ( b - c == 1 and c - a ==1) or  ( b - a == 1 and a - c ==1) or ( c - a == 1 and a - b ==1) or  ( c - b == 1 and b - a ==1):
            result["CTN"].append((a, b, c)) # CTN
        elif (a == b) or (b==c) or (a==c):
            result["PAIR"].append((a, b, c)) # PAIR
        elif (a - b == 1) or (a - c ==1 ) or (b-a ==1 ) or (b - c == 1) or (c - a ==1) or (c - b ==1):
            result["HALF"].append((a, b, c)) # HALF
        else:
            result["SIX"].append((a, b, c)) # SIX
    return (result, len(result))

def OThreeStarSpecialFront3_Check(opencode, beton):
    (a, b, c) = (int(opencode[0]), int(opencode[1]), int(opencode[2]))
    if (a, b, c) in beton:
        return 1
    else:
        return -1

def OThreeStarSpecialMiddle3_Check(opencode, beton):
    (a, b, c) = (int(opencode[1]), int(opencode[2]), int(opencode[3]))
    if (a, b, c) in beton:
        return 1
    else:
        return -1

def OThreeStarSpecialLast3_Check(opencode, beton):
    (a, b, c) = (int(opencode[2]), int(opencode[3]), int(opencode[4]))
    if (a, b, c) in beton:
        return 1
    else:
        return -1

def OTwoStarZhi_Beton():
    result = []
    for (a, b) in itertools.product([0,1,2,3,4,5,6,7,8,9], repeat=2):
        result.append((a, b))
    return (result, len(result))

def OTwoStarZhiWQ_Check(opencode, beton):
    (a, b) = (int(opencode[0]), int(opencode[1]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZhiWB_Check(opencode, beton):
    (a, b) = (int(opencode[0]), int(opencode[2]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZhiWS_Check(opencode, beton):
    (a, b) = (int(opencode[0]), int(opencode[3]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZhiWG_Check(opencode, beton):
    (a, b) = (int(opencode[0]), int(opencode[4]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZhiQB_Check(opencode, beton):
    (a, b) = (int(opencode[1]), int(opencode[2]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZhiQS_Check(opencode, beton):
    (a, b) = (int(opencode[1]), int(opencode[3]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZhiQG_Check(opencode, beton):
    (a, b) = (int(opencode[1]), int(opencode[4]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZhiBS_Check(opencode, beton):
    (a, b) = (int(opencode[2]), int(opencode[3]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZhiBG_Check(opencode, beton):
    (a, b) = (int(opencode[2]), int(opencode[4]))
    if (a, b) == beton:
        return 1
    else:
        return -1
    
def OTwoStarZhiSG_Check(opencode, beton):
    (a, b) = (int(opencode[3]), int(opencode[4]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZu_Beton():
    result = []
    for (a, b) in itertools.combinations([0,1,2,3,4,5,6,7,8,9], 2):
        result.append((a, b))
    return (result, len(result))

def OTwoStarZuWQ_Check(opencode, beton):
    (a, b) = (int(opencode[0]), int(opencode[1]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZuWB_Check(opencode, beton):
    (a, b) = (int(opencode[0]), int(opencode[2]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZuWS_Check(opencode, beton):
    (a, b) = (int(opencode[0]), int(opencode[3]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZuWG_Check(opencode, beton):
    (a, b) = (int(opencode[0]), int(opencode[4]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZuQB_Check(opencode, beton):
    (a, b) = (int(opencode[1]), int(opencode[2]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZuQS_Check(opencode, beton):
    (a, b) = (int(opencode[1]), int(opencode[3]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZuQG_Check(opencode, beton):
    (a, b) = (int(opencode[1]), int(opencode[4]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZuBS_Check(opencode, beton):
    (a, b) = (int(opencode[2]), int(opencode[3]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZuBG_Check(opencode, beton):
    (a, b) = (int(opencode[2]), int(opencode[4]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZuSG_Check(opencode, beton):
    (a, b) = (int(opencode[3]), int(opencode[4]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def ODingWeiDanS_Beton():
    result = []
    for p in [ "W", "Q", "B", "S", "G" ]:
        for num in [0,1,2,3,4,5,6,7,8,9]:
            result.append(f"{p}{num}")
    return (result, len(result))

def ODingWeiDanS_Check(opencode, beton):
    pos = beton[0]
    num = beton[1]
    if pos == "W" and opencode[0] == num:
        return 1
    elif pos == "Q" and opencode[1] == num:
        return 1
    elif pos == "B" and opencode[2] == num:
        return 1
    elif pos == "S" and opencode[3] == num:
        return 1
    elif pos == "G" and opencode[4] == num:
        return 1
    else:
        return -1

def OBSOES_Beton():
    result = []
    for p in [ "W", "Q", "B", "S", "G" ]:
        for b in [ "O", "B", "S", "E" ]:
            result.append(f"{p}{b}")
    return (result, len(result))

def OBSOES_Check(opencode, beton):
    map = { 
        "W" : 0, 
        "Q" : 1,
        "B" : 2,
        "S" : 3,
        "G" : 4,
    }
    pos = map[beton[0]]
    num = int(opencode[pos])
    if beton[1] == "O" :
        return 1 if  (num % 2) != 0  else -1
    elif beton[1] == "B" :
        return 1 if num >= 5  else -1
    elif beton[1] == "S" :
        return 1 if num <= 4  else -1
    elif beton[1] == "E" :
        return 1 if  (num % 2) == 0  else -1

enableOFiveStarZhiFu = False
def main():
    parser = ArgumentParser()
    parser.add_argument("--header", help="optional argument", dest="header", default=False)
    parser.add_argument("--opencode", help="optional argument", dest="opencode", default=None)
    args = parser.parse_args()
    hasHeader = bool(args.header)
    print("header arg:", hasHeader)
    print("opencode arg:", args.opencode)

    currentPath = os.path.dirname(os.path.abspath(__file__))
    currentPath = currentPath.replace("/tools", "")

    # b百 s拾 q千 w萬 g個
    with open(f'{currentPath}/data/opencode_table_ssc.csv', 'w+', encoding='UTF-8') as f:
        # header
        #====================================================================================
        header = "opencode,"
        """
        # O_FiveStar_ZhiFu 五星直選
        if enableOFiveStarZhiFu:
            (result, length ) = OFiveStarZhiFu_Beton()
            for beton in result:
                header += f"O_FiveStar_ZhiFu_{beton[0]}{beton[1]}{beton[2]}{beton[3]}{beton[4]},"

        # O_FiveStar_Zu120 五星組選120
        (result, length )= OFiveStarZu120_Beton()
        for beton in result:
            header += f"O_FiveStar_Zu120_{beton[0]}{beton[1]}{beton[2]}{beton[3]}{beton[4]},"

        # O_FiveStar_Zu60 五星組選60
        (result, length) = OFiveStarZu60_Beton()
        for beton in result:
            header += f"O_FiveStar_Zu60_{beton[0]}{beton[1]}{beton[2]}{beton[3]}{beton[4]},"

        # O_FiveStar_Zu30 五星組選30
        (result, length) = OFiveStarZu30_Beton()
        for beton in result:
            header += f"O_FiveStar_Zu30_{beton[0]}{beton[1]}{beton[2]}{beton[3]}{beton[4]},"

        # O_FiveStar_Zu20 五星組選20
        (result, length) = OFiveStarZu20_Beton()
        for beton in result:
            header += f"O_FiveStar_Zu20_{beton[0]}{beton[1]}{beton[2]}{beton[3]}{beton[4]},"

         # O_FiveStar_Zu10 五星組選10
        (result, length) = OFiveStarZu10_Beton()
        for beton in result:
            header += f"O_FiveStar_Zu10_{beton[0]}{beton[1]}{beton[2]}{beton[3]}{beton[4]},"

        # O_FiveStar_Zu5 五星組選5
        (result, length) = OFiveStarZu5_Beton()
        for beton in result:
            header += f"O_FiveStar_Zu5_{beton[0]}{beton[1]}{beton[2]}{beton[3]}{beton[4]},"

        # O_FiveStar_SpecialOne 一帆风顺
        (result, length) = OFiveStarSpecialOne_Beton()
        for beton in result:
            header += f"O_FiveStar_SpecialOne_{beton},"
        
        # O_FiveStar_SpecialTwo 好事成雙
        (result, length) = OFiveStarSpecialTwo_Beton()
        for beton in result:
            header += f"O_FiveStar_SpecialTwo_{beton},"
        
        # O_FiveStar_SpecialTwo 三星報喜
        (result, length) = OFiveStarSpecialThree_Beton()
        for beton in result:
            header += f"O_FiveStar_SpecialThree_{beton},"

        # O_FiveStar_SpecialTwo 四季發財
        (result, length) = OFiveStarSpecialFour_Beton()
        for beton in result:
            header += f"O_FiveStar_SpecialFour_{beton},"

        # O_FourStar_ZhiFu 四星直選
        (result, length) = OFourStarZhiFu_Beton()
        for beton in result:
            header += f"O_FourStar_ZhiFu_{beton[0]}{beton[1]}{beton[2]}{beton[3]},"

        # O_FourStar_Zu24 四星組選24
        (result, length) = OFourStarZu24_Beton()
        for beton in result:
            header += f"O_FourStar_Zu24_{beton[0]}{beton[1]}{beton[2]}{beton[3]},"

        # O_FourStar_Zu12 四星組選12
        (result, length) = OFourStarZu12_Beton()
        for beton in result:
            header += f"O_FourStar_Zu12_{beton[0]}{beton[1]}{beton[2]}{beton[3]},"

        # O_FourStar_Zu6 四星組選6
        (result, length) = OFourStarZu6_Beton()
        for beton in result:
            header += f"O_FourStar_Zu6_{beton[0]}{beton[1]}{beton[2]}{beton[3]},"

        # O_FourStar_Zu4 四星組選4
        (result, length) = OFourStarZu4_Beton()
        for beton in result:
            header += f"O_FourStar_Zu4_{beton[0]}{beton[1]}{beton[2]}{beton[3]},"

        # O_ThreeStar_Zhi_Front3_S  三位直選前三
        (result, length) = OThreeStarZhiFront3S_Beton()
        for beton in result:
            header += f"O_ThreeStar_Zhi_Front3_S_{beton[0]}{beton[1]}{beton[2]},"

        # O_ThreeStar_Zhi_Front3_S  三位直選中三
        (result, length) = OThreeStarZhiMiddle3S_Beton()
        for beton in result:
            header += f"O_ThreeStar_Zhi_Middle3_S_{beton[0]}{beton[1]}{beton[2]},"

        # O_ThreeStar_Zhi_Last3_S  三位直選後三
        (result, length) = OThreeStarZhiLast3S_Beton()
        for beton in result:
            header += f"O_ThreeStar_Zhi_Last3_S_{beton[0]}{beton[1]}{beton[2]},"

        # O_ThreeStar_Zu_Front3_S  三位組選前三
        (result, length) = OThreeStarZuFront3S_Beton()
        for beton in result:
            header += f"O_ThreeStar_Zu_Front3_S_{beton[0]}{beton[1]}{beton[2]},"

        # O_ThreeStar_Zu_Middle3_S  三位組選前三
        (result, length) = OThreeStarZuMiddle3S_Beton()
        for beton in result:
            header += f"O_ThreeStar_Zu_Middle3_S_{beton[0]}{beton[1]}{beton[2]},"

        # O_ThreeStar_Zu_Last3_S  三位組選後三
        (result, length) = OThreeStarZuLast3S_Beton()
        for beton in result:
            header += f"O_ThreeStar_Zu_Last3_S_{beton[0]}{beton[1]}{beton[2]},"
        """

        # O_ThreeStar_Special_Front3 三位特殊號前三
        (result, length) =  OThreeStarSpecial3_Beton()
        for beton in result.keys():
            header += f"O_ThreeStar_Special_Front3_{beton},"
        
        # O_ThreeStar_Special_Middle3 三位特殊號中三
        (result, length) =  OThreeStarSpecial3_Beton()
        for beton in result.keys():
            header += f"O_ThreeStar_Special_Middle3_{beton},"
        
        # O_ThreeStar_Special_Last3 三位特殊號後三
        (result, length) =  OThreeStarSpecial3_Beton()
        for beton in result.keys():
            header += f"O_ThreeStar_Special_Last3_{beton},"

        # O_TwoStar_Zhi_wq 二位直選萬千
        (result, length) =  OTwoStarZhi_Beton()
        for beton in result:
            header += f"O_TwoStar_Zhi_wq_{beton[0]}{beton[1]},"
        
        # O_TwoStar_Zhi_wb 二位直選萬百
        (result, length) =  OTwoStarZhi_Beton()
        for beton in result:
            header += f"O_TwoStar_Zhi_wb_{beton[0]}{beton[1]},"

        # O_TwoStar_Zhi_ws 二位直選萬十
        (result, length) =  OTwoStarZhi_Beton()
        for beton in result:
            header += f"O_TwoStar_Zhi_ws_{beton[0]}{beton[1]},"

        # O_TwoStar_Zhi_wg 二位直選萬個
        (result, length) =  OTwoStarZhi_Beton()
        for beton in result:
            header += f"O_TwoStar_Zhi_wg_{beton[0]}{beton[1]},"

         # O_TwoStar_Zhi_qb 二位直選千百
        (result, length) =  OTwoStarZhi_Beton()
        for beton in result:
            header += f"O_TwoStar_Zhi_qb_{beton[0]}{beton[1]},"

        # O_TwoStar_Zhi_qs 二位直選千十
        (result, length) =  OTwoStarZhi_Beton()
        for beton in result:
            header += f"O_TwoStar_Zhi_qs_{beton[0]}{beton[1]},"

        # O_TwoStar_Zhi_qg 二位直選千個
        (result, length) =  OTwoStarZhi_Beton()
        for beton in result:
            header += f"O_TwoStar_Zhi_qg_{beton[0]}{beton[1]},"

        # O_TwoStar_Zhi_bs 二位直選百十
        (result, length) =  OTwoStarZhi_Beton()
        for beton in result:
            header += f"O_TwoStar_Zhi_bs_{beton[0]}{beton[1]},"

        # O_TwoStar_Zhi_bg 二位直選百個
        (result, length) =  OTwoStarZhi_Beton()
        for beton in result:
            header += f"O_TwoStar_Zhi_bg_{beton[0]}{beton[1]},"
        
        # O_TwoStar_Zhi_sg 二位直選十個
        (result, length) =  OTwoStarZhi_Beton()
        for beton in result:
            header += f"O_TwoStar_Zhi_sg_{beton[0]}{beton[1]},"

        # O_TwoStar_Zu_wq 二位組選萬千
        (result, length) =  OTwoStarZu_Beton()
        for beton in result:
            header += f"O_TwoStar_Zu_wq_{beton[0]}{beton[1]},"
        
        # O_TwoStar_Zu_wb 二位組選萬百
        (result, length) =  OTwoStarZu_Beton()
        for beton in result:
            header += f"O_TwoStar_Zu_wb_{beton[0]}{beton[1]},"

        # O_TwoStar_Zu_ws 二位組選萬十
        (result, length) =  OTwoStarZu_Beton()
        for beton in result:
            header += f"O_TwoStar_Zu_ws_{beton[0]}{beton[1]},"

        # O_TwoStar_Zu_wg 二位組選萬個
        (result, length) =  OTwoStarZu_Beton()
        for beton in result:
            header += f"O_TwoStar_Zu_wg_{beton[0]}{beton[1]},"

        # O_TwoStar_Zu_qb 二位組選千百
        (result, length) =  OTwoStarZu_Beton()
        for beton in result:
            header += f"O_TwoStar_Zu_qb_{beton[0]}{beton[1]},"

        # O_TwoStar_Zu_qs 二位組選千十
        (result, length) =  OTwoStarZu_Beton()
        for beton in result:
            header += f"O_TwoStar_Zu_qs_{beton[0]}{beton[1]},"

        # O_TwoStar_Zu_qg 二位組選千個
        (result, length) =  OTwoStarZu_Beton()
        for beton in result:
            header += f"O_TwoStar_Zu_qg_{beton[0]}{beton[1]},"

        # O_TwoStar_Zu_bs 二位組選百十
        (result, length) =  OTwoStarZu_Beton()
        for beton in result:
            header += f"O_TwoStar_Zu_bs_{beton[0]}{beton[1]},"
        
        # O_TwoStar_Zu_bg 二位組選百個
        (result, length) =  OTwoStarZu_Beton()
        for beton in result:
            header += f"O_TwoStar_Zu_bg_{beton[0]}{beton[1]},"
        
        # O_TwoStar_Zu_sg 二位組選十個
        (result, length) =  OTwoStarZu_Beton()
        for beton in result:
            header += f"O_TwoStar_Zu_sg_{beton[0]}{beton[1]},"

        # O_DingWeiDan_S 定位膽
        (result, length) = ODingWeiDanS_Beton()
        for beton in result:
            header += f"O_DingWeiDan_S_{beton},"

        # O_BSOE_S 大小單雙
        (result, length) = OBSOES_Beton()
        for beton in result:
            header += f"O_BSOE_S_{beton},"

        f.write(header+ '\n')  

        # line
        #====================================================================================
        for opencode in itertools.product('0123456789', repeat = 5):
        #for opencode in itertools.product('012345', repeat = 5):
            print(f"opencode = {opencode[0]}, {opencode[1]}, {opencode[2]}, {opencode[3]}, {opencode[4]}")
            line = f"{opencode[0]}-{opencode[1]}-{opencode[2]}-{opencode[3]}-{opencode[4]},"
            
            """
            # O_FiveStar_ZhiFu 五星直選
            if enableOFiveStarZhiFu:
                (result, length ) = OFiveStarZhiFu_Beton()
                for beton in result:
                    line +=  str(OFiveStarZhiFu_Check(opencode, beton)) + ","
            
            # O_FiveStar_Zu120 五星組選120
            (result, length )= OFiveStarZu120_Beton()
            for beton in result:
                line +=  str(OFiveStarZu120_Check(opencode, beton)) + ","

            # O_FiveStar_Zu60 五星組選60
            (result, length) = OFiveStarZu60_Beton()
            for beton in result:
                line  += str(OFiveStarZu60_Check(opencode, beton)) + ","

            # O_FiveStar_Zu30 五星組選30
            (result, length) = OFiveStarZu30_Beton()
            for beton in result:
                line  += str(OFiveStarZu30_Check(opencode, beton)) + ","

            # O_FiveStar_Zu20 五星組選20
            (result, length) = OFiveStarZu20_Beton()
            for beton in result:
                line  += str(OFiveStarZu20_Check(opencode, beton)) + ","

            # O_FiveStar_Zu10 五星組選10
            (result, length) = OFiveStarZu10_Beton()
            for beton in result:
                line  += str(OFiveStarZu10_Check(opencode, beton)) + ","

            # O_FiveStar_Zu5 五星組選5
            (result, length) = OFiveStarZu5_Beton()
            for beton in result:
                line  += str(OFiveStarZu5_Check(opencode, beton)) + ","

            # O_FiveStar_SpecialOne 一帆风顺
            (result, length) = OFiveStarSpecialOne_Beton()
            for beton in result:
                line  += str(OFiveStarSpecialOne_Check(opencode, beton)) + ","

            # O_FiveStar_SpecialTwo 好事成雙
            (result, length) = OFiveStarSpecialTwo_Beton()
            for beton in result:
                line  += str(OFiveStarSpecialTwo_Check(opencode, beton)) + ","

            # O_FiveStar_SpecialTwo 三星報喜
            (result, length) = OFiveStarSpecialThree_Beton()
            for beton in result:
                line  += str(OFiveStarSpecialThree_Check(opencode, beton)) + ","

            # O_FiveStar_SpecialTwo 四季發財
            (result, length) = OFiveStarSpecialFour_Beton()
            for beton in result:
                line  += str(OFiveStarSpecialFour_Check(opencode, beton)) + ","

            # O_FourStar_ZhiFu 四星直選
            (result, length) = OFourStarZhiFu_Beton()
            for beton in result:
                line  += str(OFourStarZhiFu_Check(opencode, beton)) + ","

            # O_FourStar_Zu24 四星組選24
            (result, length) = OFourStarZu24_Beton()
            for beton in result:
                line  += str(OFourStarZu24_Check(opencode, beton)) + ","

            # O_FourStar_Zu12 四星組選12
            (result, length) = OFourStarZu12_Beton()
            for beton in result:
                line  += str(OFourStarZu12_Check(opencode, beton)) + ","

            # O_FourStar_Zu6 四星組選6
            (result, length) = OFourStarZu6_Beton()
            for beton in result:
                line  += str(OFourStarZu6_Check(opencode, beton)) + ","

            # O_FourStar_Zu4 四星組選4
            (result, length) = OFourStarZu4_Beton()
            for beton in result:
                line  += str(OFourStarZu4_Check(opencode, beton)) + ","

            # O_ThreeStar_Zhi_Front3_S  三位直選錢三
            (result, length) = OThreeStarZhiFront3S_Beton()
            for beton in result:
                line  += str(OThreeStarZhiFront3S_Check(opencode, beton)) + ","

            # O_ThreeStar_Zhi_Front3_S  三位直選中三
            (result, length) = OThreeStarZhiMiddle3S_Beton()
            for beton in result:
                line  += str(OThreeStarZhiMiddle3S_Check(opencode, beton)) + ","

            # O_ThreeStar_Zhi_Last3_S  三位直選後三
            (result, length) = OThreeStarZhiLast3S_Beton()
            for beton in result:
                line  += str(OThreeStarZhiLast3S_Check(opencode, beton)) + ","
            
            # O_ThreeStar_Zu_Front3_S  三位組選前三
            (result, length) = OThreeStarZuFront3S_Beton()
            for beton in result:
                line += str(OThreeStarZuFront3S_Check(opencode, beton)) + ","

            # O_ThreeStar_Zu_Middle_S  三位組選中三
            (result, length) = OThreeStarZuMiddle3S_Beton()
            for beton in result:
                line += str(OThreeStarZuMiddle3S_Check(opencode, beton)) + ","

            # O_ThreeStar_Zu_Last_S  三位組選後三
            (result, length) = OThreeStarZuLast3S_Beton()
            for beton in result:
                line += str(OThreeStarZuLast3S_Check(opencode, beton)) + ","
            """

            # O_ThreeStar_Special_Front3 三位特殊號前三
            (result, length) = OThreeStarSpecial3_Beton()
            for beton in result.keys():
                line += str(OThreeStarSpecialFront3_Check(opencode, result[beton])) + ","

            # O_ThreeStar_Special_Middle3 三位特殊號中三
            (result, length) =  OThreeStarSpecial3_Beton()
            for beton in result.keys():
                line += str(OThreeStarSpecialMiddle3_Check(opencode, result[beton])) + ","
        
            # O_ThreeStar_Special_Last3 三位特殊號後三
            (result, length) =  OThreeStarSpecial3_Beton()
            for beton in result.keys():
                line += str(OThreeStarSpecialLast3_Check(opencode, result[beton])) + ","

            # O_TwoStar_Zhi_wq 二位直選萬千
            (result, length) =  OTwoStarZhi_Beton()
            for beton in result:
                line += str(OTwoStarZhiWQ_Check(opencode, beton)) + ","

             # O_TwoStar_Zhi_wb 二位直選萬百
            (result, length) =  OTwoStarZhi_Beton()
            for beton in result:
                line += str(OTwoStarZhiWB_Check(opencode, beton)) + ","

            # O_TwoStar_Zhi_ws 二位直選萬十
            (result, length) =  OTwoStarZhi_Beton()
            for beton in result:
                line += str(OTwoStarZhiWS_Check(opencode, beton)) + ","

            # O_TwoStar_Zhi_wg 二位直選萬個
            (result, length) =  OTwoStarZhi_Beton()
            for beton in result:
                line += str(OTwoStarZhiWG_Check(opencode, beton)) + ","

            # O_TwoStar_Zhi_qb 二位直選千百
            (result, length) =  OTwoStarZhi_Beton()
            for beton in result:
                line += str(OTwoStarZhiQB_Check(opencode, beton)) + ","

            # O_TwoStar_Zhi_qs 二位直選千十
            (result, length) =  OTwoStarZhi_Beton()
            for beton in result:
                line += str(OTwoStarZhiQS_Check(opencode, beton)) + ","

            # O_TwoStar_Zhi_qg 二位直選千個
            (result, length) =  OTwoStarZhi_Beton()
            for beton in result:
                line += str(OTwoStarZhiQG_Check(opencode, beton)) + ","
            
            # O_TwoStar_Zhi_bs 二位直選百十
            (result, length) =  OTwoStarZhi_Beton()
            for beton in result:
                line += str(OTwoStarZhiBS_Check(opencode, beton)) + ","

            # O_TwoStar_Zhi_bg 二位直選百個
            (result, length) =  OTwoStarZhi_Beton()
            for beton in result:
                line += str(OTwoStarZhiBG_Check(opencode, beton)) + ","
            
            # O_TwoStar_Zhi_sg 二位直選十個
            (result, length) =  OTwoStarZhi_Beton()
            for beton in result:
                line += str(OTwoStarZhiSG_Check(opencode, beton)) + ","

            # O_TwoStar_Zu_wq 二位組選萬千
            (result, length) =  OTwoStarZu_Beton()
            for beton in result:
                line += str(OTwoStarZuWQ_Check(opencode, beton)) + ","
            
            # O_TwoStar_Zu_wb 二位組選萬百
            (result, length) =  OTwoStarZu_Beton()
            for beton in result:
                line += str(OTwoStarZuWB_Check(opencode, beton)) + ","

            # O_TwoStar_Zu_ws 二位組選萬十
            (result, length) =  OTwoStarZu_Beton()
            for beton in result:
                line += str(OTwoStarZuWS_Check(opencode, beton)) + ","

            # O_TwoStar_Zu_wg 二位組選萬個
            (result, length) =  OTwoStarZu_Beton()
            for beton in result:
                line += str(OTwoStarZuWG_Check(opencode, beton)) + ","

            # O_TwoStar_Zu_qb 二位組選千百
            (result, length) =  OTwoStarZu_Beton()
            for beton in result:
                line += str(OTwoStarZuQB_Check(opencode, beton)) + ","

            # O_TwoStar_Zu_qs 二位組選千十
            (result, length) =  OTwoStarZu_Beton()
            for beton in result:
                line += str(OTwoStarZuQS_Check(opencode, beton)) + ","

            # O_TwoStar_Zu_qg 二位組選千個
            (result, length) =  OTwoStarZu_Beton()
            for beton in result:
                line += str(OTwoStarZuQG_Check(opencode, beton)) + ","

            # O_TwoStar_Zu_bs 二位組選百十
            (result, length) =  OTwoStarZu_Beton()
            for beton in result:
                line += str(OTwoStarZuBS_Check(opencode, beton)) + ","
            
            # O_TwoStar_Zu_bg 二位組選百個
            (result, length) =  OTwoStarZu_Beton()
            for beton in result:
                line += str(OTwoStarZuBG_Check(opencode, beton)) + ","
            
            # O_TwoStar_Zu_sg 二位組選十個
            (result, length) =  OTwoStarZu_Beton()
            for beton in result:
                line += str(OTwoStarZuSG_Check(opencode, beton)) + ","
                
            # O_DingWeiDan_S 定位膽
            (result, length) = ODingWeiDanS_Beton()
            for beton in result:
                line += str(ODingWeiDanS_Check(opencode, beton)) + ","

            # O_BSOE_S 大小單雙
            (result, length) = OBSOES_Beton()
            for beton in result:
                line += str(OBSOES_Check(opencode, beton)) + ","

            f.write(line+ '\n')

    #print(rows)
if __name__ == '__main__':
    main()
    