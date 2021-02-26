import TransferWager.A5_K3 as A5_K3
import itertools

if __name__ == "__main__":

    with open('k3_beton_list.txt', 'w+', encoding='UTF-8') as f:
        
        (result, length ) = A5_K3.OSumK_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_Sum_K length:{length}")
        
        (result, length ) = A5_K3.OSumBSOEK_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_Sum_BSOE_K length:{length}")

        (result, length ) = A5_K3.OSame3B_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_Same3B length:{length}")

        (result, length ) = A5_K3.OSame3A_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_Same3A length:{length}")
    
        (result, length ) = A5_K3.ODiff3_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_Diff3 length:{length}")

        (result, length ) = A5_K3.OCtn3B_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_Ctn3B length:{length}")

        (result, length ) = A5_K3.OSame2B_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_Same2B length:{length}")

        (result, length ) = A5_K3.OSame2A_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_Same2A length:{length}")

        (result, length ) = A5_K3.ODfif2_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_Diff2 length:{length}")

        (result, length ) = A5_K3.OKUADU_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_KUADU length:{length}")

        (result, length ) = A5_K3.OSIX_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_SIX length:{length}")

        (result, length ) = A5_K3.O3_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_3 length:{length}")

        (result, length ) = A5_K3.K3SUM03_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SUM_03 length:{length}")
    
        (result, length ) = A5_K3.K3SUM04_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SUM_04 length:{length}")

        (result, length ) = A5_K3.K3SUM05_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SUM_05 length:{length}")

        (result, length ) = A5_K3.K3SUM06_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SUM_06 length:{length}")

        (result, length ) = A5_K3.K3SUM07_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SUM_07 length:{length}")

        (result, length ) = A5_K3.K3SUM08_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SUM_08 length:{length}")

        (result, length ) = A5_K3.K3SUM09_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SUM_09 length:{length}")

        (result, length ) = A5_K3.K3SUM10_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SUM_10 length:{length}")

        (result, length ) = A5_K3.K3SUM11_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SUM_11 length:{length}")

        (result, length ) = A5_K3.K3SUM12_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SUM_12 length:{length}")

        (result, length ) = A5_K3.K3SUM13_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SUM_13 length:{length}")

        (result, length ) = A5_K3.K3SUM14_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SUM_14 length:{length}")

        (result, length ) = A5_K3.K3SUM15_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SUM_15 length:{length}")

        (result, length ) = A5_K3.K3SUM16_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SUM_16 length:{length}")

        (result, length ) = A5_K3.K3SUM17_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SUM_17 length:{length}")

        (result, length ) = A5_K3.K3SUM18_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SUM_18 length:{length}")

        (result, length ) = A5_K3.K3SUMBS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SUMBS length:{length}")

        (result, length ) = A5_K3.K3SUMOE_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SUMOE length:{length}")

        (result, length ) = A5_K3.K3OBS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_OBS length:{length}")

        (result, length ) = A5_K3.K3EBS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_EBS length:{length}")
        
        (result, length ) = A5_K3.K3SAME3A_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SAME3A length:{length}")

        (result, length ) = A5_K3.K3SAME3B_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SAME3B length:{length}")

        (result, length ) = A5_K3.K3CTN3A_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_CTN3A length:{length}")

        (result, length ) = A5_K3.K3CTN3B_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_CTN3B length:{length}")

        (result, length ) = A5_K3.K3DIFF3_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_DIFF3 length:{length}")

        (result, length ) = A5_K3.K3SAME2A_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SAME2A length:{length}")

        (result, length ) = A5_K3.K3SAME2B_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SAME2B length:{length}")

        (result, length ) = A5_K3.K3DIFF2_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_DIFF2 length:{length}")

        (result, length ) = A5_K3.K33_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_3 length:{length}")

        (result, length ) = A5_K3.K3SIX_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_SIX length:{length}")

        (result, length ) = A5_K3.K3KUADU_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_KUADU length:{length}")

        (result, length ) = A5_K3.K3BLACKOE_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_BLACKOE length:{length}")

        (result, length ) = A5_K3.K3BLACKBS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_BLACKBS length:{length}")

        (result, length ) = A5_K3.K3REDOE_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_REDOE length:{length}")

        (result, length ) = A5_K3.K3REDBS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_REDBS length:{length}")

        (result, length ) = A5_K3.K3BLACKRED_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"K3_BLACKRED length:{length}")

    with open('k3_opencode_list.txt', 'w+', encoding='UTF-8') as f:
         for (a, b, c) in  itertools.combinations_with_replacement('123456', 3):
            f.write(f"{a},{b},{c}\n")