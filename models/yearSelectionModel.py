from models.groupSelectionModel import FILTER_MODES
from models.baseSelectionModel import baseSelectionModel
from models.singularSelectionModel import SingularImageSelector
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
            sortedByDistance = sorted(inputCopy, key=lambda image: abs(image["year"] - goalYear))
            smallestDistance = abs(sortedByDistance[0]["year"] - goalYear)
            closestFew = list(filter(lambda element: abs(element["year"] - goalYear) == smallestDistance, sortedByDistance))
            chosen = closestFew[0]
            if (len(closestFew) > 1):
                candidates = SingularImageSelector.getMostDifferentImages(outputList, closestFew, 1)
                if len(candidates) > 0:
                    chosen = candidates[0]

            inputCopy.remove(chosen)
            outputList.append(chosen)

        return outputList



