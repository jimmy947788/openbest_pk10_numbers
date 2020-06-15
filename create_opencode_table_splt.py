import itertools
import pandas as pd
from argparse import ArgumentParser


def O_DingWeiDan(balls, pos, num):
    return 1 if balls[pos -1] == num else -1

def O_ThreeStar_Zhi_Front3(balls, num):
    return 1 if (balls[0] == num[0] and balls[1] == num[1] and balls[2] == num[2])  else -1

def O_ThreeStar_Zhi_Front2(balls, num):
    return 1 if (balls[0] == num[0] and balls[1] == num[1])  else -1

def O_ThreeStar_Zhi_Front1(balls, num):
    return 1 if balls[0] == num else -1

def O_B(balls, pos):
    return 1 if balls[pos -1] >=6  else -1

def O_S(balls, pos):
    return 1 if balls[pos -1] < 6  else -1

def O_O(balls, pos):
    return 1 if  (balls[pos -1] % 2) != 0  else -1

def O_E(balls, pos):
    return 1 if  (balls[pos -1] % 2) == 0  else -1

def O_P(balls, pos):
    return 1 if  (balls[pos -1] in [ 1, 2, 3, 5, 7]) == 0  else -1

def O_C(balls, pos):
    return 1 if  (balls[pos -1] in [ 4, 6, 8, 9, 10]) == 0  else -1

def O_Dragon1(balls):
    return 1 if balls[0] > balls[9]  else -1

def O_Dragon2(balls):
    return 1 if balls[1] > balls[8]  else -1

def O_Dragon3(balls):
    return 1 if balls[2] > balls[7]  else -1

def O_Dragon4(balls):
    return 1 if balls[3] > balls[6]  else -1

def O_Dragon5(balls):
    return 1 if balls[4] > balls[5]  else -1

def O_Tiger1(balls):
    return 1 if balls[0] < balls[9]  else -1

def O_Tiger2(balls):
    return 1 if balls[1] < balls[8]  else -1

def O_Tiger3(balls):
    return 1 if balls[2] < balls[7]  else -1

def O_Tiger4(balls):
    return 1 if balls[3] < balls[6]  else -1

def O_Tiger5(balls):
    return 1 if balls[4] < balls[5]  else -1

def O_12Sum(balls, num):
    return 1 if (balls[0] + balls[1])  == num else -1

def O_12Sum_B(balls):
    return 1 if (balls[0] + balls[1] ) > 11  else -1

def O_12Sum_S(balls):
    return 1 if (balls[0] + balls[1] ) <= 11  else -1

def O_12Sum_O(balls):
    return 1 if  ((balls[0] + balls[1] ) % 2) != 0  else -1

def O_12Sum_E(balls):
    return 1 if  ((balls[0] + balls[1] ) % 2) == 0  else -1

def O_TwoStar_Zu_Front2(balls, num):
    result1 = balls[0] == num[0] and  balls[1] == num[1] 
    result2 = balls[0] == num[1] and  balls[1] == num[0] 
    return 1 if ( result1 or result2 ) else -1

def main():
    parser = ArgumentParser()
    parser.add_argument("--header", help="optional argument", dest="header", default=False)
    args = parser.parse_args()
    hasHeader = bool(args.header)
    print("header arg:", hasHeader)

    all_balls = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ballsList = list(itertools.permutations(all_balls, 10))
    
    ftable = None
    ftable1 =  open('opencode_table_1.csv', 'w+',  encoding='UTF-8')
    ftable2 =  open('opencode_table_2.csv', 'w+',  encoding='UTF-8')
    ftable3 =  open('opencode_table_3.csv', 'w+',  encoding='UTF-8')
    ftable4 =  open('opencode_table_4.csv', 'w+',  encoding='UTF-8')
    ftable5 =  open('opencode_table_5.csv', 'w+',  encoding='UTF-8')

    #for balls in ballsList[:5000]: 
    for balls in ballsList: # ALL
        print(balls)
        if balls[0] == 1 or  balls[0] == 2:
            ftable = ftable1
        elif balls[0] == 3 or balls[0] == 4:
            ftable1.close
            ftable = ftable2
        elif balls[0] == 5 or balls[0] == 6:
            ftable2.close
            ftable = ftable3
        elif balls[0] == 7 or  balls[0] == 8:
            ftable3.close
            ftable = ftable4
        elif balls[0] == 9 or  balls[0] == 10:
            ftable4.close
            ftable = ftable5

        # 定位膽
        for pos in range(1, 11):
            for num in range(1, 11):
                ftable.write(str(O_DingWeiDan(balls, pos, num))+ ',')
        
        # 前三直選
        for num in list(itertools.permutations(all_balls, 3)):
            ftable.write( str(O_ThreeStar_Zhi_Front3(balls, num)) + ',')

        # 前二直選
        for num in  list(itertools.permutations(all_balls, 2)):
            ftable.write( str(O_ThreeStar_Zhi_Front2(balls, num)) + ',')

        # 前一直選
        for num in  all_balls:
            ftable.write( str(O_ThreeStar_Zhi_Front1(balls, num)) + ',')

        # 1-10 大
        for pos in range(1, 11):
            ftable.write( str(O_B(balls, pos)) + ',')

        # 1-10 小
        for pos in range(1, 11):
            ftable.write( str(O_S(balls, pos)) + ',')
        
        # 1-10 單
        for pos in range(1, 11):
            ftable.write( str(O_E(balls, pos)) + ',')

        # 1-10 雙
        for pos in range(1, 11):
            ftable.write( str(O_O(balls, pos)) + ',')

        # 1-10 質
        for pos in range(1, 11):
            ftable.write( str(O_P(balls, pos)) + ',')

        # 1-10 合
        for pos in range(1, 11):
            ftable.write( str(O_C(balls, pos)) + ',')

        # 冠军龙
        ftable.write(str(O_Dragon1(balls))+ ',')
        # 亚军龙
        ftable.write(str(O_Dragon2(balls))+ ',')
        # 季军龙
        ftable.write(str(O_Dragon3(balls))+ ',')
        # 第四名龙
        ftable.write(str(O_Dragon4(balls))+ ',')
        # 第五名龙
        ftable.write(str(O_Dragon5(balls))+ ',')
        # 冠军虎
        ftable.write(str(O_Tiger1(balls))+ ',')
        # 亚军虎
        ftable.write(str(O_Tiger2(balls))+ ',')
        # 季军虎
        ftable.write(str(O_Tiger3(balls))+ ',')
        # 第四名虎
        ftable.write(str(O_Tiger4(balls))+ ',')
        # 第五名虎
        ftable.write(str(O_Tiger5(balls))+ ',')

        # 冠亚和
        for sum in range(3, 20):
            ftable.write( str(O_12Sum(balls, sum))+ ',')

        # 冠亚和大
        ftable.write(str(O_12Sum_B(balls))+ ',')
        # 冠亚和小
        ftable.write(str(O_12Sum_S(balls))+ ',')
        # 冠亚和單
        ftable.write(str(O_12Sum_O(balls))+ ',')
        # 冠亚和雙
        ftable.write(str(O_12Sum_E(balls))+ ',')

        # 冠亞組合
        for num in  list(itertools.combinations(all_balls, 2)):
            ftable.write(str(O_TwoStar_Zu_Front2(balls, num))+ ',')

        ftable.write('\n')

    ftable5.close()

if __name__ == '__main__':
    main()
    