from enum import Enum
from database.imageMapper import imageMapper
import database.connection as connection
from database.queryBuilder import imageQueryBuilder
from models.selectionModel import ImageSelector

class SEARCH_MODES(Enum):
    PALETTE: int = 0
    PALETTE_RATIOS: int = 1
    ANGLE_RATIOS: int = 2
    SALIENCY_CENTER: int = 3
    SALIENCY_RECT: int = 4
    
class similaritySearchModel:
    imgMapper: imageMapper
    # searchFor the base record by ID
    # create a searchstring for each type searched
    # execute said searchstring
    # extract relevant data
    # return list of images 
    def __init__(self, mapper = None) -> None:
        if mapper == None:
            self.imgMapper = imageMapper()
        else:
            self.imgMapper = mapper         

    def _removeDoublesById(self, objectList):
        unique =  {}
        for elem in objectList:
            unique[elem["idimage"]] = elem
        
        return list(unique.values()) 


    def getImageListBySimilarity(self, searchTypes: list, amountPerType: int, baseImageID: int):
        #dev. write mapper, that creates the palette.
        baseData = None
        if baseImageID == -1:
            baseData = self.getRandomBaseImage()
        else:
            baseData = self.getBaseImageInfo(baseImageID)

        queryBuilder = imageQueryBuilder()
        images = [baseData]
        for searchType in searchTypes:
            queryBuilder.clearConditions()
            # restore these to the ENUM when I find out hwo
            match searchType:
                case SEARCH_MODES.PALETTE.value:
                    queryBuilder.similarPalette(baseData).paletteSorting(baseData)

                case SEARCH_MODES.PALETTE_RATIOS.value:
                    queryBuilder.similarPaletteRatios(baseData).paletteRatioSorting(baseData)
                    
                case SEARCH_MODES.ANGLE_RATIOS.value:
                    queryBuilder.similarAngleRatios(baseData).angleRatioSorting(baseData)  
                
                case SEARCH_MODES.SALIENCY_CENTER.value:
                    center = (baseData["sal_center_x"], baseData["sal_center_y"])
                    queryBuilder.similarSaliencyCenter(center).saliencyCenterSorting(center)

                case SEARCH_MODES.SALIENCY_RECT.value:
                    queryBuilder.similarSaliencyRect(baseData).saliencyRectSorting(baseData)

            fullquery = queryBuilder.notMainImg(baseImageID).buildQuery(100, False)
            unselected = self.imgMapper.searchRecords(fullquery) 
            selected = ImageSelector.getMostDifferentImages(baseData, unselected, amountPerType)
            images.extend(selected)

        for image in images:
            if image["idimage"] == baseData["idimage"]:
                image["isMain"] = True
            else:
                image["isMain"] = False

        return self._removeDoublesById(images)      

    def getRandomBaseImage(self):
        queryBuilder = imageQueryBuilder()
        randomQuery = queryBuilder.randomIdSorting().buildQuery(1)
        possibles = self.imgMapper.searchRecords(randomQuery)
        if len(possibles) > 0:
            return possibles[0]

    def getBaseImageInfo(self, baseID):
        queryBuilder = imageQueryBuilder()
        possibles = self.imgMapper.searchRecords(queryBuilder.imgByID(baseID).buildQuery(1))
        if len(possibles) > 0:
            return possibles[0]
        




