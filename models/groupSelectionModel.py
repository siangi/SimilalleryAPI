from models.baseSelectionModel import FILTER_MODES, baseSelectionModel


# select images in groups based on their difference to the baseData
class GroupImageSelector(baseSelectionModel):
    def __init__(self) -> None:
        super().__init__()

    def getMostDifferentImages(baseData: dict, inputList: list, goalLength: int): 
        outputList = []
        inputCopy = inputList.copy()
        filterList = [FILTER_MODES.CATEGORY, FILTER_MODES.ORIGIN_YEAR, FILTER_MODES.NATIONALITY, FILTER_MODES.ARTIST]
        
        while len(filterList) > 0 and len(outputList) < goalLength:
            filtered: list = GroupImageSelector.filterByMultipleCriteria(baseData, inputCopy, filterList)

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