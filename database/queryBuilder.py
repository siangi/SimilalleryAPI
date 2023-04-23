import numpy as np

class imageQueryBuilder:
    conditions: str

    def __init__(self) -> None:
        self.conditions = ""
    
    #returns a query to search for images with conditions  from the member variable. Call this function last
    def buildQuery(self, count: int, fullData: bool = True):
        neededRows = "image.*, artist.name, category.name"
        if not fullData:
            neededRows = "image.idimage, image.title, image.year, image.URL, artist.name, category.name"

        print(self.conditions)
        return f"""SELECT {neededRows} FROM scheme_test_similallery.image 
            INNER JOIN artist ON image.artist_id = artist.idartist 
            INNER JOIN category ON category.idcategory = image.category_id
            {self.conditions}
            LIMIT {count}"""

    def clearConditions(self):
        self.conditions = ""
        return self

    def imgByIDCondition(self, id:int):
        self.appendNewClause(f"image.idimage = {id}")
        return self

    def similarPaletteCondition(self, palette: list):
        H_DIFFERENCE = 10
        S_DIFFERENCE = 7
        L_DIFFERENCE = 7
        MAX_H = 360
        MAX_S = 100
        MAX_L = 100
        SIMILARITY_DEPTH = 3
        for index in range(1, SIMILARITY_DEPTH + 1):
            self.appendNewClause(f"""(h_{index} BETWEEN {max(palette[f"h_{index}"] - H_DIFFERENCE,0)} AND {min(palette[f"h_{index}"] + H_DIFFERENCE, MAX_H)}) AND 
                (s_{index} BETWEEN {max(palette[f"s_{index}"] - S_DIFFERENCE, 0)} AND {min(palette[f"s_{index}"] + S_DIFFERENCE, MAX_S)}) AND 
                (l_{index} BETWEEN {max(palette[f"l_{index}"] - L_DIFFERENCE, 0)} AND {min(palette[f"l_{index}"] + L_DIFFERENCE, MAX_L)})""")
        return self

    def similarPaletteRatiosCondition(self, baseRatios):
        pass

    def similarAngleRatiosCondition(self, baseRatios):
        pass

    def similarSaliencyCenterCondition(self, baseCenter):
        SALIENCY_DIFF = 3
        self.appendNewClause(f"(sal_center_x between {max(baseCenter[0] - SALIENCY_DIFF, 0)} and {min(baseCenter[0] + SALIENCY_DIFF, 100)}) and (sal_center_y between {max(baseCenter[1] - SALIENCY_DIFF, 0)} and {min(baseCenter[1] + SALIENCY_DIFF, 100)})")
        print(self.conditions)
        return self

    def similarSaliencyRectCondition(self, baseRect):
        pass

    def differentMetadataCondition(self, originalMetadata):
        pass

    # connects a new where clause to the member variable. 
    def appendNewClause(self, clause: str):
        if self.conditions.strip() == "":
            self.conditions = f"WHERE {clause}"
        else:
            self.conditions = f"{self.conditions} AND {clause}"







