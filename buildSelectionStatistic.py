from typing import List
from decimal import Decimal
from models.searchModel import similaritySearchModel, SEARCH_MODES
from database.imageMapper import imageMapper
import statistics as pystat
import time

# for easier calculation of the overall statistic afterwards
class queryStatistic:
    baseID: int
    similarityValues: List[Decimal]
    averageSimilarity: Decimal
    # all the Lists here should only have unique Values
    indexes: List[int]
    artists: List[int]
    nationalities: List[int]
    categories: List[int]
    years: List[int]

    def cleanAllDuplicates(self):
        self.indexes = list(dict.fromkeys(self.indexes))
        self.artists = list(dict.fromkeys(self.artists))
        self.nationalities = list(dict.fromkeys(self.nationalities))
        self.categories = list(dict.fromkeys(self.categories))
        self.years = list(dict.fromkeys(self.years))

    def __init__(self) -> None:
        self.similarityValues = []
        self.indexes = []
        self.artists = []
        self.nationalities = []
        self.categories = []
        self.years = []

class statisticBuilder: 
    def tryFindImagesWithToFewResults():
        SampleSize = 10000
        randomIDs = statisticBuilder.getListOfRandomImageIDs(SampleSize)
        model = similaritySearchModel()
        counter = 0
        for Id in randomIDs:
            try:
                model.getImageListBySimilarity([SEARCH_MODES.SALIENCY_RECT], 30, Id["idimage"])
            except Exception as ex :
                print(print(ex))
                counter += 1
                print(Id)
        
        print("amount of failing Ids" + str(counter))

    def getListOfRandomImageIDs(length) -> List[dict]:
        # sollte das auch in querybuilder eingebaut werden?
        query = f"SELECT idimage from image ORDER BY RAND() LIMIT {length}"
        mapper = imageMapper()
        
        return mapper.searchRecords(query)
    

    def CollectImageData(searchModes: List[int], sampleSize: int) -> List[List[dict]]:
        SIMILAR_IMAGES_COUNT = 10
        randomRecords = statisticBuilder.getListOfRandomImageIDs(sampleSize)
        imageData = []
        model = similaritySearchModel()
        for record in randomRecords:
            similars = model.getImageListBySimilarity(searchModes, 10, record["idimage"])
            queryData = statisticBuilder.createQueryStatistic(similars, record["idimage"])
            imageData.append(queryData)

        return imageData
    
    def createQueryStatistic(similars: list, baseID) -> queryStatistic:
        statistic = queryStatistic()
        for similar in similars:
            statistic.baseID = baseID
            statistic.indexes.append(similar["idimage"])
            statistic.artists.append(similar["artist_id"])
            statistic.categories.append(similar["category_id"])
            statistic.nationalities.append(similar["artist_nationality"])
            statistic.years.append(similar["year"])
            # statistic.similarityValues.append(similar["similarity_Val"])
            statistic.cleanAllDuplicates()

        return statistic

    def calculateOverallStatistcs(queriesData: List[queryStatistic]):
        artistLengths = []
        categoryLengths = []
        nationLengths = []
        yearLengths = []
        indexLengths = []

        for query in queriesData:
            indexLengths.append(len(query.indexes))
            artistLengths.append(len(query.artists))
            categoryLengths.append(len(query.categories))
            nationLengths.append(len(query.nationalities))
            yearLengths.append(len(query.years))

        return {
            "artistStats": {"mean": round(pystat.mean(artistLengths), 2), "median": round(pystat.median(artistLengths), 2), "stdDeviation": round(pystat.stdev(artistLengths), 2)},
            "categoryStats": {"mean": round(pystat.mean(categoryLengths), 2), "median": round(pystat.median(categoryLengths), 2), "stdDeviation": round(pystat.stdev(categoryLengths), 2)},
            "nationStats": {"mean": round(pystat.mean(nationLengths), 2), "median": round(pystat.median(nationLengths), 2), "stdDeviation": round(pystat.stdev(nationLengths), 2)},
            "yearStats": {"mean": round(pystat.mean(yearLengths), 2), "median": round(pystat.median(yearLengths), 2), "stdDeviation": round(pystat.stdev(yearLengths), 2)},
            "indexStats": {"mean": round(pystat.mean(indexLengths), 2), "median": round(pystat.median(indexLengths), 2), "stdDeviation": round(pystat.stdev(indexLengths), 2)},
        }

    def createSelectionStatistcs():
        startTime = time.time()
        queries = statisticBuilder.CollectImageData([4], 1000)
        overall = statisticBuilder.calculateOverallStatistcs(queries)
        endTime = time.time()
        print(f"time elapsed: {(endTime - startTime)}")
        for key in overall:
            print(key, overall[key])

if __name__ == '__main__':
    print("try build statistics")
    statisticBuilder.createSelectionStatistcs()