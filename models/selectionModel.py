
from enum import Enum

class FILTER_MODES(Enum):
    CATEGORY: str = "category_name"
    ORIGIN_YEAR: int = "year"
    NATIONALITY: int = "artist_nationality"
    ARTIST: int = "artist_name"

class ImageSelector:
    def getMostDifferentImages(baseData: dict, inputList: list, goalLength: int):
        if(len(inputList) < goalLength):
            raise Exception("Cannot fill the List, not enough Input!")
        
        outputList = []
        inputCopy = inputList.copy()
        filterList = [FILTER_MODES.CATEGORY, FILTER_MODES.ORIGIN_YEAR, FILTER_MODES.NATIONALITY, FILTER_MODES.ARTIST]
        
        while len(filterList) > 0 and len(outputList) < goalLength:
            filtered: list = ImageSelector.filterByMultipleCriteria(baseData, inputCopy, filterList)

            spacesToFill = goalLength - len(outputList)
            if(len(filtered) <= spacesToFill):
                outputList.extend(filtered)
            else:
                outputList.extend(filtered[0:spacesToFill - 1])

            inputCopy = list(filter(lambda element: element not in outputList, inputCopy))
            filterList = filterList[1:]
        
        return outputList


    def filterByMultipleCriteria(baseData: dict, inputList: list, filters: list[FILTER_MODES]) -> list:
        filtered: list = inputList
        
        for filterCrit in filters:
            filtered = list(filter(lambda element: element[filterCrit.value] != baseData[filterCrit.value], filtered))

        return filtered

    