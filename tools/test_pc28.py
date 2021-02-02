import itertools
from logging import NullHandler
import random
from random import sample
import time
import datetime

def ttttt():
    try:
        start_rand = random.randrange(1, 20)
        end_rand = random.randrange(20, 50)
        #print(f"start_rand={start_rand}, end_rand={end_rand}")
        return random.sample(range(start_rand, end_rand), 6)
    except:
        return None

if __name__ == '__main__':
    now = datetime.datetime.now()
    random.seed(now.microsecond)

    for i in range(10000):
        tmp = None
        while tmp == None:
            try:
                tmp = ttttt()
                s = str(sum(tmp))
                last_digit = s[-1:]
                #print(f"s={s}, last digit={last_digit}")
                if last_digit == '7':
                    break
            except:
                tmp = None
        
        tmp.sort()
        print(tmp)