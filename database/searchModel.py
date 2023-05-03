from enum import Enum
from database.imageMapper import imageMapper
import database.connection as connection
from database.queryBuilder import imageQueryBuilder

class SEARCH_MODES(Enum):
    PALETTE: int = 1
    PALETTE_RATIOS: int = 2
    ANGLE_RATIOS: int = 3
    SALIENCY_CENTER: int = 4
    SALIENCY_RECT: int = 5
    
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
        baseData = self.getBaseImageInfo(baseImageID)
        queryBuilder = imageQueryBuilder()
        images = [baseData]
        for searchType in searchTypes:
            queryBuilder.clearConditions()
            # restore these to the ENUM when I find out hwo
            match searchType:
                case 1:
                    queryBuilder.similarPalette(baseData)

                case 2:
                    queryBuilder.similarPaletteRatios(baseData)
                    
                case 3:
                    queryBuilder.similarAngleRatios(baseData)  
                
                case 4:
                    queryBuilder.similarSaliencyCenter((baseData["sal_center_x"], baseData["sal_center_y"]))

                case 5:
                    queryBuilder.similarSaliencyRect(baseData)                           
            
            images.extend(self.imgMapper.searchRecords(
                queryBuilder
                    .notMainImg(baseImageID)
                    .buildQuery(amountPerType, False)
            ))

            
        for index, image in enumerate(images):
            if int(image["idimage"]) == baseImageID:
                image["isMain"] = True
            else:
                image["isMain"] = False

        return self._removeDoublesById(images)      


    def getBaseImageInfo(self, baseID):
        queryBuilder = imageQueryBuilder()
        possibles = self.imgMapper.searchRecords(queryBuilder.imgByID(baseID).buildQuery(1))
        if len(possibles) > 0:
            return possibles[0]


