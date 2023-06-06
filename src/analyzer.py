import pandas as pd
import numpy as np
from enum import Enum

class Column(Enum):
    NAME = 0
    GENDER = 1
    AGE = 2
    WEIGHT = 3
    MAJOR = 4
    WEEKDAY = 5
    STRESS = 6
    KIND_OF_MEAL = 7
    LOCATION = 8
    KIND_OF_DISH = 9
    PRICE = 10
    SATISFICATION = 11
    WITH_WHOM = 12
    TIME_TO_MOVE = 13
    TIME_TO_EAT = 14
    HOW_TO_MOVE = 15
    DATA_FROM_WHEN = 16

class HSS001Analyzer:
    def __init__(self):
        self.targetDf = pd.read_excel("../dataset/DB_230523.xlsx")

        self.mandExpDict = {}    #필수식비
        self.expEffOnCampusDict = {}        #학사식당식비효용

    def __calcMandExpAt(self, argYear: str, arg1000Breakfast: bool, argConsiderAdv: int):

        if(str != type(argYear)):
            print("calcMandExpAt: argYear must be a string")
            return 0

        if(argYear not in ["2017-2018년", "2022년 1학기", "2022년 2학기", "2023년 1학기"]):
           print("calcMandExpAt: wrong argYear")
           return 0
        
        sumOfPrice = 0
        count = 0
        
        for rowIndex in range(len(self.targetDf.index)):
            targetRow = self.targetDf.iloc[rowIndex]
            year = targetRow[Column.DATA_FROM_WHEN.value]
            kindOfMeal = targetRow[Column.KIND_OF_MEAL.value]
            location = targetRow[Column.LOCATION.value]
            price = targetRow[Column.PRICE.value]

            if(year != argYear):
                continue
            elif(kindOfMeal not in ["아침", "점심", "저녁"]):
                continue
            elif("집" == location):
                continue
            elif(0 == price):
                continue
            else:
                if(True == arg1000Breakfast and "아침" == kindOfMeal and location in ["북측", "동측", "서측"]):
                    price = 1000

                sumOfPrice += price
                count += 1

        if(True == arg1000Breakfast):
            newOne = argConsiderAdv
            sumOfPrice += newOne * 1000
            count += newOne

        mandExp = round(np.float32(sumOfPrice/count) / 6964.65, 2)

        self.mandExpDict[argYear] = mandExp

    def calcMandExp(self, arg1000Breakfast):

        print("============= Mandatory Expense =============")

        if(False == arg1000Breakfast):
            for year in ["2017-2018년", "2022년 1학기", "2022년 2학기", "2023년 1학기"]:
                self.__calcMandExpAt(year, arg1000Breakfast, 0)
            print(self.mandExpDict)
            print("================")

        else:
            for adv in range(0, 301, 50):
                print("Adv: ", adv)
                for year in ["2017-2018년", "2022년 1학기", "2022년 2학기", "2023년 1학기"]:
                    self.__calcMandExpAt(year, arg1000Breakfast, adv)
                print(self.mandExpDict)
                print("================")

        print()

    def __calcExpEffOnCampusAt(self, argYear: str, arg1000Breakfast: bool, argConsiderAdv: int):

        if(str != type(argYear)):
            print("calcMandExpAt: argYear must be a string")
            return 0

        if(argYear not in ["2017-2018년", "2022년 1학기", "2022년 2학기", "2023년 1학기"]):
           print("calcMandExpAt: wrong argYear")
           return 0
        
        sumOfPriceOnCampus = 0
        sumOfPriceNotOnCampus = 0

        countOnCampus = 0
        countNotOnCampus = 0
        
        for rowIndex in range(len(self.targetDf.index)):
            targetRow = self.targetDf.iloc[rowIndex]
            year = targetRow[Column.DATA_FROM_WHEN.value]
            kindOfMeal = targetRow[Column.KIND_OF_MEAL.value]
            location = targetRow[Column.LOCATION.value]
            price = targetRow[Column.PRICE.value]

            if(year != argYear):
                continue
            elif(kindOfMeal not in ["아침", "점심", "저녁"]):
                continue
            elif("집" == location):
                continue
            elif(0 == price):
                continue
            else:
                if(True == arg1000Breakfast and "아침" == kindOfMeal and location in ["북측", "동측", "서측"]):
                    price = 1000

                if(location in ["북측, 동측", "서측"]):
                    sumOfPriceOnCampus += price
                    countOnCampus += 1
                elif(location in ["어은동", "궁동"]):
                    sumOfPriceNotOnCampus += price
                    countNotOnCampus += 1

        if(True == arg1000Breakfast):
            newOne = argConsiderAdv
            sumOfPriceOnCampus += newOne * 1000
            countOnCampus += newOne

        avgExpOnCampus = np.float32(sumOfPriceOnCampus/countOnCampus)
        avgExpNotOnCampus = np.float32(sumOfPriceNotOnCampus/countNotOnCampus)

        expEffOnCampus = round(np.float32(1 - avgExpOnCampus/avgExpNotOnCampus), 2)

        self.expEffOnCampusDict[argYear] = expEffOnCampus

    def calcExpEffOnCampus(self, arg1000Breakfast):

        print("============= Expence Efficiency On Campus =============")

        if(False == arg1000Breakfast):
            for year in ["2017-2018년", "2022년 1학기", "2022년 2학기", "2023년 1학기"]:
                self.__calcExpEffOnCampusAt(year, arg1000Breakfast, 0)
            print(self.expEffOnCampusDict)
            print("================")

        else:
            for adv in range(0, 301, 50):
                print("Adv: ", adv)
                for year in ["2017-2018년", "2022년 1학기", "2022년 2학기", "2023년 1학기"]:
                    self.__calcExpEffOnCampusAt(year, arg1000Breakfast, adv)
                print(self.expEffOnCampusDict)
                print("================")

        print()
    

    def printStatus(self):

        genderDict = {}
        ageDict ={}
        weightDict = {}
        majorDict = {}

        for rowIndex in range(len(self.targetDf.index)):
            targetRow = self.targetDf.iloc[rowIndex]

            name = targetRow[Column.NAME.value]
            gender = targetRow[Column.GENDER.value]
            age = targetRow[Column.AGE.value]
            weight = targetRow[Column.WEIGHT.value]
            major = targetRow[Column.MAJOR.value]

            for (item, itemDict) in [(gender, genderDict), (age, ageDict), (weight, weightDict), (major, majorDict)]:
                if(item in itemDict):
                    exists = 0

                    for key in list(itemDict.keys()):
                        if(name in itemDict[key]):
                            exists = 1

                    if(0 == exists):
                        itemDict[item].append(name)

                else:
                    itemDict[item] = [name]


        for (item, itemDict) in [("gender", genderDict), ("age", ageDict), ("weight", weightDict), ("major", majorDict)]:
            
            print("========" + item + "========")

            totalNum = 0 

            for key in list(itemDict.keys()):
                print(key, len(itemDict[key]))
                totalNum += len(itemDict[key])

            print("Total: ", totalNum)
            print()

            




