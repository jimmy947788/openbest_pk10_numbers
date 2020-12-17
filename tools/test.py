import itertools
from posix import PRIO_USER
import TransferWager.A5_SSC as A5_SSC
from collections import Counter

def split(word): 
    return [char for char in word]  

if __name__ == "__main__":
    with open(f"/home/matrix/openbest_pk10_numbers/data/opencode_ssc_table.csv") as f:
        line = f.readline()
        print(line)
        print(len(line.split(',')))