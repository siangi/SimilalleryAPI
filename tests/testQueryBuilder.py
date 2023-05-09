import unittest
from database.queryBuilder import imageQueryBuilder
from decimal import *

class testQueryBuilder(unittest.TestCase):
    def testImgID(self):
        testCases = (
            {"inputId": 4, "expectedOutput": ["image.idimage = 4"]},
            {"inputId": 300, "expectedOutput": ["image.idimage = 300"]},
            {"inputId": 70, "expectedOutput": ["image.idimage = 70"]},
        )
        for case in testCases:
            builder = imageQueryBuilder()
            builder.imgByID(case["inputId"])
            self.assertEqual(builder.filters, case["expectedOutput"])

    def testSaliencyCenter(self):
        cases = (
            {"input": (2, 98), "expectedOutput": ["(sal_center_x between 0 and 5) and (sal_center_y between 95 and 100)"]},
            {"input": (98, 2), "expectedOutput": ["(sal_center_x between 95 and 100) and (sal_center_y between 0 and 5)"]}
        )
        for case in cases:
            builder = imageQueryBuilder()
            builder.similarSaliencyCenter(case["input"])
            self.assertEqual(builder.filters, case["expectedOutput"])
    
    def testPaletteRatios(self):
        input = {"pal_ratio_1": Decimal("0.0"), "pal_ratio_2": Decimal("0.95"), "pal_ratio_3": Decimal("0.5"), "pal_ratio_4": Decimal("0.22"), "pal_ratio_5": Decimal("0.768"), }
        expectedOutput =  ["(pal_ratio_1 BETWEEN 0 AND 0.100)","(pal_ratio_2 BETWEEN 0.850 AND 1)","(pal_ratio_3 BETWEEN 0.400 AND 0.600)","(pal_ratio_4 BETWEEN 0.120 AND 0.320)","(pal_ratio_5 BETWEEN 0.668 AND 0.868)"]
            
        builder = imageQueryBuilder()
        builder.similarPaletteRatios(input)
        self.maxDiff = None
        self.assertEqual(builder.filters, expectedOutput)

    def testEuclidianDistanceColumn(self):
        input = {"values": [0, 1, 2], "columns": ["test_1", "test_2", "test_3"], "name": "test_name"}
        expected = "round(sqrt(pow(0 - test_1, 2) + pow(1 - test_2, 2) + pow(2 - test_3, 2)), 2) as test_name"

        builder = imageQueryBuilder()
        builder.euclidianDistanceFakeColumn(input["values"], input["columns"], input["name"])
        self.assertTrue(expected in builder.columns)

    def testNewSorting(self):
        input = [{"col": "test_col", "isAscending": False}, {"col": "test_col2", "isAscending": True}]
        expected = ["test_col DESC", "test_col2 ASC"]

        builder = imageQueryBuilder()
        builder.appendNewSorting(input[0]["col"], input[0]["isAscending"])
        builder.appendNewSorting(input[1]["col"], input[1]["isAscending"])
        self.assertListEqual(builder.sorting, expected)

    def testSimilarPaletteFullQuery(self):
        palette = ({"h_1": 100, "s_1": 50, "l_1": 50, "h_2": 360, "s_2": 100, "l_2": 100, "h_3": 0, "s_3": 0, "l_3": 0})
        builder = imageQueryBuilder()
        LIMIT = 15
        EXPECTED = """SELECT image.*, artist.name as artist_name, category.name as category_name FROM scheme_test_similallery.image
            INNER JOIN artist ON image.artist_id = artist.idartist INNER JOIN category ON category.idcategory = image.category_id
            WHERE (h_1 BETWEEN 85 AND 115) AND
                (s_1 BETWEEN 40 AND 60) AND
                (l_1 BETWEEN 40 AND 60) AND (h_2 BETWEEN 345 AND 360) AND
                (s_2 BETWEEN 90 AND 100) AND
                (l_2 BETWEEN 90 AND 100) AND (h_3 BETWEEN 0 AND 15) AND
                (s_3 BETWEEN 0 AND 10) AND
                (l_3 BETWEEN 0 AND 10)
            ORDER BY image.idimage ASC
            LIMIT 15"""
        actual = builder.similarPalette(palette).appendNewSorting("image.idimage", True).buildQuery(LIMIT)
    
        # i used multiline strings for better readability, so i have to remove all of the whitespace
        # for easier comparison
        cleanExpected = "".join(EXPECTED.split())
        cleanAcutal = "".join(actual.split())
        self.assertEqual(cleanExpected, cleanAcutal)

if __name__ == '__main__':
    unittest.main()