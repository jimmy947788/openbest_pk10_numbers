import json
import itertools
import logging
import os, sys
from pathlib import Path
import datetime
import pyopencl as cl
import time
import numpy as np

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

def ConvertWager(raw_data):
    amount_table = []
    amount_with_odds_table = []
    jdata = json.loads(raw_data)
    total_bet_count = 0
    total_bet_amount = 0
    
    expectId = jdata["ExpectID"]

    wager_length = len(jdata["Bets"])
    for bet in jdata["Bets"]:
        betTypePlayCode = bet['BetTypePlayCode']
        unitAmount = bet["UnitAmount"]
        rawBetOn = bet["BetOn"]
        betOnCount = int(bet["BetOnCount"])
        #logging.debug(f"BetTypePlayCode={betTypePlayCode}, BetOn={rawBetOn}, UnitAmount={unitAmount}, betOnCount={betOnCount}")
        extraData = json.loads(bet["ExtraData"])
        odds = []
        betOn = []
        for i in range(betOnCount):
            if len(extraData["ExtraBets"]) == 1:
                odds.append(extraData["ExtraBets"][0]["Odds"])
            else:
                odds.append(extraData["ExtraBets"][i]["Odds"])

        # betTypePlayCode 轉換成解答表格式
        if betTypePlayCode == "O_12Sum":
            betOn=SUM(rawBetOn)
        elif betTypePlayCode == "O_12Sum_BSOE":
            betOn=SUM_BSOE(rawBetOn)
        elif betTypePlayCode == "O_BSOE":
            betOn=BSOE(rawBetOn)
        elif betTypePlayCode == "O_DingWeiDan":
            betOn=DWD(rawBetOn)
        elif betTypePlayCode == "O_DragonTiger":
            betOn=DT(rawBetOn)
        elif betTypePlayCode == "O_ThreeStar_Zhi_Front1":
            betOn=TZF1(rawBetOn)
        elif betTypePlayCode == "O_ThreeStar_Zhi_Front2":
            betOn=TZF2(rawBetOn)
        elif betTypePlayCode == "O_ThreeStar_Zhi_Front3":
            betOn=TZF3(rawBetOn)
        elif betTypePlayCode == "O_TwoStar_Zu_Front2":
            betOn=TSZF2(rawBetOn)
        elif betTypePlayCode == "PK10_1":
            betOn=["DWD1_" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_1BS" or betTypePlayCode == "PK10_1DT" or  betTypePlayCode == "PK10_1OE" or betTypePlayCode == "PK10_1PC":
            betOn=[rawBetOn + "1"]
        elif betTypePlayCode == "PK10_2":
            betOn=["DWD2_" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_2BS" or betTypePlayCode == "PK10_2DT" or  betTypePlayCode == "PK10_2OE" or betTypePlayCode == "PK10_2PC":
            betOn=[rawBetOn + "2"]
        elif betTypePlayCode == "PK10_3":
            betOn=["DWD3_" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_3BS" or betTypePlayCode == "PK10_3DT" or  betTypePlayCode == "PK10_3OE" or betTypePlayCode == "PK10_3PC":
            betOn=[rawBetOn + "3"]
        elif betTypePlayCode == "PK10_4":
            betOn=["DWD4_" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_4BS" or betTypePlayCode == "PK10_4DT" or  betTypePlayCode == "PK10_4OE" or betTypePlayCode == "PK10_4PC":
            betOn=[rawBetOn + "4"]
        elif betTypePlayCode == "PK10_5":
            betOn=["DWD5_" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_5BS" or betTypePlayCode == "PK10_5DT" or  betTypePlayCode == "PK10_5OE" or betTypePlayCode == "PK10_5PC":
            betOn=[rawBetOn + "5"]
        elif betTypePlayCode == "PK10_6":
            betOn=["DWD6_" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_6BS" or  betTypePlayCode == "PK10_6OE" or betTypePlayCode == "PK10_6PC":
            betOn=[rawBetOn + "6"]
        elif betTypePlayCode == "PK10_7":
            betOn=["DWD7_" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_7BS" or  betTypePlayCode == "PK10_7OE" or betTypePlayCode == "PK10_7PC":
            betOn=[rawBetOn + "7"]
        elif betTypePlayCode == "PK10_8":
            betOn=["DWD8_" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_8BS" or  betTypePlayCode == "PK10_8OE" or betTypePlayCode == "PK10_8PC":
            betOn=[rawBetOn + "8"]
        elif betTypePlayCode == "PK10_9":
            betOn=["DWD9_" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_9BS" or  betTypePlayCode == "PK10_9OE" or betTypePlayCode == "PK10_9PC":
            betOn=[rawBetOn + "9"]
        elif betTypePlayCode == "PK10_10":
            betOn=["DWD10_" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_10BS" or  betTypePlayCode == "PK10_10OE" or betTypePlayCode == "PK10_10PC":
            betOn=[rawBetOn + "10"]
        elif "PK10_SUM_" in betTypePlayCode:
            betOn=["SUM" + str(int(rawBetOn))]
        elif betTypePlayCode == "PK10_SUMBS" or  betTypePlayCode == "PK10_SUMOE":
            betOn=["SUM" +rawBetOn]

        row_by_amount = []
        row_by_amount_odds = []
        odds_index = 0
        for b in all_betons:
            if b in betOn:
                row_by_amount.append(unitAmount)
                row_by_amount_odds.append((odds[odds_index]-1) * unitAmount)
                odds_index+=1
                total_bet_count += 1
                total_bet_amount += unitAmount
            else:
                row_by_amount.append(0)
                row_by_amount_odds.append(0)

        amount_table.append(row_by_amount)
        amount_with_odds_table.append(row_by_amount_odds)

    logging.info(f"total_bet_count={total_bet_count}, total_bet_amount={total_bet_amount}")
    return (expectId, amount_table, amount_with_odds_table, wager_length)

if __name__ == "__main__":
    global all_betons

    currentPath = os.path.dirname(os.path.abspath(__file__))
    
    if not os.path.exists(f"{currentPath}/log"):
        os.mkdir(f"{currentPath}/log")
    home_path = str(Path.home())
    log_fliename = datetime.datetime.now().strftime(f"{currentPath}/log/opencode-%Y-%m-%d.log")
    print(f"log filename formate = {log_fliename}")
    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            datefmt='%m-%d %H:%M:%S',
            filename=log_fliename)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logging.debug("current path : " + currentPath)


    # 從檔案讀取所有beton
    with open(f"{currentPath}/data/beton_list.txt", 'r') as f:
        all_betons = f.read().split(',') # 讀取檔案內容

    # 從檔案讀取wager json資料
    with open(f"{currentPath}/data/test_wager_data.txt", 'r') as f:
        raw_data = f.read() # 讀取檔案內容
    logging.debug(f"row data: {raw_data}")
    
    # 轉換json wager變成 numnpy array
    (expectId, amount_table, amount_with_odds_table, wager_length) = ConvertWager(raw_data)
    logging.info(f"expectId:{expectId}")

    amount_file = f"{currentPath}/data/beton_amount_{expectId}.csv"
    with open(amount_file, 'w+') as f:
        for a in amount_table:
            strAmountWithComma = ','.join(str(e) for e in a)
            f.write(strAmountWithComma + "\n")
    logging.info(f"output wager total amount file: {amount_file}")

    amount_with_odds_file = f"{currentPath}/data/beton_amount_with_odds_{expectId}.csv"
    with open(amount_with_odds_file, 'w+') as f:
        for a in amount_with_odds_table:
            strAmountWithComma = ','.join(str(e) for e in a)
            f.write(strAmountWithComma + "\n")
    logging.info(f"output wager total amount(with odds) file: {amount_with_odds_file}")
    