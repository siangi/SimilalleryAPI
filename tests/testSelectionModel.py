import unittest
from models.selectionModel import ImageSelector
from models.selectionModel import FILTER_MODES


#most of these tests were written by ChatGPT and controlled by me
class testImageSelecter(unittest.TestCase):
    
    def testFilterMethodSingleCriteria(self):
        basedata = {"category_name": "damnyouactuallyreadmytests"}
        inputList = [
            {"category_name": "test1"},
            {"category_name": "test1"},
            {"category_name": "test1"},
            {"category_name": "test1"},
            {"category_name": "damnyouactuallyreadmytests"},
        ]
        expectedOutput = [
            {"category_name": "test1"},
            {"category_name": "test1"},
            {"category_name": "test1"},
            {"category_name": "test1"},
        ]
        outputList = ImageSelector.filterByMultipleCriteria(basedata, inputList, [FILTER_MODES.CATEGORY])
        self.assertListEqual(outputList, expectedOutput)

    def test_filterByMultipleCriteria(self):
        basedata = {
            'category_name': 'Abstract',
            'year': 2021,
            'artist_nationality': 'USA',
            'artist_name': 'John Doe'
        }
        inputList = [
            {'category_name': 'Abstract', 'year': 2019, 'artist_nationality': 'USA', 'artist_name': 'John Doe'},
            {'category_name': 'Landscape', 'year': 2022, 'artist_nationality': 'UK', 'artist_name': 'Alice Smith'},
            {'category_name': 'Portrait', 'year': 2021, 'artist_nationality': 'USA', 'artist_name': 'Bob Johnson'}
        ]
        filters = [
            FILTER_MODES.CATEGORY,
            FILTER_MODES.ORIGIN_YEAR
        ]
        expected_output = [
            {'category_name': 'Landscape', 'year': 2022, 'artist_nationality': 'UK', 'artist_name': 'Alice Smith'},
        ]

        result = ImageSelector.filterByMultipleCriteria(basedata, inputList, filters)
        self.assertEqual(result, expected_output)

    def test_filterByMultipleCriteria_empty_inputList(self):
        basedata = {
            'category_name': 'Abstract',
            'year': 2021,
            'artist_nationality': 'USA',
            'artist_name': 'John Doe'
        }
        inputList = []
        filters = [
            FILTER_MODES.CATEGORY,
            FILTER_MODES.ORIGIN_YEAR
        ]
        expected_output = []

        result = ImageSelector.filterByMultipleCriteria(basedata, inputList, filters)
        self.assertEqual(result, expected_output)

    def test_filterByMultipleCriteria_empty_filters(self):
        basedata = {
            'category_name': 'Abstract',
            'year': 2021,
            'artist_nationality': 'USA',
            'artist_name': 'John Doe'
        }
        inputList = [
            {'category_name': 'Abstract', 'year': 2021, 'artist_nationality': 'USA', 'artist_name': 'John Doe'},
            {'category_name': 'Landscape', 'year': 2022, 'artist_nationality': 'UK', 'artist_name': 'Alice Smith'},
            {'category_name': 'Portrait', 'year': 2020, 'artist_nationality': 'USA', 'artist_name': 'Bob Johnson'}
        ]
        filters = []
        expected_output = inputList

        result = ImageSelector.filterByMultipleCriteria(basedata, inputList, filters)
        self.assertEqual(result, expected_output)   

    def test_filterByMultipleCriteria_all_filters(self):
        basedata = {
            'category_name': 'Abstract',
            'year': 2021,
            'artist_nationality': 'USA',
            'artist_name': 'John Doe'
        }
        inputList = [
            {'category_name': 'Abstract', 'year': 2021, 'artist_nationality': 'USA', 'artist_name': 'John Doe'},
            {'category_name': 'Figurative', 'year': 2021, 'artist_nationality': 'UK', 'artist_name': 'Charlie Brown'},
            {'category_name': 'Landscape', 'year': 2024, 'artist_nationality': 'USA', 'artist_name': 'David Lee'},
            {'category_name': 'Portrait', 'year': 2023, 'artist_nationality': 'UK', 'artist_name': 'John Doe'},
            {'category_name': 'Landscape', 'year': 2022, 'artist_nationality': 'UK', 'artist_name': 'Alice Smith'},
            {'category_name': 'Portrait', 'year': 2023, 'artist_nationality': 'CH', 'artist_name': 'Bob Johnson'},                     
            
        ]
        filters = [
            FILTER_MODES.CATEGORY,
            FILTER_MODES.ORIGIN_YEAR,
            FILTER_MODES.NATIONALITY,
            FILTER_MODES.ARTIST
        ]
        expected_output = [
            {'category_name': 'Landscape', 'year': 2022, 'artist_nationality': 'UK', 'artist_name': 'Alice Smith'},
            {'category_name': 'Portrait', 'year': 2023, 'artist_nationality': 'CH', 'artist_name': 'Bob Johnson'},  
                 
        ]

        result = ImageSelector.filterByMultipleCriteria(basedata, inputList, filters)
        self.assertEqual(result, expected_output)
    
    def test_getMostDifferentImages(self):
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
            {'category_name': 'Portrait', 'year': 2023, 'artist_nationality': 'UK', 'artist_name': 'Eva Green'}
        ]

        expectedOutput = [
             {'category_name': 'Landscape', 'year': 2022, 'artist_nationality': 'UK', 'artist_name': 'Alice Smith'},
             {'category_name': 'Portrait', 'year': 2023, 'artist_nationality': 'UK', 'artist_name': 'Eva Green'},
             {'category_name': 'Abstract', 'year': 2021, 'artist_nationality': 'UK', 'artist_name': 'Charlie Brown'},
        ]
        goalLength = 3

        # Test that the output list has the correct length
        outputList = ImageSelector.getMostDifferentImages(basedata, inputList, goalLength)
        self.assertListEqual(outputList, expectedOutput)
        
        # Test that an exception is raised when goalLength is greater than the number of input images
        with self.assertRaises(Exception):
            ImageSelector.getMostDifferentImages(basedata, inputList, len(inputList)+1)




if __name__ == '__main__':
    unittest.main()