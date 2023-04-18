from enum import Enum
import mysql.connector
import database.connection as connection
from database.queryBuilder import imageQueryBuilder

class SEARCH_MODES(Enum):
    PALETTE: 1
    PALETTE_RATIOS: 2
    ANGLE_RATIOS: 3
    SALIENCY_CENTER: 4
    SALIENCY_RECT: 5
    
class similaritySearchModel:
    # searchFor the base record by ID
    # create a searchstring for each type searched
    # execute said searchstring
    # extract relevant data
    # return list of images 
    def __init__(self) -> None:
        self._dbConnection = None   

    def prepareDbConnection(self):
        if self._dbConnection == None:
            mysql.connector.connect(host=connection.host, username=connection.username, password=connection.password, database="scheme_test_similallery")


    def getImageListBySimilarity(self, searchTypes: list, amountPerType: int, baseImageID: int):
        self.prepareDbConnection()
        baseData = self.getBaseImageInfo(baseImageID)
        pass

    def getBaseImageInfo(self, baseID):
        queryBuilder = imageQueryBuilder()
        pass