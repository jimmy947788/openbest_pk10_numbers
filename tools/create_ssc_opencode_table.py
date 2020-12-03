import itertools
import pandas as pd
from argparse import ArgumentParser
import re
import os

def O_BSOE_S(opencode, pos, beton):
    if beton == "B":
        return 1 if int(opencode[pos]) in BIG else -1
    if beton == "S":
        return 1 if int(opencode[pos]) in SMALL else -1
    if beton == "O":
        return 1 if int(opencode[pos]) in ODD else -1
    if beton == "E":
        return 1 if int(opencode[pos]) in EVEN else -1

def O_DingWeiDan_S(opencode, pos, beton):
    return 1 if int(opencode[pos]) == beton else -1

def O_DragonTiger(opencode, pos1, pos2 , beton):
    if beton == "D":
        return 1 if int(opencode[pos1]) > int(opencode[pos2]) else -1
    if beton == "T":
        return 1 if int(opencode[pos1]) < int(opencode[pos2]) else -1
    if beton == "TT":
        return 1 if int(opencode[pos1]) == int(opencode[pos2]) else -1

def O_FiveStar_ZhiFu(opencode, beton):
    return 1 if opencode == beton else -1

ALL_BALLS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
BIG = [ 5, 6, 7, 8, 9 ]
SMALL = [ 0, 1, 2, 3, 4 ]
ODD = [1, 3, 5, 7, 9]
EVEN = [0, 2, 4, 6, 8]

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
        # O_BSOE_S 大小单双
        for betOn in ['B', 'S', 'O', 'E']:
            for pos in range(5):
                header += f"O_BSOE_S_{pos+1}{betOn},"

        # O_DingWeiDan_S
        for betOn in ALL_BALLS:
            for pos in range(5):
                header +=  f"O_DingWeiDan_S_{pos+1}{betOn},"

        # O_DragonTiger 龙虎
        for betOn in [ "D", "T", "TT"]:
            for (pos1, pos2) in [ (0, 1), (0, 2), (0, 3), (0, 4),  (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]:
                header += f"O_DragonTiger_{pos1+1}{pos2+1}{betOn},"

        #  O_FiveStar_ZhiFu	五星直选复式
        # O_FiveStar_ZhiDan	五星直选单式
        for a1 in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                for a2 in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    for a3 in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                        for a4 in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                            for a5 in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                                s = [a1, a2, a3, a4, a5]
                                header += f"O_FiveStar_ZhiFu_{a1}{a2}{a3}{a4}{a5},"
        """
        for (a, b, c, d, e) in itertools.product('0123456789', repeat = 5):
            header += f"O_FiveStar_ZhiFu_{a}{b}{c}{d}{e},"

        f.write(header+ '\n')

        # line
        #====================================================================================
        for (a, b, c, d, e) in itertools.product('0123456789', repeat = 5):
        #for opencode in itertools.product('01', repeat = 5):
            opencode = f"{a}-{b}-{c}-{d}-{e}"
            print(opencode)
            line = opencode +","
            
            for (a1, b1, c1, d1, e1) in itertools.product('0123456789', repeat = 5):
                line +=  str(O_FiveStar_ZhiFu(opencode,  f"{a1}-{b1}-{c1}-{d1}-{e1}")) + ","
            
            f.write(line+ '\n')
        """
            # O_BSOE_S 大小单双
            for betOn in ['B', 'S', 'O', 'E']:
                for pos in range(5):
                    line += str(O_BSOE_S(opencode, pos, betOn)) + ","
            
            # O_DingWeiDan_S
            for betOn in ALL_BALLS:
                for pos in range(5):
                    line += str(O_DingWeiDan_S(opencode, pos, betOn)) + ","

            # O_DragonTiger 龙虎
            for betOn in [ "D", "T", "TT"]:
                for (pos1, pos2) in [ (0, 1), (0, 2), (0, 3), (0, 4),  (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]:
                    line += str(O_DragonTiger(opencode, pos1, pos2, betOn)) + ","
            
            for a1 in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                for a2 in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    for a3 in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                        for a4 in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                            for a5 in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                                s = ( f"{a1}", f"{a2}", f"{a3}", f"{a4}", f"{a5}")
                                #print(f"{opencode} x {s}={O_FiveStar_ZhiFu(opencode, s)}")
                                line += str(O_FiveStar_ZhiFu(opencode, s)) + ","

            # O_FiveStar_Zu120
            " ""
            O_FiveStar_Zu120	五星组选120
            O_FiveStar_Zu60	五星组选60
            O_FiveStar_Zu30	五星组选30
            O_FiveStar_Zu20	五星组选20
            O_FiveStar_Zu10	五星组选10
            O_FiveStar_Zu5	五星组选5

            O_FiveStar_SpecialOne	一帆风顺
            O_FiveStar_SpecialTwo	好事成双
            O_FiveStar_SpecialThree	三星报喜
            O_FiveStar_SpecialFour	四季发财
            " ""

            " ""
            O_FourStar_ZhiFu	四星直选复式
            O_FourStar_ZhiDan	四星直选单式

            O_FourStar_Zu24 四星组选24
            O_FourStar_Zu12 四星组选12
            O_FourStar_Zu6 四星组选6
            O_FourStar_Zu4 四星组选4
            " ""

            " ""
            O_ThreeStar_Zhi_Front3_S	前三直选
            O_ThreeStar_Zhi_Last3_S	后三直选
            O_ThreeStar_Zhi_Middle3_S	中三直选

            O_ThreeStar_Zu_Front3_S	前三组选
            O_ThreeStar_Zu_Last3_S	后三组选
            O_ThreeStar_Zu_Middle3_S	中三组选

            O_ThreeStar_Special_Front3	前三特殊号
            O_ThreeStar_Special_Last3	后三特殊号
            O_ThreeStar_Special_Middle3	中三特殊号
            " ""
            " ""
            O_TwoStar_Zhi_wq	万千直选
            O_TwoStar_Zhi_wb	万百直选
            O_TwoStar_Zhi_ws	万拾直选
            O_TwoStar_Zhi_wg	万个直选
            O_TwoStar_Zhi_qb	千百直选
            O_TwoStar_Zhi_qs	千拾直选
            O_TwoStar_Zhi_qg	千个直选
            O_TwoStar_Zhi_bs	百拾直选
            O_TwoStar_Zhi_bg	百个直选
            O_TwoStar_Zhi_sg	拾个直选
            
            O_TwoStar_Zu_bg	百个组选
            O_TwoStar_Zu_bs	百拾组选
            O_TwoStar_Zu_qb	千百组选
            O_TwoStar_Zu_qg	千个组选
            O_TwoStar_Zu_qs	千拾组选
            O_TwoStar_Zu_sg	拾个组选
            O_TwoStar_Zu_wb	万百组选
            O_TwoStar_Zu_wg	万个组选
            O_TwoStar_Zu_wq	万千组选
            O_TwoStar_Zu_ws	万拾组选
            """
            #print (f"opencode={opencode}")
            #f.write(line+ '\n')

    #print(rows)
if __name__ == '__main__':
    main()
    