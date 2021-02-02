import TransferWager.A5_PC28 as A5_PC28
import itertools

if __name__ == "__main__":

    with open('pc28_beton_list.txt', 'w+', encoding='UTF-8') as f:
        # O_FiveStar_ZhiFu 五星直選
        (result, length ) = A5_PC28.OSumP_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_Sum_P length:{length}")

        (result, length ) = A5_PC28.OSumBSOEP_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_Sum_BSOE_P length:{length}")

        (result, length ) = A5_PC28.OSumSpecial_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_Sum_Special length:{length}")

        (result, length ) = A5_PC28.OSpecial_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_Special length:{length}")

        (result, length ) = A5_PC28.ODragonTigerP_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_DragonTiger_P length:{length}")

        (result, length ) = A5_PC28.OCOLORPC28_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_COLOR_PC28 length:{length}")

        (result, length ) = A5_PC28.PC28SUM01_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_COLOR_PC28 length:{length}")
        

    with open('pc28_opencode_list.txt', 'w+', encoding='UTF-8') as f:
        for (a, b, c) in  itertools.permutations([1, 2, 3, 4, 5, 6, 7, 8, 9], 3):
            f.write(f"{a},{b},{c}\n")