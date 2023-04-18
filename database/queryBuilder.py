import numpy as np

class imageQueryBuilder:
    conditions: str

    def __init__(self) -> None:
        self.conditions = ""
    
    #returns a query to search for images with conditions  from the member variable. Call this function last
    def FullImageDataQuery(self, count: int):
        return f"""SELECT image.*, artist.name, category.name FROM scheme_test_similallery.image 
            INNER JOIN artist ON image.artist_id = artist.idartist 
            INNER JOIN category ON category.idcategory = image.category_id
            {self.conditions}
            LIMIT {count}"""


    def imgByIDCondition(self, id:int):
        self.appendNewClause(f"image.idimage = {id}")
        return self

    def similarPaletteCondition(self, palette: list):
        H_DIFFERENCE = 5
        S_DIFFERENCE = 5
        L_DIFFERENCE = 5
        MAX_H = 360
        MAX_S = 100
        MAX_L = 100
        SIMILARITY_DEPTH = 3
        for index in range(SIMILARITY_DEPTH):
            self.appendNewClause(f"""(h_{index + 1} BETWEEN {max(palette[index]["h"] - H_DIFFERENCE,0)} AND {min(palette[index]["h"] + H_DIFFERENCE, MAX_H)}) AND 
                (s_{index + 1} BETWEEN {max(palette[index]["s"] - S_DIFFERENCE, 0)} AND {min(palette[index]["s"] + S_DIFFERENCE, MAX_S)}) AND 
                (l_{index + 1} BETWEEN {max(palette[index]["l"] - L_DIFFERENCE, 0)} AND {min(palette[index]["l"] + L_DIFFERENCE, MAX_L)})""")
        return self

    def similarPaletteRatiosCondition(self, baseRatios):
        pass

    def similarAngleRatiosCondition(self, baseRatios):
        pass

    def similarSaliencyCenterCondition(self, baseCenter):
        pass

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







