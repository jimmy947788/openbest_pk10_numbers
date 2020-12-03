import itertools

if __name__ == "__main__":
    """
    O_FiveStar_SpecialFour (10)
    O_FiveStar_SpecialThree (10)
    O_FiveStar_SpecialTwo (10)
    O_FiveStar_SpecialOne (10)
    O_FiveStar_Zu5     (90)
    O_FiveStar_Zu10   (90)
    O_FiveStar_Zu20   (360)
    O_FiveStar_Zu30   (360) 
    O_FiveStar_Zu60   (840) #itertools.permutations('0123456789', 3):
    O_FiveStar_Zu120 (252) #itertools.combinations('0123456789', 5):
    O_FiveStar_ZhiFu (100000)
    """

    print("O_FiveStar_Zu60")
    for i in  ["00", "11", "22", "33", "44", "55", "66", "77", "88", "99"]:
        for j in ["012", "123", "234", "345", "456", "789"]:
            print(f"{i}, {j}")

