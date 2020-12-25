import TransferWager.A5_SSC as A5_SSC
import itertools

if __name__ == "__main__":
    with open('ssc_beton_list.txt', 'w+', encoding='UTF-8') as f:

        # O_FiveStar_ZhiFu 五星直選
        (result, length ) = A5_SSC.OFiveStarZhiFu_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_FiveStar_ZhiFu length:{length}")

        # O_FiveStar_Zu120 五星組選120
        (result, length )= A5_SSC.OFiveStarZu120_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_FiveStar_Zu120 length:{length}")

        # O_FiveStar_Zu60 五星組選60
        (result, length) = A5_SSC.OFiveStarZu60_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_FiveStar_Zu60 length:{length}")

        # O_FiveStar_Zu30 五星組選30
        (result, length) = A5_SSC.OFiveStarZu30_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_FiveStar_Zu30 length:{length}")

        # O_FiveStar_Zu20 五星組選20
        (result, length) = A5_SSC.OFiveStarZu20_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_FiveStar_Zu20 length:{length}")

            # O_FiveStar_Zu10 五星組選10
        (result, length) = A5_SSC.OFiveStarZu10_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_FiveStar_Zu10 length:{length}")

        # O_FiveStar_Zu5 五星組選5
        (result, length) = A5_SSC.OFiveStarZu5_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_FiveStar_Zu5 length:{length}")

        # O_FiveStar_SpecialOne 一帆风顺
        (result, length) = A5_SSC.OFiveStarSpecialOne_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_FiveStar_SpecialOne length:{length}")

        # O_FiveStar_SpecialTwo 好事成雙
        (result, length) = A5_SSC.OFiveStarSpecialTwo_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_FiveStar_SpecialTwo length:{length}")
        
        # O_FiveStar_SpecialTwo 三星報喜
        (result, length) = A5_SSC.OFiveStarSpecialThree_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_FiveStar_SpecialThree length:{length}")

        # O_FiveStar_SpecialTwo 四季發財
        (result, length) = A5_SSC.OFiveStarSpecialFour_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_FiveStar_SpecialFour length:{length}")

        # O_FourStar_ZhiFu 四星直選
        (result, length) = A5_SSC.OFourStarZhiFu_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_FourStar_ZhiFu length:{length}")

        # O_FourStar_Zu24 四星組選24
        (result, length) = A5_SSC.OFourStarZu24_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_FourStar_Zu24 length:{length}")

        # O_FourStar_Zu12 四星組選12
        (result, length) = A5_SSC.OFourStarZu12_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_FourStar_Zu12 length:{length}")

        # O_FourStar_Zu6 四星組選6
        (result, length) = A5_SSC.OFourStarZu6_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_FourStar_Zu6 length:{length}")

        # O_FourStar_Zu4 四星組選4
        (result, length) = A5_SSC.OFourStarZu4_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_FourStar_Zu4 length:{length}")

        # O_ThreeStar_Zhi_Front3_S  三位直選前三
        (result, length) = A5_SSC.OThreeStarZhiFront3S_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_ThreeStar_Zhi_Front3_S length:{length}")

        # O_ThreeStar_Zhi_Front3_S  三位直選中三
        (result, length) = A5_SSC.OThreeStarZhiMiddle3S_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_ThreeStar_Zhi_Middle3_S length:{length}")

        # O_ThreeStar_Zhi_Last3_S  三位直選後三
        (result, length) = A5_SSC.OThreeStarZhiLast3S_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_ThreeStar_Zhi_Last3_S length:{length}")

        # O_ThreeStar_Zu_Front3_S  三位組選前三
        (result, length) = A5_SSC.OThreeStarZuFront3S_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_ThreeStar_Zu_Front3_S length:{length}")

        # O_ThreeStar_Zu_Middle3_S  三位組選前三
        (result, length) = A5_SSC.OThreeStarZuMiddle3S_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_ThreeStar_Zu_Middle3_S length:{length}")

        # O_ThreeStar_Zu_Last3_S  三位組選後三
        (result, length) = A5_SSC.OThreeStarZuLast3S_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_ThreeStar_Zu_Last3_S length:{length}")

        # O_ThreeStar_Special_Front3 三位特殊號前三
        (result, length) =  A5_SSC.OThreeStarSpecialFront3_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_ThreeStar_Special_Front3 length:{length}")
        
        # O_ThreeStar_Special_Middle3 三位特殊號中三
        (result, length) =  A5_SSC.OThreeStarSpecialMiddle3_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_ThreeStar_Special_Middle3 length:{length}")

        # O_ThreeStar_Special_Last3 三位特殊號後三
        (result, length) =  A5_SSC.OThreeStarSpecialLast3_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_ThreeStar_Special_Last3 length:{length}")

        # O_TwoStar_Zhi_wq 二位直選萬千
        (result, length) =  A5_SSC.OTwoStarZhiWQ_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zhi_wq length:{length}")

        # O_TwoStar_Zhi_wb 二位直選萬百
        (result, length) =  A5_SSC.OTwoStarZhiWB_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zhi_wb length:{length}")

        # O_TwoStar_Zhi_ws 二位直選萬十
        (result, length) =  A5_SSC.OTwoStarZhiWS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zhi_ws length:{length}")

        # O_TwoStar_Zhi_wg 二位直選萬個
        (result, length) = A5_SSC.OTwoStarZhiWG_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zhi_wg length:{length}")

        # O_TwoStar_Zhi_qb 二位直選千百
        (result, length) = A5_SSC.OTwoStarZhiQB_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zhi_qb length:{length}")

        # O_TwoStar_Zhi_qs 二位直選千十
        (result, length) = A5_SSC.OTwoStarZhiQS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zhi_qs length:{length}")

        # O_TwoStar_Zhi_qg 二位直選千個
        (result, length) = A5_SSC.OTwoStarZhiQG_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zhi_qg length:{length}")

        # O_TwoStar_Zhi_bs 二位直選百十
        (result, length) = A5_SSC.OTwoStarZhiBS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zhi_bs length:{length}")

        # O_TwoStar_Zhi_bg 二位直選百個
        (result, length) = A5_SSC.OTwoStarZhiBG_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zhi_bg length:{length}")

        # O_TwoStar_Zhi_sg 二位直選十個
        (result, length) = A5_SSC.OTwoStarZhiSG_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zhi_sg length:{length}")

        # O_TwoStar_Zu_wq 二位組選萬千
        (result, length) = A5_SSC.OTwoStarZuWQ_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zu_wq length:{length}")

        # O_TwoStar_Zu_wb 二位組選萬百
        (result, length) = A5_SSC.OTwoStarZuWB_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zu_wb length:{length}")

        # O_TwoStar_Zu_ws 二位組選萬十
        (result, length) = A5_SSC.OTwoStarZuWS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zu_ws length:{length}")

        # O_TwoStar_Zu_wg 二位組選萬個
        (result, length) =  A5_SSC.OTwoStarZuWG_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zu_wg length:{length}")

        # O_TwoStar_Zu_qb 二位組選千百
        (result, length) =  A5_SSC.OTwoStarZuQB_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zu_qb length:{length}")

        # O_TwoStar_Zu_qs 二位組選千十
        (result, length) = A5_SSC.OTwoStarZuQS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zu_qs length:{length}")

        # O_TwoStar_Zu_qg 二位組選千個
        (result, length) = A5_SSC.OTwoStarZuQG_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zu_qg length:{length}")

        # O_TwoStar_Zu_bs 二位組選百十
        (result, length) = A5_SSC.OTwoStarZuBS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zu_bs length:{length}")

        # O_TwoStar_Zu_bg 二位組選百個
        (result, length) = A5_SSC.OTwoStarZuBG_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zu_bg length:{length}")

        # O_TwoStar_Zu_sg 二位組選十個
        (result, length) = A5_SSC.OTwoStarZuSG_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_TwoStar_Zu_sg length:{length}")

        # O_DingWeiDan_S 定位膽
        (result, length) = A5_SSC.ODingWeiDanS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_DingWeiDan_S length:{length}")

        # O_BSOE_S 大小單雙
        (result, length) = A5_SSC.OBSOES_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_BSOE_S length:{length}")

        # O_DragonTiger_wq 龍虎和萬千
        (result, length) = A5_SSC.ODragonTigerWQ_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_DragonTiger_wq length:{length}")

        # O_DragonTiger_wb 龍虎和萬百
        (result, length) = A5_SSC.ODragonTigerWB_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_DragonTiger_wb length:{length}")

        # O_DragonTiger_ws 龍虎和萬十
        (result, length) = A5_SSC.ODragonTigerWS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_DragonTiger_ws length:{length}")

        # O_DragonTiger_wg 龍虎和萬個
        (result, length) = A5_SSC.ODragonTigerWG_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_DragonTiger_wq length:{length}")

        # O_DragonTiger_qb 龍虎和千百
        (result, length) = A5_SSC.ODragonTigerQB_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_DragonTiger_qb length:{length}")

        # O_DragonTiger_qs 龍虎和千十
        (result, length) = A5_SSC.ODragonTigerQS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_DragonTiger_qs length:{length}")

        # O_DragonTiger_qg 龍虎和千個
        (result, length) = A5_SSC.ODragonTigerQG_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_DragonTiger_qg length:{length}")

        # O_DragonTiger_bs 龍虎和百十
        (result, length) = A5_SSC.ODragonTigerBS_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_DragonTiger_bs length:{length}")

        # O_DragonTiger_bg 龍虎和百個
        (result, length) = A5_SSC.ODragonTigerBG_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_DragonTiger_bg length:{length}")

        # O_DragonTiger_sg 龍虎和十個
        (result, length) = A5_SSC.ODragonTigerSG_Beton()
        for beton in result:
            f.write(f"{beton}\n")
        print(f"O_DragonTiger_sg length:{length}")

    with open('ssc_opencode_list.txt', 'w+', encoding='UTF-8') as f:
        for (a, b, c, d, e) in  itertools.product('0123456789', repeat = 5):
            f.write(f"{a},{b},{c},{d},{e}\n")