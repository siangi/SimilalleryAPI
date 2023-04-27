import unittest
from database.queryBuilder import imageQueryBuilder

class testQueryBuilder(unittest.TestCase):
    def testImgID(self):
        testCases = (
            {"inputId": 4, "expectedOutput": "WHERE image.idimage = 4"},
            {"inputId": 300, "expectedOutput": "WHERE image.idimage = 300"},
            {"inputId": 70, "expectedOutput": "WHERE image.idimage = 70"},
        )
        for case in testCases:
            builder = imageQueryBuilder()
            builder.imgByID(case["inputId"])
            self.assertEqual(builder.filters, case["expectedOutput"])

    def testSaliencyCenter(self):
        cases = (
            {"input": (2, 98), "expectedOutput": "WHERE (sal_center_x between 0 and 5) and (sal_center_y between 95 and 100)"},
            {"input": (98, 2), "expectedOutput": "WHERE (sal_center_x between 95 and 100) and (sal_center_y between 0 and 5)"}
        )

        for case in cases:
            builder = imageQueryBuilder()
            builder.similarSaliencyCenter(case["input"])
            self.assertEqual(builder.filters, case["expectedOutput"])
    
    def testPaletteRatios(self):
        input = {"pal_ratio_1": 0.0, "pal_ratio_2": 0.95, "pal_ratio_3": 0.5, "pal_ratio_4": 0.22, "pal_ratio_5": 0.768, }
        expectedOutput =  "WHERE (pal_ratio_1 BETWEEN 0 AND 0.1) AND (pal_ratio_2 BETWEEN 0.85 AND 1) AND (pal_ratio_3 BETWEEN 0.4 AND 0.6) AND (pal_ratio_4 BETWEEN 0.12 AND 0.32) AND (pal_ratio_5 BETWEEN 0.668 AND 0.868)"
            
        builder = imageQueryBuilder()
        builder.similarPaletteRatios(input)
        self.maxDiff = None
        self.assertEqual(builder.filters, expectedOutput)

    def testAppendNewClauseSingle(self):
        builder = imageQueryBuilder()
        CLAUSE = "appendTest"
        builder.appendNewFilter(CLAUSE)
        self.assertEqual(builder.filters, f"WHERE {CLAUSE}")

    def testAppendNewClauseMulti(self):
        builder = imageQueryBuilder()
        CLAUSE = "append.Test"
        APPEND_ROUNDS = 4
        for idx in range(APPEND_ROUNDS):
            builder.appendNewFilter(CLAUSE)
        
        self.assertEqual(builder.filters, f"WHERE {CLAUSE} AND {CLAUSE} AND {CLAUSE} AND {CLAUSE}")

    def testSimilarPaletteFullQuery(self):
        palette = ({"h_1": 100, "s_1": 50, "l_1": 50, "h_2": 360, "s_2": 100, "l_2": 100, "h_3": 0, "s_3": 0, "l_3": 0})
        builder = imageQueryBuilder()
        LIMIT = 15
        EXPECTED = """SELECT image.*, artist.name, category.name FROM scheme_test_similallery.image
            INNER JOIN artist ON image.artist_id = artist.idartist INNER JOIN category ON category.idcategory = image.category_id
            WHERE (h_1 BETWEEN 85 AND 115) AND
                (s_1 BETWEEN 40 AND 60) AND
                (l_1 BETWEEN 40 AND 60) AND (h_2 BETWEEN 345 AND 360) AND
                (s_2 BETWEEN 90 AND 100) AND
                (l_2 BETWEEN 90 AND 100) AND (h_3 BETWEEN 0 AND 15) AND
                (s_3 BETWEEN 0 AND 10) AND
                (l_3 BETWEEN 0 AND 10)
            LIMIT 15"""
        actual = builder.similarPalette(palette).buildQuery(LIMIT)
        # i used multiline strings for better readability, so i have to remove all of the whitespace
        # for easier comparison
        cleanExpected = "".join(EXPECTED.split())
        cleanAcutal = "".join(actual.split())
        self.assertEqual(cleanExpected, cleanAcutal)

if __name__ == '__main__':
    unittest.main()