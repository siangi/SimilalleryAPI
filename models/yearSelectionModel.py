from models.groupSelectionModel import FILTER_MODES
from models.baseSelectionModel import baseSelectionModel
from typing import List

class YearImageSelector(baseSelectionModel):
    def getMostDifferentImages(baseData: dict, inputList: list, goalLength: int):
        outputList = []
        inputCopy = inputList.copy()

        if(len(inputCopy) == 0):
            return outputList

        minYear = min(inputCopy, key=lambda img: img["year"])["year"]
        maxYear = max(inputCopy, key=lambda img: img["year"])["year"]
        goalGap = (maxYear - minYear) / (goalLength - 1)

        for i in range(0, goalLength):
            if(len(inputCopy) < 1):
                break

            goalYear = minYear + goalGap * i
            closest = sorted(inputCopy, key=lambda image: abs(image["year"] - goalYear))[0]
            inputCopy.remove(closest)
            outputList.append(closest)

        return outputList



