import itertools
import pandas as pd
from argparse import ArgumentParser
import re

def DWD(balls, pos, num):
    return 1 if balls[pos -1] == num else -1

def TFZ3(balls, num1, num2, num3):
    return 1 if (balls[0] == num1 and balls[1] == num2 and balls[2] == num3)  else -1

def TFZ2(balls, num1, num2):
    return 1 if (balls[0] == num1 and balls[1] == num2)  else -1

def TFZ1(balls, num):
    return 1 if balls[0] == num else -1

def B(balls, pos):
    return 1 if balls[pos -1] >=6  else -1

def S(balls, pos):
    return 1 if balls[pos -1] < 6  else -1

def O(balls, pos):
    return 1 if  (balls[pos -1] % 2) != 0  else -1

def E(balls, pos):
    return 1 if  (balls[pos -1] % 2) == 0  else -1

def P(balls, pos):
    return 1 if (balls[pos -1] in [ 1, 2, 3, 5, 7]) else -1

def C(balls, pos):
    return 1 if (balls[pos -1] in [ 4, 6, 8, 9, 10])  else -1

def D1(balls):
    return 1 if balls[0] > balls[9]  else -1

def D2(balls):
    return 1 if balls[1] > balls[8]  else -1

def D3(balls):
    return 1 if balls[2] > balls[7]  else -1

def D4(balls):
    return 1 if balls[3] > balls[6]  else -1

def D5(balls):
    return 1 if balls[4] > balls[5]  else -1

def T1(balls):
    return 1 if balls[0] < balls[9]  else -1

def T2(balls):
    return 1 if balls[1] < balls[8]  else -1

def T3(balls):
    return 1 if balls[2] < balls[7]  else -1

def T4(balls):
    return 1 if balls[3] < balls[6]  else -1

def T5(balls):
    return 1 if balls[4] < balls[5]  else -1

def SUM(balls, num):
    return 1 if (balls[0] + balls[1]) == num else -1

def SUMB(balls):
    return 1 if (balls[0] + balls[1] ) > 11  else -1

def SUMS(balls):
    return 1 if (balls[0] + balls[1] ) <= 11  else -1

def SUMO(balls):
    return 1 if  ((balls[0] + balls[1] ) % 2) != 0  else -1

def SUME(balls):
    return 1 if  ((balls[0] + balls[1] ) % 2) == 0  else -1

def TSZF2(balls, num1, num2):
    result1 = balls[0] == num1 and balls[1] == num2 
    result2 = balls[0] == num2 and balls[1] == num1 
    return 1 if ( result1 or result2 ) else -1

def createHeader():
    headers = [ "opencode" ]
    for i in ALL_BALLS:
        for j in ALL_BALLS:
            headers.append(f"DWD{i}_{j}")
    for (i, j, k) in list(itertools.permutations(ALL_BALLS, 3)):
        headers.append(f"TZF3_{i}-{j}-{k}")
    for (i, j) in list(itertools.permutations(ALL_BALLS, 2)):
        headers.append(f"TZF2_{i}-{j}")
    for i in ALL_BALLS:
        headers.append(f"TZF1_{i}")
    for i in ALL_BALLS:
        headers.append(f"B{i}")   
    for i in ALL_BALLS:
        headers.append(f"S{i}") 
    for i in ALL_BALLS:
        headers.append(f"O{i}") 
    for i in ALL_BALLS:
        headers.append(f"E{i}") 
    for i in ALL_BALLS:
        headers.append(f"P{i}") 
    for i in ALL_BALLS:
        headers.append(f"C{i}") 
    for i in range(1,6):
        headers.append(f"D{i}") 
    for i in range(1,6):
        headers.append(f"T{i}")
    for i in range(3,20):
        headers.append(f"SUM{i}") 
    headers.append(f"SUMB")
    headers.append(f"SUMS")
    headers.append(f"SUMO")
    headers.append(f"SUME")
    for (i, j) in list(itertools.combinations(ALL_BALLS, 2)):
        headers.append(f"TSZF2_{i}-{j}")
    return headers

ALL_BALLS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
def main():
    parser = ArgumentParser()
    parser.add_argument("--header", help="optional argument", dest="header", default=False)
    args = parser.parse_args()
    hasHeader = bool(args.header)
    print("header arg:", hasHeader)

    #ballsList = [(1, 2, 3, 4, 5, 6, 7, 8, 10, 9)]
    ballsList = list(itertools.permutations(ALL_BALLS, 10))

    row_max_length = 20
    row_count = 0
    with open('data/opencode_table.csv', 'w+', encoding='UTF-8') as f:
        headers = createHeader()
        if hasHeader:
            strHeaderWithComma = ','.join(str(e) for e in headers)
            f.write(strHeaderWithComma + "\n")
            print(f"header length:{len(headers)}")

        for balls in ballsList: # ALL
            print(balls)

            #if balls[0] >= 6:
            #    break

            columns = []
            for header in headers:
                if re.match("^DWD([0-9]{1,2})_([0-9]{1,2})$", header):
                    pos = int(header.split("_")[0].replace("DWD", ""))
                    num = int(header.split("_")[1])
                    ret = DWD(balls, pos, num) 
                    columns.append(ret)
                    #print(f"DWD{pos}_{num} = {ret}")
                elif re.match("^TZF3_([0-9]{1,2})-([0-9]{1,2})-([0-9]{1,2})$", header):
                    nums = header.replace("TZF3_", "")
                    num1 = int(nums.split("-")[0])
                    num2 = int(nums.split("-")[1])
                    num3 = int(nums.split("-")[2])
                    ret = TFZ3(balls, num1, num2, num3)
                    columns.append(ret)
                    #print(f"TZF3_{num1}-{num2}-{num3} = {ret}")
                elif re.match("^TZF2_([0-9]{1,2})-([0-9]{1,2})$", header):
                    nums = header.replace("TZF2_", "")
                    num1 = int(nums.split("-")[0])
                    num2 = int(nums.split("-")[1])
                    ret = TFZ2(balls, num1, num2)
                    columns.append(ret)
                    #print(f"TZF2_{num1}-{num2} = {ret}")
                elif re.match("^TZF1_([0-9]{1,2})$", header):
                    num = int(header.replace("TZF1_", ""))
                    ret = TFZ1(balls, num)
                    columns.append(ret)
                    #print(f"TZF1_{num} = {ret}")
                elif re.match("^B([0-9]{1,2})$", header):
                    pos = int(header.replace("B", ""))
                    ret = B(balls, pos)
                    columns.append(ret)
                    #print(f"B{pos} = {ret}")
                elif re.match("^S([0-9]{1,2})$", header):
                    pos = int(header.replace("S", ""))
                    ret = S(balls, pos)
                    columns.append(ret)
                    #print(f"S{pos} = {ret}")
                elif re.match("^O([0-9]{1,2})$", header):
                    pos = int(header.replace("O", ""))
                    ret = O(balls, pos)
                    columns.append(ret)
                    #print(f"O{pos} = {ret}")
                elif re.match("^E([0-9]{1,2})$", header):
                    pos = int(header.replace("E", ""))
                    ret = E(balls, pos)
                    columns.append(ret)
                    #print(f"E{pos} = {ret}")
                elif re.match("^P([0-9]{1,2})$", header):
                    pos = int(header.replace("P", ""))
                    ret = P(balls, pos)
                    columns.append(ret)
                    #print(f"P{pos} = {ret}")
                elif re.match("^C([0-9]{1,2})$", header):
                    pos = int(header.replace("C", ""))
                    ret = C(balls, pos)
                    columns.append(ret)
                    #print(f"C{pos} = {ret}")
                elif header == "D1":
                    ret = D1(balls)
                    columns.append(ret)
                    #print(f"D1 = {ret}")
                elif header == "D2":
                    ret = D2(balls)
                    columns.append(ret)
                    #print(f"D2 = {ret}")
                elif header == "D3":
                    ret = D3(balls)
                    columns.append(ret)
                    #print(f"D3 = {ret}")
                elif header == "D4":
                    ret = D4(balls)
                    columns.append(ret)
                    #print(f"D4 = {ret}")
                elif header == "D5":
                    ret = D5(balls)
                    columns.append(ret)
                    #print(f"D5 = {ret}")
                elif header == "T1":
                    ret = T1(balls)
                    columns.append(ret)
                    #print(f"T1 = {ret}")
                elif header == "T2":
                    ret = T2(balls)
                    columns.append(ret)
                    #print(f"T2 = {ret}")
                elif header == "T3":
                    ret = T3(balls)
                    columns.append(ret)
                    #print(f"T3 = {ret}")
                elif header == "T4":
                    ret = T4(balls)
                    columns.append(ret)
                    #print(f"T4 = {ret}")
                elif header == "T5":
                    ret = T5(balls)
                    columns.append(ret)
                    #print(f"T5 = {ret}")
                elif re.match("^SUM([0-9]{1,2})$", header):
                    num = int(header.replace("SUM", ""))
                    ret = SUM(balls, num)
                    columns.append(ret)
                    #print(f"SUM{num} = {ret}")
                elif header == "SUMB":
                    ret = SUMB(balls)
                    columns.append(ret)
                    #print(f"SUMB = {ret}")
                elif header == "SUMS":
                    ret = SUMS(balls)
                    columns.append(ret)
                    #print(f"SUMS = {ret}")
                elif header == "SUMO":
                    ret = SUMO(balls)
                    columns.append(ret)
                    #print(f"SUMO = {ret}")
                elif header == "SUME":
                    ret = SUME(balls)
                    columns.append(ret)
                    #print(f"SUME = {ret}")
                elif re.match("^TSZF2_([0-9]{1,2})-([0-9]{1,2})$", header):
                    nums = header.replace("TSZF2_", "")
                    num1 = int(nums.split("-")[0])
                    num2 = int(nums.split("-")[1])
                    ret = TSZF2(balls, num1, num2)
                    columns.append(ret)
                    #print(f"TSZF2_{num1}-{num2} = {ret}")

            row_count +=1

            #print(f"columns length:{len(columns)}")
            #rows.append(columns)
            strBalls = '-'.join(str(e) for e in balls)
            strColumnsWithComma = ','.join(str(e) for e in columns)
            f.write(strBalls + "," + strColumnsWithComma + "\n")

    #print(rows)
if __name__ == '__main__':
    main()
    