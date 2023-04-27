from enum import Enum
from database.imageMapper import imageMapper
import database.connection as connection
from database.queryBuilder import imageQueryBuilder

class SEARCH_MODES(Enum):
    PALETTE = 1
    PALETTE_RATIOS = 2
    ANGLE_RATIOS = 3
    SALIENCY_CENTER = 4
    SALIENCY_RECT = 5
    
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


    def getImageListBySimilarity(self, searchTypes: list, amountPerType: int, baseImageID: int):
        #dev. write mapper, that creates the palette.
        baseData = self.getBaseImageInfo(baseImageID)
        queryBuilder = imageQueryBuilder()
        images = [baseData]
        for searchType in searchTypes:
            queryBuilder.clearConditions()
            match searchType:
                case SEARCH_MODES.PALETTE:
                    #dev . write data stripper so only basics are returned
                    queryBuilder.similarPalette(baseData)

                case SEARCH_MODES.PALETTE_RATIOS:
                    queryBuilder.similarPaletteRatios(baseData)
                    
                case SEARCH_MODES.SALIENCY_CENTER:
                    queryBuilder.similarSaliencyCenter((baseData["sal_center_x"], baseData["sal_center_y"]))
                
                case SEARCH_MODES.SALIENCY_RECT:
                    queryBuilder.similarSaliencyRect(baseData)

                case SEARCH_MODES.ANGLE_RATIOS:
                    queryBuilder.similarAngleRatios(baseData)                
            
            images.extend(self.imgMapper.searchRecords(
                queryBuilder
                    .notMainImg(baseImageID)
                    .buildQuery(amountPerType, False)
            ))
            
        for index, image in enumerate(images):
            if index == 0:
                image["isMain"] = True
            else:
                image["isMain"] = False

        return images

        

    def getBaseImageInfo(self, baseID):
        queryBuilder = imageQueryBuilder()
        possibles = self.imgMapper.searchRecords(queryBuilder.imgByID(baseID).buildQuery(1))
        if len(possibles) > 0:
            return possibles[0]


