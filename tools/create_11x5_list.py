import TransferWager.A5_11x5 as A5_11x5
import itertools

if __name__ == "__main__":

    with open('11x5_beton_list.txt', 'w+', encoding='UTF-8') as f:
        # O_FiveStar_ZhiFu 五星直選
        (result, length ) = A5_11x5.OThreeStarZhiFront3X_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_ThreeStar_Zhi_Front3_X length:{length}")

        # O_FiveStar_ZhiFu 五星直選
        (result, length ) = A5_11x5.OThreeStarZhiMiddle3X_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_ThreeStar_Zhi_Middle3_X length:{length}")

        (result, length ) = A5_11x5.OThreeStarZhiLast3X_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_ThreeStar_Zhi_Last3_X length:{length}")

        (result, length ) = A5_11x5.OThreeStarZuFront3X_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_ThreeStar_Zu_Front3_X length:{length}")

        (result, length ) = A5_11x5.OThreeStarZuMiddle3X_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_ThreeStar_Zu_Middle3_X length:{length}")

        (result, length ) = A5_11x5.OThreeStarZuLast3X_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_ThreeStar_Zu_Last3_X length:{length}")

        (result, length ) = A5_11x5.OTwoStarZhi12_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zhi_12 length:{length}")
        
        (result, length ) = A5_11x5.OTwoStarZu12_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zu_12 length:{length}")

        (result, length ) = A5_11x5.OTwoStarAny1_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Any_1 length:{length}")

        (result, length ) = A5_11x5.OTwoStarAny2_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Any_2 length:{length}")

        (result, length ) = A5_11x5.OTwoStarAny3_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Any_3 length:{length}")

        (result, length ) = A5_11x5.OTwoStarAny4_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Any_4 length:{length}")

        (result, length ) = A5_11x5.OTwoStarAny5_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Any_5 length:{length}")

        (result, length ) = A5_11x5.OTwoStarAny6_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Any_6 length:{length}")

        (result, length ) = A5_11x5.OTwoStarAny7_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Any_7 length:{length}")

        (result, length ) = A5_11x5.OTwoStarAny8_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Any_8 length:{length}")

        (result, length ) = A5_11x5.ODingWeiDanX_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_DingWeiDan_X length:{length}")
        
        (result, length ) = A5_11x5.OBSOEX_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_BSOE_X length:{length}")

        (result, length ) = A5_11x5.OSumBSOEX_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_Sum_BSOE_X length:{length}")

        (result, length ) = A5_11x5.X11X51_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"X11X5_1 length:{length}")

        (result, length ) = A5_11x5.X11X52_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"X11X5_2 length:{length}")

        (result, length ) = A5_11x5.X11X53_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"X11X5_3 length:{length}")

        (result, length ) = A5_11x5.X11X54_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"X11X5_4 length:{length}")

        (result, length ) = A5_11x5.X11X55_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"X11X5_5 length:{length}")

        (result, length ) = A5_11x5.X11X51ON1_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"X11X5_1ON1 length:{length}")

        (result, length ) = A5_11x5.X11X5SUMBS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"X11X5_SUMBS length:{length}")

        (result, length ) = A5_11x5.X11X5SUMOE_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"X11X5_SUMOE length:{length}")

        (result, length ) = A5_11x5.X11X5TAILBS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"X11X5_TAILBS length:{length}")

        (result, length ) = A5_11x5.X11X5DT_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"X11X5_DT length:{length}")

        (result, length ) = A5_11x5.X11X51BS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"X11X5_1BS length:{length}")

        (result, length ) = A5_11x5.X11X51OE_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"X11X5_1OE length:{length}")

        (result, length ) = A5_11x5.X11X52BS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"X11X5_2BS length:{length}")

        (result, length ) = A5_11x5.X11X52OE_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"X11X5_2OE length:{length}")

        (result, length ) = A5_11x5.X11X53BS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"X11X5_3BS length:{length}")

        (result, length ) = A5_11x5.X11X53OE_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"X11X5_3OE length:{length}")

        (result, length ) = A5_11x5.X11X54BS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"X11X5_4BS length:{length}")

        (result, length ) = A5_11x5.X11X54OE_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"X11X5_4OE length:{length}")

        (result, length ) = A5_11x5.X11X55BS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"X11X5_5BS length:{length}")

        (result, length ) = A5_11x5.X11X55OE_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"X11X5_5OE length:{length}")

    with open('11x5_opencode_list.txt', 'w+', encoding='UTF-8') as f:
        for (a, b, c, d, e) in  itertools.permutations([1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11], 5):
            f.write(f"{a},{b},{c},{d},{e}\n")