import unittest
from models.yearSelectionModel import YearImageSelector

class testYearImageSelector(unittest.TestCase):
    def testGetMostDifferentCorrectOrder(self):
        baseData = {}
        inputList = [
            {"year": 2000, "title": "last"},
            {"year": 0, "title": "first"},
            {"year": 1333, "title": "third"},
            {"year": 666, "title": "second"},   
        ]
        expectedOutput = [
            {"year": 0, "title": "first"},
            {"year": 666, "title": "second"},
            {"year": 1333, "title": "third"},
            {"year": 2000, "title": "last"},              
        ]

        goalLength = 4

        actualOutput = YearImageSelector.getMostDifferentImages(baseData, inputList, goalLength)
        self.assertListEqual(actualOutput, expectedOutput)

    def testMostDifferentClosest(self):
        baseData ={}
        inputList = [
            {"year": 2000, "title": "last", "artist_name": "daniel dopeson", "category_name": "abstract", "artist_nationality": "swiss"},
            {"year": 1997, "title": "left-out", "artist_name": "magic johnson", "category_name": "abstract", "artist_nationality": "swiss"},
            {"year": 1639, "title": "left-out", "artist_name": "son goku", "category_name": "abstract", "artist_nationality": "swiss"},
            {"year": 0, "title": "first", "artist_name": "luke skywalker", "category_name": "abstract", "artist_nationality": "swiss"},
            {"year": 5, "title": "left-out", "artist_name": "neil armstrong", "category_name": "abstract", "artist_nationality": "swiss"},
            {"year": 534, "title": "left-out", "artist_name": "sofles", "category_name": "abstract", "artist_nationality": "swiss"},
            {"year": 1333, "title": "third", "artist_name": "vans the omega", "category_name": "abstract", "artist_nationality": "swiss"},
            {"year": 666, "title": "second", "artist_name": "mark maggiori", "category_name": "landscape", "artist_nationality": "french"},
            {"year": 666, "title": "left-out", "artist_name": "smash137", "category_name": "abstract", "artist_nationality": "swiss"},   
        ]
        expectedOutput = [
            {"year": 0, "title": "first", "artist_name": "luke skywalker", "category_name": "abstract", "artist_nationality": "swiss"},
            {"year": 666, "title": "second", "artist_name": "mark maggiori", "category_name": "landscape", "artist_nationality": "french"},
            {"year": 1333, "title": "third", "artist_name": "vans the omega", "category_name": "abstract", "artist_nationality": "swiss"},
            {"year": 2000, "title": "last", "artist_name": "daniel dopeson", "category_name": "abstract", "artist_nationality": "swiss"},              
        ]
        goalLength = 4

        actualOutput = YearImageSelector.getMostDifferentImages(baseData, inputList, goalLength)
        self.assertListEqual(actualOutput, expectedOutput)
        
    def testEmptyInput(self):
        baseData ={}
        inputList = []
        expectedOutput = []
        goalLength = 4

        actualOutput = YearImageSelector.getMostDifferentImages(baseData, inputList, goalLength)
        self.assertListEqual(actualOutput, expectedOutput)


if __name__ == '__main__':
    unittest.main()
