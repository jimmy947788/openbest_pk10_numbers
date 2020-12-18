import itertools
from posix import PRIO_USER
import TransferWager.A5_SSC as A5_SSC
from collections import Counter

def split(word): 
    return [char for char in word]  

if __name__ == "__main__":
    opencode_header = "opencode,"
    with open(f"/home/matrix/openbest_pk10_numbers/data/ssc_opencode_table_1.csv") as f:
        header = f.readline()

    with open('/home/matrix/openbest_pk10_numbers/data/ssc_beton_list.csv', 'w+', encoding='UTF-8') as f:
        temp_header = header.replace(opencode_header, "")
        temp_header_len = len(temp_header)
        f.write(temp_header[:temp_header_len-1]) #移除最後一個逗號
    
    