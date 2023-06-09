from models.groupSelectionModel import FILTER_MODES
from models.baseSelectionModel import baseSelectionModel
from typing import List

# select images one by one based on their differences to all of the selected images.
class SingularImageSelector(baseSelectionModel): 
    def getMostDifferentImages(baseData: dict, inputList: list, goalLength: int):
        return SingularImageSelector.getMostDifferentImages([baseData], inputList, goalLength)

    def getMostDifferentImages(baseData: List[dict], inputList: list, goalLength: int):
        if (not isinstance(baseData, List)):
            baseData = [baseData]
        outputList = []
        inputCopy = inputList.copy()
        containedValues = {
            FILTER_MODES.CATEGORY.value: [],
            FILTER_MODES.ORIGIN_YEAR.value: [],
            FILTER_MODES.NATIONALITY.value: [],
            FILTER_MODES.ARTIST.value: [],
        }
        filterList = [FILTER_MODES.CATEGORY, FILTER_MODES.ORIGIN_YEAR, FILTER_MODES.NATIONALITY, FILTER_MODES.ARTIST]

        #first image just needs to be different from the base data
        SingularImageSelector.addRecordValuesToDict(containedValues, baseData)
        while len(outputList) < goalLength and len(inputCopy) > 0:
            filtered = SingularImageSelector.filterByMultipleCriteriaAndValues(inputCopy, containedValues, filterList)

            if (len(filtered) > 0):
                outputList.append(filtered[0])
                SingularImageSelector.addRecordValuesToDict(containedValues, [filtered[0]])
                inputCopy = list(filter(lambda element: element not in outputList, inputCopy))
            else:
                filterList = filterList[1:]

            # we want to fill the list even if there are duplicates so just copy the first few, since they are the most similar
            if len(filterList) < 1:
                spacesToFill = spacesToFill = goalLength - len(outputList)
                outputList.extend(inputCopy[:spacesToFill])

        return outputList

    def addRecordValuesToDict(containedValues: dict, listToAdd: List[dict]) -> dict:
        for key in containedValues:
            for toAdd in listToAdd:
                containedValues[key].append(toAdd[key])
    
        return containedValues       


    def filterByMultipleCriteriaAndValues(inputList: List[dict], valuesToAvoid: dict, filters: List[FILTER_MODES]) -> List[dict]:
        filtered: list = inputList

        for filterCrit in filters: 
            filtered = list(filter(lambda element: element[filterCrit.value] not in valuesToAvoid[filterCrit.value], filtered))
        
        return filtered
    

    