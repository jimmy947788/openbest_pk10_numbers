# 1 2 3 4 5 6 7 8 9 10,
# 1 2 3 4 5 6 7 8 9 10,
# 6 7 8 9 10,
# 1 2 3 4 5,
# 1 3 5 7 9,
# 1 3 5 7 9,
# 1 3 5 7 9,
# 2 4 6 8 10,
# 2 4 6 8 10,
# 2 4 6 8 10
import itertools

def SUM(rawBetOn):
    betOn=[]
    for b in rawBetOn.split(' '):
        betOn.append(f"SUM{b}")
    return betOn

def TSZF2(rawBetOn):
    betOn=[]
    for b in  list(itertools.combinations(rawBetOn.split(' '), 2)):
        str1 = '-'.join(str(e) for e in b)
        betOn.append("TSZF2_" + str1)
    return betOn

def DT(rawBetOn):
    betOn=[]
    pos = 1
    for beton_pos in rawBetOn.split(','):
        for beton in beton_pos.split(' '):
            betOn.append(f"{beton}{pos}")
        pos+=1
    return betOn

def BSOE(rawBetOn):
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

def DWD(rawBetOn):
    betOn=[]
    pos = 1
    for num_pos in rawBetOn.split(','):
        for num in num_pos.split(' '):
            betOn.append(f"DWD{pos}_{num}")
        pos+=1

    return betOn

if __name__ == '__main__':
    #print(DWD("1 2 3 4 5 6 7 8 9 10,1 2 3 4 5 6 7 8 9 10,6 7 8 9 10,1 2 3 4 5,1 3 5 7 9,1 3 5 7 9,1 3 5 7 9,2 4 6 8 10,2 4 6 8 10,2 4 6 8 10"))
    #list =TZF3("6 7 8 9 10,1 2 3 4 5,1 3 5 7 9") 
    #list =TZF2("1 2 3 4 5,1 3 5 7 9") 
    #list =TZF1("1 3 6 8 10") 
    #list = BSOE("E,B O,S,S,O,E,B O E,B S E,B O E,B O E")
    #list = DT("T,D,D T,D T,D T")
    #list = SUM("4 5 6 8 10 11 12 13 14 15 17 18 19")
    #list = TSZF2("1 2 3 4 5 6 7 8 9 10")
    list = SUM("4 5 6 8 10 11 12 13 14 15 17 18 19")
    print(list)
    print(len(list))
    