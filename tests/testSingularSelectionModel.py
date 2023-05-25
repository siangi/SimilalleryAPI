import unittest
from models.singularSelectionModel import SingularImageSelector
from models.baseSelectionModel import FILTER_MODES

class testSingularImageSelector(unittest.TestCase):
    
    def testGetMostDifferentImages(self):
        basedata = {
            'category_name': 'Abstract',
            'year': 2021,
            'artist_nationality': 'USA',
            'artist_name': 'John Doe'
        }
        inputList = [
            {'category_name': 'Abstract', 'year': 2021, 'artist_nationality': 'USA', 'artist_name': 'John Doe'},
            {'category_name': 'Landscape', 'year': 2022, 'artist_nationality': 'UK', 'artist_name': 'Alice Smith'},
            {'category_name': 'Portrait', 'year': 2023, 'artist_nationality': 'USA', 'artist_name': 'Bob Johnson'},
            {'category_name': 'Abstract', 'year': 2021, 'artist_nationality': 'UK', 'artist_name': 'Charlie Brown'},
            {'category_name': 'Landscape', 'year': 2024, 'artist_nationality': 'USA', 'artist_name': 'David Lee'},
            {'category_name': 'Portrait', 'year': 2023, 'artist_nationality': 'UK', 'artist_name': 'Eva Green'},
            {'category_name': 'Abstract', 'year': 2025, 'artist_nationality': 'CH', 'artist_name': 'Rick Astley'},
        ]

        expectedOutput = [
            {'category_name': 'Landscape', 'year': 2022, 'artist_nationality': 'UK', 'artist_name': 'Alice Smith'},
            {'category_name': 'Abstract', 'year': 2025, 'artist_nationality': 'CH', 'artist_name': 'Rick Astley'},
            {'category_name': 'Portrait', 'year': 2023, 'artist_nationality': 'USA', 'artist_name': 'Bob Johnson'},
            {'category_name': 'Abstract', 'year': 2021, 'artist_nationality': 'UK', 'artist_name': 'Charlie Brown'}, 
        ]
        
        goalLength = 4

        actualOutput = SingularImageSelector.getMostDifferentImages(basedata, inputList, goalLength)

        self.assertListEqual(expectedOutput, actualOutput)


    def testAddRecordValuesToDict(self):
        testData = [
            {"inputDict": { "key1": [], "key2": [], "key3": []},
             "toAdd": {"key1": "val1", "key2": "val2", "key3": "val3", "key4": "val4"},
             "expected": { "key1": ["val1"], "key2": ["val2"], "key3": ["val3"]}
             },
            {"inputDict": { "key1": ["existing1"], "key2": ["existing2"], "key3": ["existing3"]},
             "toAdd": {"key1": "val1", "key2": "val2", "key3": "val3", "key4": "val4"},
             "expected": { "key1": ["existing1", "val1"], "key2": ["existing2", "val2"], "key3": ["existing3", "val3"]}
            }
        ]
        
        for test in testData:
            actual = SingularImageSelector.addRecordValuesToDict(test["inputDict"], test["toAdd"])
            self.assertDictEqual(test["expected"], actual)

    def testFilterByMultiCritsAndVals(self):
        testData = [
            {"inputList": [{FILTER_MODES.CATEGORY.value: "rapid", FILTER_MODES.ARTIST.value: "lorem", FILTER_MODES.NATIONALITY.value: "funky"},
                            {FILTER_MODES.CATEGORY.value: "dopeness", FILTER_MODES.ARTIST.value: "brokes", FILTER_MODES.NATIONALITY.value: "jumpy"},
                            {FILTER_MODES.CATEGORY.value: "rapid", FILTER_MODES.ARTIST.value: "sing", FILTER_MODES.NATIONALITY.value: "song"},
                            {FILTER_MODES.CATEGORY.value: "loco", FILTER_MODES.ARTIST.value: "moco", FILTER_MODES.NATIONALITY.value: "toco"},
                            {FILTER_MODES.CATEGORY.value: "i", FILTER_MODES.ARTIST.value: "still", FILTER_MODES.NATIONALITY.value: "standing"}],
            "toAvoid": {FILTER_MODES.CATEGORY.value: ["rapid", "loco"], FILTER_MODES.ARTIST.value: ["brokes"], FILTER_MODES.NATIONALITY.value: []},
            "filters": [FILTER_MODES.CATEGORY, FILTER_MODES.ARTIST, FILTER_MODES.NATIONALITY],
            "expected": [{FILTER_MODES.CATEGORY.value: "i", FILTER_MODES.ARTIST.value: "still", FILTER_MODES.NATIONALITY.value: "standing"}]
            }
        ]

        for test in testData:
            actual = SingularImageSelector.filterByMultipleCriteriaAndValues(test["inputList"], test["toAvoid"], test["filters"])
            self.assertListEqual(actual, test["expected"])
            self.assertDictEqual(actual[0], test["expected"][0])
             
         
    

if __name__ == '__main__':
        unittest.main()