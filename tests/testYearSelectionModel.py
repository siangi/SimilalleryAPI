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
            {"year": 2000, "title": "last"},
            {"year": 1997, "title": "left-out"},
            {"year": 1639, "title": "left-out"},
            {"year": 0, "title": "first"},
            {"year": 5, "title": "left-out"},
            {"year": 534, "title": "left-out"},
            {"year": 1333, "title": "third"},
            {"year": 666, "title": "second"},
            {"year": 666, "title": "left-out"},   
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

if __name__ == '__main__':
    unittest.main()
