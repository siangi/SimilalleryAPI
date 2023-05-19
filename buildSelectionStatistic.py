from models.searchModel import similaritySearchModel, SEARCH_MODES
from database.imageMapper import imageMapper




class statisticBuilder: 
    def tryFindImagesWithToFewResults():
        SampleSize = 10000
        randomIDs = statisticBuilder.getListOfRandomImageIDs(SampleSize)
        model = similaritySearchModel()
        counter = 0
        for Id in randomIDs:
            try:
                model.getImageListBySimilarity([SEARCH_MODES.SALIENCY_CENTER], 30, Id["idimage"])
            except Exception as ex :
                print(print(ex))
                counter += 1
                print(Id)
        
        print("amount of failing Ids" + str(counter))




    def getListOfRandomImageIDs(length) -> list:
        query = f"SELECT idimage from image ORDER BY RAND() LIMIT {length}"
        mapper = imageMapper()
        return mapper.searchRecords(query)


if __name__ == '__main__':
    print("not enough results for following IDs:")
    statisticBuilder.tryFindImagesWithToFewResults()