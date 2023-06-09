from typing import List
from decimal import Decimal
from models.searchModel import similaritySearchModel, SEARCH_MODES
from models.groupSelectionModel import GroupImageSelector
from models.singularSelectionModel import SingularImageSelector
from models.yearSelectionModel import YearImageSelector
from models.baseSelectionModel import baseSelectionModel
from database.imageMapper import imageMapper
import statistics as pystat
import time
import logging

# for easier calculation of the overall statistic afterwards
class queryStatistic:
    baseID: int
    similarityValues: List[float]
    similarityMean: float
    similarityDeviation: float
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
        self.similarityMean = -1.0
        self.similarityDeviation = -1.0

class statisticBuilder: 
    SAMPLE_SIZE = 1000
    SELECTED_IMAGES_LENGTH = 5

    # was used to adjust the search ranges for each criteria
    def tryFindImagesWithToFewResults():
        SampleSize = 10000
        randomIDs = statisticBuilder.getListOfRandomImageIDs(SampleSize)
        model = similaritySearchModel()
        counter = 0
        for Id in randomIDs:
            try:
                model.getImageListBySimilarity([2], 25, Id["idimage"])
            except Exception as ex :
                counter += 1
                print(Id, counter, ex)
        
        print("amount of failing Ids" + str(counter))

    def getListOfRandomImageIDs(length) -> List[dict]:
        query = f"SELECT idimage from image ORDER BY RAND() LIMIT {length}"
        mapper = imageMapper()
        
        return mapper.searchRecords(query)
    
    def createQueryStatistic(similars: list, baseID) -> queryStatistic:
        statistic = queryStatistic()
        for similar in similars:
            statistic.baseID = baseID
            statistic.indexes.append(similar["idimage"])
            statistic.artists.append(similar["artist_id"])
            statistic.categories.append(similar["category_id"])
            statistic.nationalities.append(similar["artist_nationality"])
            statistic.years.append(similar["year"])
            if(similar["idimage"] != baseID):
                statistic.similarityValues.append(similar["similarity_val"])
            statistic.cleanAllDuplicates()

        try:
            if(len(similars) == 1 and similars[0]["idimage"] != baseID):
                statistic.similarityMean = statistic.similarityValues[0]
                statistic.similarityDeviation = 0
            elif(len(similars) <= 3):
                statistic.similarityMean = 0.5
                statistic.similarityDeviation = 0.5
            else:
                statistic.similarityMean = pystat.mean(statistic.similarityValues)
                statistic.similarityDeviation = pystat.stdev(statistic.similarityValues) 
        except Exception as e:
            raise UserWarning(f"{e} with baseID {baseID} and amount {len(similars)}") from e


        return statistic

    def calculateOverallStatistcs(queriesData: List[queryStatistic]):
        artistLengths = []
        categoryLengths = []
        nationLengths = []
        yearLengths = []
        indexLengths = []
        similarityMeans = []

        for query in queriesData:
            indexLengths.append(len(query.indexes))
            artistLengths.append(len(query.artists))
            categoryLengths.append(len(query.categories))
            nationLengths.append(len(query.nationalities))
            yearLengths.append(len(query.years))
            similarityMeans.append(query.similarityMean)

        return {
            "similarityStats": { "mean": round(pystat.mean(similarityMeans), 5), "median": round(pystat.median(similarityMeans), 5), "stdDeviation": round(pystat.stdev(similarityMeans), 5)},
            "artistStats": {"mean": round(pystat.mean(artistLengths), 2), "median": round(pystat.median(artistLengths), 2), "stdDeviation": round(pystat.stdev(artistLengths), 2)},
            "categoryStats": {"mean": round(pystat.mean(categoryLengths), 2), "median": round(pystat.median(categoryLengths), 2), "stdDeviation": round(pystat.stdev(categoryLengths), 2)},
            "nationStats": {"mean": round(pystat.mean(nationLengths), 2), "median": round(pystat.median(nationLengths), 2), "stdDeviation": round(pystat.stdev(nationLengths), 2)},
            "yearStats": {"mean": round(pystat.mean(yearLengths), 2), "median": round(pystat.median(yearLengths), 2), "stdDeviation": round(pystat.stdev(yearLengths), 2)},
            "indexStats": {"mean": round(pystat.mean(indexLengths), 2), "median": round(pystat.median(indexLengths), 2), "stdDeviation": round(pystat.stdev(indexLengths), 2)},
        }

    def createSelectionStatistcsSpeedy():
        logging.basicConfig(filename="./logs/statsticsLogs.log", encoding="UTF-8", level=logging.DEBUG)
        baseIDs = statisticBuilder.getListOfRandomImageIDs(statisticBuilder.SAMPLE_SIZE)
        logging.info("----------------------------")
        logging.info(f"selection statistics calculated with sampleSize {statisticBuilder.SAMPLE_SIZE}, selection Size {statisticBuilder.SELECTED_IMAGES_LENGTH} at {time.strftime('%b %d %Y %H:%M:%S', time.localtime())}")
        startTime = time.time()
        for categoryIdx in range(0, 5):
            logging.info(f"search type {categoryIdx} for all three Selections")
            selectors: List[dict] = [
                {"model": GroupImageSelector, "queryStatistics": []} ,
                {"model": YearImageSelector, "queryStatistics": []},
                {"model": SingularImageSelector, "queryStatistics": []},
                {"model": None, "queryStatistics": []}]
            
            for record in baseIDs:
                id = record["idimage"]
                searchModel = similaritySearchModel()
                baseData = searchModel.getBaseImageInfo(id)
                similars = searchModel.getImageListBySimilarity([categoryIdx], 100, id, "none")

                for selector in selectors:
                    chosen: list
                    if(selector["model"] == None):
                        chosen = similars[:statisticBuilder.SELECTED_IMAGES_LENGTH]
                    else:
                        chosen = selector["model"].getMostDifferentImages(baseData, similars, statisticBuilder.SELECTED_IMAGES_LENGTH)   
                    
                    selector["queryStatistics"].append(statisticBuilder.createQueryStatistic(chosen, id))

            for selector in selectors:
                logging.info(f"selector: {selector['model']}")
                overall = statisticBuilder.calculateOverallStatistcs(selector["queryStatistics"])
                for key in overall:
                    logging.info(f"{key}: {overall[key]}")

        endTime = time.time()
        logging.info(f"time elapsed: {(endTime - startTime)}")

if __name__ == '__main__':
    print("building statistics")

    statisticBuilder.createSelectionStatistcsSpeedy()

    print("done, see log for details")