import itertools
from collections import Counter
import time
import logging
import sys
import json
import TransferWager.A5_SSC as A5_SSC

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
    """
    with open('ssc_opencode_list.txt', 'w+', encoding='UTF-8') as f:
        for (a, b, c, d, e) in  itertools.product('0123456789', repeat = 5):
            f.write(f"{a},{b},{c},{d},{e}\n")
    """

    """
    (result, length) =  A5_SSC.SSC1_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSC2_Beton()
    for beton in result:
        print(beton)

    (result, length) =  A5_SSC.SSC3_Beton()
    for beton in result:
        print(beton)

    (result, length) =  A5_SSC.SSC4_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSC5_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCD1T2_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCD1T3_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCD1T5_Beton()
    for beton in result:
        print(beton)

    (result, length) =  A5_SSC.SSCD2T3_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCD2T4_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCD2T5_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCD3T4_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCD3T5_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCD4T5_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCTIE12_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCTIE13_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCTIE14_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCTIE15_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCTIE23_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCTIE24_Beton()
    for beton in result:
        print(beton)

    (result, length) =  A5_SSC.SSCTIE25_Beton()
    for beton in result:
        print(beton)

    (result, length) =  A5_SSC.SSCTIE34_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCTIE35_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCTIE45_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSC1BS_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSC2BS_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSC3BS_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSC4BS_Beton()
    for beton in result:
        print(beton)

    (result, length) =  A5_SSC.SSC5BS_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSC1OE_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSC2OE_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSC3OE_Beton()
    for beton in result:
        print(beton)

    (result, length) =  A5_SSC.SSC4OE_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSC5OE_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCF3CTN_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCF3HALF_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCF3LEOPARD_Beton()
    for beton in result:
        print(beton)

    (result, length) =  A5_SSC.SSCF3PAIR_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCF3SIX_Beton()
    for beton in result:
        print(beton)
    
    #
    (result, length) =  A5_SSC.SSCM3CTN_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCM3HALF_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCM3LEOPARD_Beton()
    for beton in result:
        print(beton)

    (result, length) =  A5_SSC.SSCM3PAIR_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCM3SIX_Beton()
    for beton in result:
        print(beton)
    #
    (result, length) =  A5_SSC.SSCL3CTN_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCL3HALF_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCL3LEOPARD_Beton()
    for beton in result:
        print(beton)

    (result, length) =  A5_SSC.SSCL3PAIR_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCL3SIX_Beton()
    for beton in result:
        print(beton)

    (result, length) =  A5_SSC.SSCSINGLE_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCPAIR_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCTHREE_Beton()
    for beton in result:
        print(beton)
    
    (result, length) =  A5_SSC.SSCFOUR_Beton()
    for beton in result:
        print(beton)
"""
    print("1=================================")
    (result, length) =  A5_SSC.OFiveStarZu20_Beton("5,3 7")
    for beton in result:
        print(f">==={beton}")
    
    print("2=================================")
    (result, length) =  A5_SSC.OFiveStarZu20_Beton("0,1 2 3")
    for beton in result:
        print(f">==={beton}")

    print("3=================================")
    (result, length) =  A5_SSC.OFiveStarZu20_Beton("7 8 9,4 5")
    for beton in result:
        print(f">==={beton}")
    
    print("4=================================")
    (result, length) =  A5_SSC.OFiveStarZu20_Beton("0 4,1 3")
    for beton in result:
        print(f">==={beton}")


