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
    with open('opencode_table.csv', 'w+',  encoding='UTF-8') as the_file:
        if hasHeader==True:
            the_file.write(u"開獎號碼,")

            # 1-10定位
            for pos in all_balls:
                for ball in all_balls:
                    the_file.write(u"DWD"+ str(pos) + "_" + str(ball)+",")
            
            # 前三直選
            for balls in list(itertools.permutations(all_balls, 3)):
                str1 = '-'.join(str(e) for e in balls)
                the_file.write(u"TZF3_" + str1 + ",")

            # 前二直選
            for balls in list(itertools.permutations(all_balls, 2)):
                str1 = '-'.join(str(e) for e in balls)
                the_file.write(u"TZF2_" + str1 + ",")

            # 前一直選
            for ball in all_balls:
                the_file.write(u"TZF1_" + str(ball) + ",")

            # 1-10大
            for pos in range(1, 11):
                the_file.write(u"B" + str(pos) + ",") 
            
            # 1-10小
            for pos in range(1, 11):
                the_file.write(u"S" + str(pos) + ",")

            # 1-10單
            for pos in range(1, 11):
                the_file.write(u"O" + str(pos) + ",")

            # 1-10雙
            for pos in range(1, 11):
                the_file.write(u"E" + str(pos) + ",")

            # 1-10質
            for pos in range(1, 11):
                the_file.write(u"P" + str(pos) + ",")
            
            # 1-10合
            for pos in range(1, 11):
                the_file.write(u"C" + str(pos) + ",")

            the_file.write(u"D1,") #冠軍龍
            the_file.write(u"D2,") #亞軍龍
            the_file.write(u"D3,") #季軍龍
            the_file.write(u"D4,") #第四名龍
            the_file.write(u"D5,") #第五名龍
            the_file.write(u"T1,") #冠軍虎
            the_file.write(u"T2,") #亞軍虎
            the_file.write(u"T3,") #季軍虎
            the_file.write(u"T4,") #第四名虎
            the_file.write(u"T5,") #第五名虎

            # 冠亞合
            for sum in range(3, 20):
                the_file.write(u"SUM" + str(sum) + ",")
            the_file.write(u"SUMB,")  # 冠亞合大
            the_file.write(u"SUMS,")  # 冠亞合小
            the_file.write(u"SUMO,") # 冠亞合單
            the_file.write(u"SUME,")  # 冠亞合雙

            # 冠亞組合
            for balls in list(itertools.combinations(all_balls, 2)):
                str1 = '-'.join(str(e) for e in balls)
                the_file.write(u"TSZF2_"+ str(str1)+",")
                
            the_file.write('\n')

        #for balls in ballsList[:5000]: 
        for balls in ballsList: # ALL
            print(balls)
            if hasHeader==True:
                str1 = '-'.join(str(e) for e in balls)
                print(str1)
                the_file.write(str1 + ',')

            # 定位膽
            for pos in range(1, 11):
                for num in range(1, 11):
                    the_file.write(str(O_DingWeiDan(balls, pos, num))+ ',')
           
            # 前三直選
            for num in list(itertools.permutations(all_balls, 3)):
                the_file.write( str(O_ThreeStar_Zhi_Front3(balls, num)) + ',')

            # 前二直選
            for num in  list(itertools.permutations(all_balls, 2)):
                the_file.write( str(O_ThreeStar_Zhi_Front2(balls, num)) + ',')

            # 前一直選
            for num in  all_balls:
                the_file.write( str(O_ThreeStar_Zhi_Front1(balls, num)) + ',')

            # 1-10 大
            for pos in range(1, 11):
                the_file.write( str(O_B(balls, pos)) + ',')

            # 1-10 小
            for pos in range(1, 11):
                the_file.write( str(O_S(balls, pos)) + ',')
            
            # 1-10 單
            for pos in range(1, 11):
                the_file.write( str(O_E(balls, pos)) + ',')
    
            # 1-10 雙
            for pos in range(1, 11):
                the_file.write( str(O_O(balls, pos)) + ',')

            # 1-10 質
            for pos in range(1, 11):
                the_file.write( str(O_P(balls, pos)) + ',')

            # 1-10 合
            for pos in range(1, 11):
                the_file.write( str(O_C(balls, pos)) + ',')

            # 冠军龙
            the_file.write(str(O_Dragon1(balls))+ ',')
            # 亚军龙
            the_file.write(str(O_Dragon2(balls))+ ',')
            # 季军龙
            the_file.write(str(O_Dragon3(balls))+ ',')
            # 第四名龙
            the_file.write(str(O_Dragon4(balls))+ ',')
            # 第五名龙
            the_file.write(str(O_Dragon5(balls))+ ',')
            # 冠军虎
            the_file.write(str(O_Tiger1(balls))+ ',')
            # 亚军虎
            the_file.write(str(O_Tiger2(balls))+ ',')
            # 季军虎
            the_file.write(str(O_Tiger3(balls))+ ',')
            # 第四名虎
            the_file.write(str(O_Tiger4(balls))+ ',')
            # 第五名虎
            the_file.write(str(O_Tiger5(balls))+ ',')

            # 冠亚和
            for sum in range(3, 20):
                the_file.write( str(O_12Sum(balls, sum))+ ',')

            # 冠亚和大
            the_file.write(str(O_12Sum_B(balls))+ ',')
            # 冠亚和小
            the_file.write(str(O_12Sum_S(balls))+ ',')
            # 冠亚和單
            the_file.write(str(O_12Sum_O(balls))+ ',')
            # 冠亚和雙
            the_file.write(str(O_12Sum_E(balls))+ ',')

            # 冠亞組合
            for num in  list(itertools.combinations(all_balls, 2)):
                the_file.write(str(O_TwoStar_Zu_Front2(balls, num))+ ',')

            the_file.write('\n')

if __name__ == '__main__':
    main()
    