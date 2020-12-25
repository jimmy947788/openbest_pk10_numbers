import itertools
from collections import Counter
import time
import logging
import sys
import json

def split(word): 
    return [char for char in word]  

if __name__ == "__main__":
    """
    opencode_header = "opencode,"
    with open(f"/home/matrix/openbest_pk10_numbers/data/ssc_opencode_table_1.csv") as f:
        header = f.readline()

    with open('/home/matrix/openbest_pk10_numbers/data/ssc_beton_list.csv', 'w+', encoding='UTF-8') as f:
        temp_header = header.replace(opencode_header, "")
        temp_header_len = len(temp_header)
        f.write(temp_header[:temp_header_len-1]) #移除最後一個逗號
    """
    """
    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            datefmt='%m-%d %H:%M:%S',
            filename="../log/test.log")
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    """

    with open('ssc_opencode_list.txt', 'w+', encoding='UTF-8') as f:
        for (a, b, c, d, e) in  itertools.product('0123456789', repeat = 5):
            f.write(f"{a},{b},{c},{d},{e}\n")