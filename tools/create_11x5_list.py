import TransferWager.A5_11x5 as A5_11x5
import itertools

if __name__ == "__main__":

    with open('11x5_beton_list.txt', 'w+', encoding='UTF-8') as f:

        # O_FiveStar_ZhiFu 五星直選
        (result, length ) = A5_11x5.OThreeStarZhiFront3X_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_ThreeStar_Zhi_Front3_X length:{length}")

        
    with open('11x5_opencode_list.txt', 'w+', encoding='UTF-8') as f:
        for (a, b, c, d, e) in  itertools.permutations([1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11], 5):
            f.write(f"{a},{b},{c},{d},{e}\n")