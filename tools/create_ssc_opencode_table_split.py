import itertools
from logging import fatal
import pandas as pd
from argparse import ArgumentParser
import TransferWager.A5_SSC as A5_SSC
import os
from collections import Counter

def split(word): 
    return [char for char in word]

def OFiveStarZhiFu_Check(opencode:tuple, beton:tuple):
    return 1 if opencode == beton else -1

def OFiveStarZu120_Check(opencode:tuple, beton:tuple):
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

def OFiveStarZu60_Check(opencode:tuple, beton:tuple):
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

def OFiveStarZu30_Check(opencode:tuple, beton:tuple):
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

def OFiveStarZu20_Check(opencode:tuple, beton:tuple):
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

def OFiveStarZu10_Check(opencode:tuple, beton:tuple):
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

def OFiveStarZu5_Check(opencode:tuple, beton:tuple):
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
    

def OFiveStarSpecialOne_Check(opencode:tuple, beton:tuple):
    s = beton[0]
    s_counter = 0
    for num in opencode:
        if s == num:
            s_counter += 1
    
    if s_counter == 1:
            return 1
    else:
        return -1    

def OFiveStarSpecialTwo_Check(opencode:tuple, beton:tuple):
    s = beton[0]
    s_counter = 0
    for num in opencode:
        if s == num:
            s_counter += 1
    
    if s_counter == 2:
            return 1
    else:
        return -1    

def OFiveStarSpecialThree_Check(opencode:tuple, beton:tuple):
    s = beton[0]
    s_counter = 0
    for num in opencode:
        if s == num:
            s_counter += 1
    
    if s_counter == 3:
            return 1
    else:
        return -1  

def OFiveStarSpecialFour_Check(opencode:tuple, beton:tuple):
    s = beton[0]
    s_counter = 0
    for num in opencode:
        if s == num:
            s_counter += 1
    
    if s_counter == 4:
            return 1
    else:
        return -1  

def OFourStarZhiFu_Check(opencode:tuple, beton:tuple):
    if  opencode[1] == beton[0] and opencode[2] == beton[1] and opencode[3] == beton[2] and opencode[4] == beton[3]:
        return 1
    else:
        return -1 

def OFourStarZu24_Check(opencode:tuple, beton:tuple):
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

def OFourStarZu12_Check(opencode:tuple, beton:tuple):
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

def OFourStarZu6_Check(opencode:tuple, beton:tuple):
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

def OFourStarZu4_Check(opencode:tuple, beton:tuple):
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

def OThreeStarZhiFront3S_Check(opencode:tuple, beton:tuple):
    if  opencode[0] == beton[0] and opencode[1] == beton[1] and opencode[2] == beton[2]:
        return 1
    else:
        return -1 

def OThreeStarZhiMiddle3S_Check(opencode:tuple, beton:tuple):
    if  opencode[1] == beton[0] and opencode[2] == beton[1] and opencode[3] == beton[2]:
        return 1
    else:
        return -1 

def OThreeStarZhiLast3S_Check(opencode:tuple, beton:tuple):
    if  opencode[2] == beton[0] and opencode[3] == beton[1] and opencode[4] == beton[2]:
        return 1
    else:
        return -1 

def OThreeStarZuFront3S_Check(opencode:tuple, beton:tuple):
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

def OThreeStarZuMiddle3S_Check(opencode:tuple, beton:tuple):
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

def OThreeStarZuLast3S_Check(opencode:tuple, beton:tuple):
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

def ThreeStartSpecialNum():
    result = {}
    result["LEOPARD"] = []
    result["CTN"] = []
    result["PAIR"] = []
    result["HALF"] = []
    result["SIX"] = []
    for (a, b, c) in itertools.product("0123456789", repeat=3):
        if a == b and b==c:
            result["LEOPARD"].append((a, b, c))
        elif (( int(a) - int(b) == 1) and ( int(b) - int(c) ==1))  or \
            (( int(b) - int(a) == 1) and ( int(a) - int(c) ==1)) or \
            (( int(b) - int(c) == 1) and ( int(c) - int(a) ==1)) or \
            (( int(c) - int(b) == 1) and ( int(b) - int(a) ==1)) or \
            (( int(c) - int(a) == 1) and ( int(a) - int(b) ==1)) or \
            (( int(a) - int(c) == 1) and ( int(c) - int(b) ==1)):
            result["CTN"].append((a, b, c))
        elif a == b or b==c or a==c:
            result["PAIR"].append((a, b, c))
        elif ( int(a) - int(b) == 1)  or  ( int(b) - int(c) == 1) or ( int(c) - int(a) == 1)  or ( int(b) - int(a) == 1)  or ( int(a) - int(c) == 1) or ( int(c) - int(b) == 1):   
            result["HALF"] .append((a, b, c))
        else:
            result["SIX"].append((a, b, c))
    return result

def OThreeStarSpecialFront3_Check(opencode:tuple, beton:str):
    result = ThreeStartSpecialNum()
    (a, b, c) = (int(opencode[0]), int(opencode[1]), int(opencode[2]))
    if (a, b, c)  in result[beton] :
        return 1
    else:
        return -1

def OThreeStarSpecialMiddle3_Check(opencode:tuple, beton:str):
    result = ThreeStartSpecialNum()
    (a, b, c) = (int(opencode[1]), int(opencode[2]), int(opencode[3]))
    if (a, b, c)  in result[beton] :
        return 1
    else:
        return -1

def OThreeStarSpecialLast3_Check(opencode:tuple, beton:str):
    result = ThreeStartSpecialNum()
    (a, b, c) = (int(opencode[2]), int(opencode[3]), int(opencode[4]))
    if (a, b, c)  in result[beton] :
        return 1
    else:
        return -1

def OTwoStarZhiWQ_Check(opencode:tuple, beton:tuple):
    (a, b) = (int(opencode[0]), int(opencode[1]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZhiWB_Check(opencode:tuple, beton:tuple):
    (a, b) = (int(opencode[0]), int(opencode[2]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZhiWS_Check(opencode:tuple, beton:tuple):
    (a, b) = (int(opencode[0]), int(opencode[3]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZhiWG_Check(opencode:tuple, beton:tuple):
    (a, b) = (int(opencode[0]), int(opencode[4]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZhiQB_Check(opencode:tuple, beton:tuple):
    (a, b) = (int(opencode[1]), int(opencode[2]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZhiQS_Check(opencode:tuple, beton:tuple):
    (a, b) = (int(opencode[1]), int(opencode[3]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZhiQG_Check(opencode:tuple, beton:tuple):
    (a, b) = (int(opencode[1]), int(opencode[4]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZhiBS_Check(opencode:tuple, beton:tuple):
    (a, b) = (int(opencode[2]), int(opencode[3]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZhiBG_Check(opencode:tuple, beton:tuple):
    (a, b) = (int(opencode[2]), int(opencode[4]))
    if (a, b) == beton:
        return 1
    else:
        return -1
    
def OTwoStarZhiSG_Check(opencode:tuple, beton:tuple):
    (a, b) = (int(opencode[3]), int(opencode[4]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZuWQ_Check(opencode:tuple, beton:tuple):
    (a, b) = (int(opencode[0]), int(opencode[1]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZuWB_Check(opencode:tuple, beton:tuple):
    (a, b) = (int(opencode[0]), int(opencode[2]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZuWS_Check(opencode:tuple, beton:tuple):
    (a, b) = (int(opencode[0]), int(opencode[3]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZuWG_Check(opencode:tuple, beton:tuple):
    (a, b) = (int(opencode[0]), int(opencode[4]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZuQB_Check(opencode:tuple, beton:tuple):
    (a, b) = (int(opencode[1]), int(opencode[2]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZuQS_Check(opencode:tuple, beton:tuple):
    (a, b) = (int(opencode[1]), int(opencode[3]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZuQG_Check(opencode:tuple, beton:tuple):
    (a, b) = (int(opencode[1]), int(opencode[4]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZuBS_Check(opencode:tuple, beton:tuple):
    (a, b) = (int(opencode[2]), int(opencode[3]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZuBG_Check(opencode:tuple, beton:tuple):
    (a, b) = (int(opencode[2]), int(opencode[4]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def OTwoStarZuSG_Check(opencode:tuple, beton:tuple):
    (a, b) = (int(opencode[3]), int(opencode[4]))
    if (a, b) == beton:
        return 1
    else:
        return -1

def ODingWeiDanS_Check(opencode:tuple, beton:tuple):
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

def OBSOES_Check(opencode:tuple, beton:tuple):
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

def ODragonTigerWQ_Check(opencode:tuple, beton:str):
    a = int(opencode[0])
    b = int(opencode[1])
    if beton == "D":
        return 1 if a > b  else -1 
    elif beton == "T":
        return 1 if a < b  else -1 
    elif beton == "TT":
        return 1 if a == b  else -1 

def ODragonTigerWB_Check(opencode:tuple, beton:str):
    a = int(opencode[0])
    b = int(opencode[2])
    if beton == "D":
        return 1 if a > b  else -1 
    elif beton == "T":
        return 1 if a < b  else -1 
    elif beton == "TT":
        return 1 if a == b  else -1

def ODragonTigerWS_Check(opencode:tuple, beton:str):
    a = int(opencode[0])
    b = int(opencode[3])
    if beton == "D":
        return 1 if a > b  else -1 
    elif beton == "T":
        return 1 if a < b  else -1 
    elif beton == "TT":
        return 1 if a == b  else -1

def ODragonTigerWG_Check(opencode:tuple, beton:str):
    a = int(opencode[0])
    b = int(opencode[4])
    if beton == "D":
        return 1 if a > b  else -1 
    elif beton == "T":
        return 1 if a < b  else -1 
    elif beton == "TT":
        return 1 if a == b  else -1

def ODragonTigerQB_Check(opencode:tuple, beton:str):
    a = int(opencode[1])
    b = int(opencode[2])
    if beton == "D":
        return 1 if a > b  else -1 
    elif beton == "T":
        return 1 if a < b  else -1 
    elif beton == "TT":
        return 1 if a == b  else -1

def ODragonTigerQS_Check(opencode:tuple, beton:str):
    a = int(opencode[1])
    b = int(opencode[3])
    if beton == "D":
        return 1 if a > b  else -1 
    elif beton == "T":
        return 1 if a < b  else -1 
    elif beton == "TT":
        return 1 if a == b  else -1

def ODragonTigerQG_Check(opencode:tuple, beton:str):
    a = int(opencode[1])
    b = int(opencode[4])
    if beton == "D":
        return 1 if a > b  else -1 
    elif beton == "T":
        return 1 if a < b  else -1 
    elif beton == "TT":
        return 1 if a == b  else -1

def ODragonTigerBS_Check(opencode:tuple, beton:str):
    a = int(opencode[2])
    b = int(opencode[3])
    if beton == "D":
        return 1 if a > b  else -1 
    elif beton == "T":
        return 1 if a < b  else -1 
    elif beton == "TT":
        return 1 if a == b  else -1

def ODragonTigerBG_Check(opencode:tuple, beton:str):
    a = int(opencode[2])
    b = int(opencode[4])
    if beton == "D":
        return 1 if a > b  else -1 
    elif beton == "T":
        return 1 if a < b  else -1 
    elif beton == "TT":
        return 1 if a == b  else -1

def ODragonTigerSG_Check(opencode:tuple, beton:str):
    a = int(opencode[3])
    b = int(opencode[4])
    if beton == "D":
        return 1 if a > b  else -1 
    elif beton == "T":
        return 1 if a < b  else -1 
    elif beton == "TT":
        return 1 if a == b  else -1

def header():
    header = "opencode,"
    # O_FiveStar_ZhiFu 五星直選
    (result, length ) = A5_SSC.OFiveStarZhiFu_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_FiveStar_ZhiFu length:{length}")

    # O_FiveStar_Zu120 五星組選120
    (result, length )= A5_SSC.OFiveStarZu120_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_FiveStar_Zu120 length:{length}")

    # O_FiveStar_Zu60 五星組選60
    (result, length) = A5_SSC.OFiveStarZu60_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_FiveStar_Zu60 length:{length}")

    # O_FiveStar_Zu30 五星組選30
    (result, length) = A5_SSC.OFiveStarZu30_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_FiveStar_Zu30 length:{length}")

    # O_FiveStar_Zu20 五星組選20
    (result, length) = A5_SSC.OFiveStarZu20_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_FiveStar_Zu20 length:{length}")

        # O_FiveStar_Zu10 五星組選10
    (result, length) = A5_SSC.OFiveStarZu10_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_FiveStar_Zu10 length:{length}")

    # O_FiveStar_Zu5 五星組選5
    (result, length) = A5_SSC.OFiveStarZu5_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_FiveStar_Zu5 length:{length}")

    # O_FiveStar_SpecialOne 一帆风顺
    (result, length) = A5_SSC.OFiveStarSpecialOne_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_FiveStar_SpecialOne length:{length}")

    # O_FiveStar_SpecialTwo 好事成雙
    (result, length) = A5_SSC.OFiveStarSpecialTwo_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_FiveStar_SpecialTwo length:{length}")
    
    # O_FiveStar_SpecialTwo 三星報喜
    (result, length) = A5_SSC.OFiveStarSpecialThree_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_FiveStar_SpecialThree length:{length}")

    # O_FiveStar_SpecialTwo 四季發財
    (result, length) = A5_SSC.OFiveStarSpecialFour_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_FiveStar_SpecialFour length:{length}")
    
    # O_FourStar_ZhiFu 四星直選
    (result, length) = A5_SSC.OFourStarZhiFu_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_FourStar_ZhiFu length:{length}")

    # O_FourStar_Zu24 四星組選24
    (result, length) = A5_SSC.OFourStarZu24_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_FourStar_Zu24 length:{length}")

    # O_FourStar_Zu12 四星組選12
    (result, length) = A5_SSC.OFourStarZu12_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_FourStar_Zu12 length:{length}")

    # O_FourStar_Zu6 四星組選6
    (result, length) = A5_SSC.OFourStarZu6_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_FourStar_Zu6 length:{length}")

    # O_FourStar_Zu4 四星組選4
    (result, length) = A5_SSC.OFourStarZu4_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_FourStar_Zu4 length:{length}")

    # O_ThreeStar_Zhi_Front3_S  三位直選前三
    (result, length) = A5_SSC.OThreeStarZhiFront3S_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_ThreeStar_Zhi_Front3_S length:{length}")

    # O_ThreeStar_Zhi_Front3_S  三位直選中三
    (result, length) = A5_SSC.OThreeStarZhiMiddle3S_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_ThreeStar_Zhi_Middle3_S length:{length}")

    # O_ThreeStar_Zhi_Last3_S  三位直選後三
    (result, length) = A5_SSC.OThreeStarZhiLast3S_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_ThreeStar_Zhi_Last3_S length:{length}")

    # O_ThreeStar_Zu_Front3_S  三位組選前三
    (result, length) = A5_SSC.OThreeStarZuFront3S_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_ThreeStar_Zu_Front3_S length:{length}")

    # O_ThreeStar_Zu_Middle3_S  三位組選前三
    (result, length) = A5_SSC.OThreeStarZuMiddle3S_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_ThreeStar_Zu_Middle3_S length:{length}")

    # O_ThreeStar_Zu_Last3_S  三位組選後三
    (result, length) = A5_SSC.OThreeStarZuLast3S_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_ThreeStar_Zu_Last3_S length:{length}")

    # O_ThreeStar_Special_Front3 三位特殊號前三
    (result, length) =  A5_SSC.OThreeStarSpecialFront3_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_ThreeStar_Special_Front3 length:{length}")
    
    # O_ThreeStar_Special_Middle3 三位特殊號中三
    (result, length) =  A5_SSC.OThreeStarSpecialMiddle3_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_ThreeStar_Special_Middle3 length:{length}")

    # O_ThreeStar_Special_Last3 三位特殊號後三
    (result, length) =  A5_SSC.OThreeStarSpecialLast3_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_ThreeStar_Special_Last3 length:{length}")

    # O_TwoStar_Zhi_wq 二位直選萬千
    (result, length) =  A5_SSC.OTwoStarZhiWQ_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_TwoStar_Zhi_wq length:{length}")

    # O_TwoStar_Zhi_wb 二位直選萬百
    (result, length) =  A5_SSC.OTwoStarZhiWB_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_TwoStar_Zhi_wb length:{length}")

    # O_TwoStar_Zhi_ws 二位直選萬十
    (result, length) =  A5_SSC.OTwoStarZhiWS_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_TwoStar_Zhi_ws length:{length}")

    # O_TwoStar_Zhi_wg 二位直選萬個
    (result, length) = A5_SSC.OTwoStarZhiWG_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_TwoStar_Zhi_wg length:{length}")

    # O_TwoStar_Zhi_qb 二位直選千百
    (result, length) = A5_SSC.OTwoStarZhiQB_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_TwoStar_Zhi_qb length:{length}")

    # O_TwoStar_Zhi_qs 二位直選千十
    (result, length) = A5_SSC.OTwoStarZhiQS_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_TwoStar_Zhi_qs length:{length}")

    # O_TwoStar_Zhi_qg 二位直選千個
    (result, length) = A5_SSC.OTwoStarZhiQG_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_TwoStar_Zhi_qg length:{length}")

    # O_TwoStar_Zhi_bs 二位直選百十
    (result, length) = A5_SSC.OTwoStarZhiBS_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_TwoStar_Zhi_bs length:{length}")

    # O_TwoStar_Zhi_bg 二位直選百個
    (result, length) = A5_SSC.OTwoStarZhiBG_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_TwoStar_Zhi_bg length:{length}")

    # O_TwoStar_Zhi_sg 二位直選十個
    (result, length) = A5_SSC.OTwoStarZhiSG_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_TwoStar_Zhi_sg length:{length}")

    # O_TwoStar_Zu_wq 二位組選萬千
    (result, length) = A5_SSC.OTwoStarZuWQ_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_TwoStar_Zu_wq length:{length}")

    # O_TwoStar_Zu_wb 二位組選萬百
    (result, length) = A5_SSC.OTwoStarZuWB_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_TwoStar_Zu_wb length:{length}")

    # O_TwoStar_Zu_ws 二位組選萬十
    (result, length) = A5_SSC.OTwoStarZuWS_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_TwoStar_Zu_ws length:{length}")

    # O_TwoStar_Zu_wg 二位組選萬個
    (result, length) =  A5_SSC.OTwoStarZuWG_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_TwoStar_Zu_wg length:{length}")

    # O_TwoStar_Zu_qb 二位組選千百
    (result, length) =  A5_SSC.OTwoStarZuQB_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_TwoStar_Zu_qb length:{length}")

    # O_TwoStar_Zu_qs 二位組選千十
    (result, length) = A5_SSC.OTwoStarZuQS_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_TwoStar_Zu_qs length:{length}")

    # O_TwoStar_Zu_qg 二位組選千個
    (result, length) = A5_SSC.OTwoStarZuQG_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_TwoStar_Zu_qg length:{length}")

    # O_TwoStar_Zu_bs 二位組選百十
    (result, length) = A5_SSC.OTwoStarZuBS_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_TwoStar_Zu_bs length:{length}")

    # O_TwoStar_Zu_bg 二位組選百個
    (result, length) = A5_SSC.OTwoStarZuBG_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_TwoStar_Zu_bg length:{length}")

    # O_TwoStar_Zu_sg 二位組選十個
    (result, length) = A5_SSC.OTwoStarZuSG_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_TwoStar_Zu_sg length:{length}")

    # O_DingWeiDan_S 定位膽
    (result, length) = A5_SSC.ODingWeiDanS_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_DingWeiDan_S length:{length}")

    # O_BSOE_S 大小單雙
    (result, length) = A5_SSC.OBSOES_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_BSOE_S length:{length}")

    # O_DragonTiger_wq 龍虎和萬千
    (result, length) = A5_SSC.ODragonTigerWQ_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_DragonTiger_wq length:{length}")

    # O_DragonTiger_wb 龍虎和萬百
    (result, length) = A5_SSC.ODragonTigerWB_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_DragonTiger_wb length:{length}")

    # O_DragonTiger_ws 龍虎和萬十
    (result, length) = A5_SSC.ODragonTigerWS_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_DragonTiger_ws length:{length}")

    # O_DragonTiger_wg 龍虎和萬個
    (result, length) = A5_SSC.ODragonTigerWG_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_DragonTiger_wq length:{length}")

    # O_DragonTiger_qb 龍虎和千百
    (result, length) = A5_SSC.ODragonTigerQB_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_DragonTiger_qb length:{length}")

    # O_DragonTiger_qs 龍虎和千十
    (result, length) = A5_SSC.ODragonTigerQS_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_DragonTiger_qs length:{length}")

    # O_DragonTiger_qg 龍虎和千個
    (result, length) = A5_SSC.ODragonTigerQG_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_DragonTiger_qg length:{length}")

    # O_DragonTiger_bs 龍虎和百十
    (result, length) = A5_SSC.ODragonTigerBS_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_DragonTiger_bs length:{length}")

    # O_DragonTiger_bg 龍虎和百個
    (result, length) = A5_SSC.ODragonTigerBG_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_DragonTiger_bg length:{length}")

    # O_DragonTiger_sg 龍虎和十個
    (result, length) = A5_SSC.ODragonTigerSG_Beton()
    for beton in result:
        header += f"{beton},"
    print(f"O_DragonTiger_sg length:{length}")

    header_len = len(header)
    return header[:header_len-1] #移除最後一個逗號

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

    f1 = open(f'{currentPath}/data/opencode_ssc_table_1.csv', 'w+', encoding='UTF-8')
    f1.write(header()+ '\n')  

    f2 = open(f'{currentPath}/data/opencode_ssc_table_2.csv', 'w+', encoding='UTF-8')
    f2.write(header()+ '\n')  

    rowIndex  = 0
    for opencode in itertools.product('0123456789', repeat = 5):
        # b百 s拾 q千 w萬 g個
        print(f"opencode = {opencode[0]}, {opencode[1]}, {opencode[2]}, {opencode[3]}, {opencode[4]}")
        line = f"{opencode[0]}-{opencode[1]}-{opencode[2]}-{opencode[3]}-{opencode[4]},"
        
        # O_FiveStar_ZhiFu 五星直選
        (result, length ) = A5_SSC.OFiveStarZhiFu_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            line +=  str(OFiveStarZhiFu_Check(opencode, tmp_beton)) + ","
        
        # O_FiveStar_Zu120 五星組選120
        (result, length )= A5_SSC.OFiveStarZu120_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            line +=  str(OFiveStarZu120_Check(opencode, tmp_beton)) + ","

        # O_FiveStar_Zu60 五星組選60
        (result, length) = A5_SSC.OFiveStarZu60_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            line  += str(OFiveStarZu60_Check(opencode, tmp_beton)) + ","

        # O_FiveStar_Zu30 五星組選30
        (result, length) =A5_SSC.OFiveStarZu30_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            line  += str(OFiveStarZu30_Check(opencode, tmp_beton)) + ","

        # O_FiveStar_Zu20 五星組選20
        (result, length) = A5_SSC.OFiveStarZu20_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            line  += str(OFiveStarZu20_Check(opencode, tmp_beton)) + ","

        # O_FiveStar_Zu10 五星組選10
        (result, length) =A5_SSC.OFiveStarZu10_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            line  += str(OFiveStarZu10_Check(opencode, tmp_beton)) + ","

        # O_FiveStar_Zu5 五星組選5
        (result, length) = A5_SSC.OFiveStarZu5_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            line  += str(OFiveStarZu5_Check(opencode, tmp_beton)) + ","

        # O_FiveStar_SpecialOne 一帆风顺
        (result, length) = A5_SSC.OFiveStarSpecialOne_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            line  += str(OFiveStarSpecialOne_Check(opencode, tmp_beton)) + ","

        # O_FiveStar_SpecialTwo 好事成雙
        (result, length) = A5_SSC.OFiveStarSpecialTwo_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            line  += str(OFiveStarSpecialTwo_Check(opencode, tmp_beton)) + ","

        # O_FiveStar_SpecialTwo 三星報喜
        (result, length) = A5_SSC.OFiveStarSpecialThree_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            line  += str(OFiveStarSpecialThree_Check(opencode, tmp_beton)) + ","

        # O_FiveStar_SpecialTwo 四季發財
        (result, length) = A5_SSC.OFiveStarSpecialFour_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            line  += str(OFiveStarSpecialFour_Check(opencode, tmp_beton)) + ","

        # O_FourStar_ZhiFu 四星直選
        (result, length) = A5_SSC.OFourStarZhiFu_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            line  += str(OFourStarZhiFu_Check(opencode, tmp_beton)) + ","

        # O_FourStar_Zu24 四星組選24
        (result, length) = A5_SSC.OFourStarZu24_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            line  += str(OFourStarZu24_Check(opencode, tmp_beton)) + ","

        # O_FourStar_Zu12 四星組選12
        (result, length) = A5_SSC.OFourStarZu12_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            line  += str(OFourStarZu12_Check(opencode, tmp_beton)) + ","

        # O_FourStar_Zu6 四星組選6
        (result, length) = A5_SSC.OFourStarZu6_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line  += str(OFourStarZu6_Check(opencode, tmp_beton)) + ","

        # O_FourStar_Zu4 四星組選4
        (result, length) = A5_SSC.OFourStarZu4_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line  += str(OFourStarZu4_Check(opencode, tmp_beton)) + ","

        # O_ThreeStar_Zhi_Front3_S  三位直選錢三
        (result, length) = A5_SSC.OThreeStarZhiFront3S_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line  += str(OThreeStarZhiFront3S_Check(opencode, tmp_beton)) + ","

        # O_ThreeStar_Zhi_Front3_S  三位直選中三
        (result, length) = A5_SSC.OThreeStarZhiMiddle3S_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line  += str(OThreeStarZhiMiddle3S_Check(opencode, tmp_beton)) + ","

        # O_ThreeStar_Zhi_Last3_S  三位直選後三
        (result, length) = A5_SSC.OThreeStarZhiLast3S_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line  += str(OThreeStarZhiLast3S_Check(opencode, tmp_beton)) + ","
        
        # O_ThreeStar_Zu_Front3_S  三位組選前三
        (result, length) = A5_SSC.OThreeStarZuFront3S_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OThreeStarZuFront3S_Check(opencode, tmp_beton)) + ","

        # O_ThreeStar_Zu_Middle_S  三位組選中三
        (result, length) = A5_SSC.OThreeStarZuMiddle3S_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OThreeStarZuMiddle3S_Check(opencode, tmp_beton)) + ","

        # O_ThreeStar_Zu_Last_S  三位組選後三
        (result, length) = A5_SSC.OThreeStarZuLast3S_Beton()
        for beton in result:
            tmp_beton = tuple(split(beton.split("_")[-1:][0]))
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OThreeStarZuLast3S_Check(opencode, tmp_beton)) + ","
        
        # O_ThreeStar_Special_Front3 三位特殊號前三
        (result, length) = A5_SSC.OThreeStarSpecialFront3_Beton()
        for beton in result:
            tmp_beton = beton.split("_")[-1:][0]
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OThreeStarSpecialFront3_Check(opencode, tmp_beton)) + ","

        # O_ThreeStar_Special_Middle3 三位特殊號中三
        (result, length) =  A5_SSC.OThreeStarSpecialMiddle3_Beton()
        for beton in result:
            tmp_beton = beton.split("_")[-1:][0]
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OThreeStarSpecialMiddle3_Check(opencode, tmp_beton)) + ","
    
        # O_ThreeStar_Special_Last3 三位特殊號後三
        (result, length) =  A5_SSC.OThreeStarSpecialLast3_Beton()
        for beton in result:
            tmp_beton = beton.split("_")[-1:][0]
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OThreeStarSpecialLast3_Check(opencode, tmp_beton)) + ","

        # O_TwoStar_Zhi_wq 二位直選萬千
        (result, length) =  A5_SSC.OTwoStarZhiWQ_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OTwoStarZhiWQ_Check(opencode, tmp_beton)) + ","

        # O_TwoStar_Zhi_wb 二位直選萬百
        (result, length) = A5_SSC.OTwoStarZhiWB_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OTwoStarZhiWB_Check(opencode, tmp_beton)) + ","

        # O_TwoStar_Zhi_ws 二位直選萬十
        (result, length) = A5_SSC.OTwoStarZhiWS_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OTwoStarZhiWS_Check(opencode, tmp_beton)) + ","

        # O_TwoStar_Zhi_wg 二位直選萬個
        (result, length) =  A5_SSC.OTwoStarZhiWG_Beton()
        for beton in result:
            tmp_beton =tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OTwoStarZhiWG_Check(opencode, tmp_beton)) + ","

        # O_TwoStar_Zhi_qb 二位直選千百
        (result, length) =  A5_SSC.OTwoStarZhiQB_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OTwoStarZhiQB_Check(opencode,tmp_beton)) + ","

        # O_TwoStar_Zhi_qs 二位直選千十
        (result, length) =  A5_SSC.OTwoStarZhiQS_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OTwoStarZhiQS_Check(opencode, tmp_beton)) + ","

        # O_TwoStar_Zhi_qg 二位直選千個
        (result, length) = A5_SSC.OTwoStarZhiQG_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OTwoStarZhiQG_Check(opencode, tmp_beton)) + ","
        
        # O_TwoStar_Zhi_bs 二位直選百十
        (result, length) =  A5_SSC.OTwoStarZhiBS_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OTwoStarZhiBS_Check(opencode, tmp_beton)) + ","

        # O_TwoStar_Zhi_bg 二位直選百個
        (result, length) = A5_SSC.OTwoStarZhiBG_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OTwoStarZhiBG_Check(opencode, tmp_beton)) + ","
        
        # O_TwoStar_Zhi_sg 二位直選十個
        (result, length) =  A5_SSC.OTwoStarZhiSG_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OTwoStarZhiSG_Check(opencode, tmp_beton)) + ","

        # O_TwoStar_Zu_wq 二位組選萬千
        (result, length) =  A5_SSC.OTwoStarZuWQ_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OTwoStarZuWQ_Check(opencode, tmp_beton)) + ","
        
        # O_TwoStar_Zu_wb 二位組選萬百
        (result, length) = A5_SSC.OTwoStarZuWB_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OTwoStarZuWB_Check(opencode, tmp_beton)) + ","

        # O_TwoStar_Zu_ws 二位組選萬十
        (result, length) =  A5_SSC.OTwoStarZuWS_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OTwoStarZuWS_Check(opencode, tmp_beton)) + ","

        # O_TwoStar_Zu_wg 二位組選萬個
        (result, length) = A5_SSC.OTwoStarZuWG_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OTwoStarZuWG_Check(opencode, tmp_beton)) + ","

        # O_TwoStar_Zu_qb 二位組選千百
        (result, length) = A5_SSC.OTwoStarZuQB_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OTwoStarZuQB_Check(opencode, tmp_beton)) + ","

        # O_TwoStar_Zu_qs 二位組選千十
        (result, length) = A5_SSC.OTwoStarZuQS_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OTwoStarZuQS_Check(opencode, tmp_beton)) + ","

        # O_TwoStar_Zu_qg 二位組選千個
        (result, length) =  A5_SSC.OTwoStarZuQG_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OTwoStarZuQG_Check(opencode, tmp_beton)) + ","

        # O_TwoStar_Zu_bs 二位組選百十
        (result, length) = A5_SSC.OTwoStarZuBS_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OTwoStarZuBS_Check(opencode, tmp_beton)) + ","
        
        # O_TwoStar_Zu_bg 二位組選百個
        (result, length) = A5_SSC.OTwoStarZuBG_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OTwoStarZuBG_Check(opencode, tmp_beton)) + ","
        
        # O_TwoStar_Zu_sg 二位組選十個
        (result, length) = A5_SSC.OTwoStarZuSG_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OTwoStarZuSG_Check(opencode, tmp_beton)) + ","
            
        # O_DingWeiDan_S 定位膽
        (result, length) = A5_SSC.ODingWeiDanS_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(ODingWeiDanS_Check(opencode, tmp_beton)) + ","

        # O_BSOE_S 大小單雙
        (result, length) = A5_SSC.OBSOES_Beton()
        for beton in result:
            tmp_beton = tuple(beton.split("_")[-1:][0])
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(OBSOES_Check(opencode, tmp_beton)) + ","

        # O_DragonTiger_wq 龍虎和萬千
        (result, length) = A5_SSC.ODragonTigerWQ_Beton()
        for beton in result:
            tmp_beton = beton.split("_")[-1:][0]
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(ODragonTigerWQ_Check(opencode, tmp_beton)) + ","
        
        # O_DragonTiger_wb 龍虎和萬百
        (result, length) = A5_SSC.ODragonTigerWB_Beton()
        for beton in result:
            tmp_beton = beton.split("_")[-1:][0]
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(ODragonTigerWB_Check(opencode, tmp_beton)) + ","
        
        # O_DragonTiger_ws 龍虎和萬十
        (result, length) = A5_SSC.ODragonTigerWS_Beton()
        for beton in result:
            tmp_beton = beton.split("_")[-1:][0]
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(ODragonTigerWS_Check(opencode, tmp_beton)) + ","

        # O_DragonTiger_wg 龍虎和萬個
        (result, length) = A5_SSC.ODragonTigerWG_Beton()
        for beton in result:
            tmp_beton = beton.split("_")[-1:][0]
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(ODragonTigerWG_Check(opencode, tmp_beton)) + ","

        # O_DragonTiger_qb 龍虎和千百
        (result, length) = A5_SSC.ODragonTigerQB_Beton()
        for beton in result:
            tmp_beton = beton.split("_")[-1:][0]
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(ODragonTigerQB_Check(opencode, tmp_beton)) + ","

        # O_DragonTiger_qs 龍虎和千十
        (result, length) = A5_SSC.ODragonTigerQS_Beton()
        for beton in result:
            tmp_beton = beton.split("_")[-1:][0]
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(ODragonTigerQS_Check(opencode, tmp_beton)) + ","

        # O_DragonTiger_qg 龍虎和千個
        (result, length) = A5_SSC.ODragonTigerQG_Beton()
        for beton in result:
            tmp_beton = beton.split("_")[-1:][0]
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(ODragonTigerQG_Check(opencode, tmp_beton)) + ","

        # O_DragonTiger_bs 龍虎和百十
        (result, length) = A5_SSC.ODragonTigerBS_Beton()
        for beton in result:
            tmp_beton = beton.split("_")[-1:][0]
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(ODragonTigerBS_Check(opencode, tmp_beton)) + ","

        # O_DragonTiger_bg 龍虎和百個
        (result, length) = A5_SSC.ODragonTigerBG_Beton()
        for beton in result:
            tmp_beton = beton.split("_")[-1:][0]
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(ODragonTigerBG_Check(opencode, tmp_beton)) + ","

        # O_DragonTiger_sg 龍虎和十個
        (result, length) = A5_SSC.ODragonTigerSG_Beton()
        for beton in result:
            tmp_beton = beton.split("_")[-1:][0]
            #print(f"beton={beton}, tmp_beton={tmp_beton}")
            line += str(ODragonTigerSG_Check(opencode, tmp_beton)) + ","

        if rowIndex < 50000:
            line_len = len(line)
            f1.write(line[:line_len-1]+ '\n') #移除最後一個逗號
        else:
            line_len = len(line)
            f2.write(line[:line_len-1]+ '\n') #移除最後一個逗號
        
        rowIndex += 1

    f1.close()
    f2.close()
    #print(rows)
if __name__ == '__main__':
    main()
    