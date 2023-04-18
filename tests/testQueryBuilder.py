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
            builder.imgByIDCondition(case["inputId"])
            self.assertEqual(builder.conditions, case["expectedOutput"])

    def testAppendNewClauseSingle(self):
        builder = imageQueryBuilder()
        CLAUSE = "appendTest"
        builder.appendNewClause(CLAUSE)
        self.assertEqual(builder.conditions, f"WHERE {CLAUSE}")

    def testAppendNewClauseMulti(self):
        builder = imageQueryBuilder()
        CLAUSE = "append.Test"
        APPENDROUNDS = 4
        for idx in range(APPENDROUNDS):
            builder.appendNewClause(CLAUSE)
        
        self.assertEqual(builder.conditions, f"WHERE {CLAUSE} AND {CLAUSE} AND {CLAUSE} AND {CLAUSE}")

    def testSimilarPaletteFullQuery(self):
        palette = (
                    {"h": 100, "s": 50, "l": 50},
                    {"h": 360, "s": 100, "l": 100},
                    {"h": 0, "s": 0, "l": 0},
                   )
        builder = imageQueryBuilder()
        LIMIT = 15
        EXPECTED = """SELECT image.*, artist.name, category.name FROM scheme_test_similallery.image
            INNER JOIN artist ON image.artist_id = artist.idartist INNER JOIN category ON category.idcategory = image.category_id
            WHERE (h_1 BETWEEN 95 AND 105) AND
                (s_1 BETWEEN 45 AND 55) AND
                (l_1 BETWEEN 45 AND 55) AND (h_2 BETWEEN 355 AND 360) AND
                (s_2 BETWEEN 95 AND 100) AND
                (l_2 BETWEEN 95 AND 100) AND (h_3 BETWEEN 0 AND 5) AND
                (s_3 BETWEEN 0 AND 5) AND
                (l_3 BETWEEN 0 AND 5)
            LIMIT 15"""
        actual = builder.similarPaletteCondition(palette).buildQuery(LIMIT)
        cleanExpected = "".join(EXPECTED.split())
        cleanAcutal = "".join(actual.split())
        self.assertEqual(cleanExpected, cleanAcutal)

if __name__ == '__main__':
    unittest.main()