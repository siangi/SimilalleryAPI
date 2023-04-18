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
        for searchType in searchTypes:
            match searchType:
                case SEARCH_MODES.PALETTE:
                    #dev . write data stripper so only basics are returned
                    images = self.imgMapper.searchRecords(
                        queryBuilder
                            .similarPaletteCondition(baseData)
                            .buildQuery(amountPerType, False))
                    return images
                case _:
                    raise Exception(f"search Type {searchType} not yet implemented")

        

    def getBaseImageInfo(self, baseID):
        queryBuilder = imageQueryBuilder()
        possibles = self.imgMapper.searchRecords(queryBuilder.imgByIDCondition(baseID).buildQuery(1))
        if len(possibles) > 0:
            return possibles[0]


