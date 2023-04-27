import numpy as np
from decimal import *

class imageQueryBuilder:
    filters: str

    def __init__(self) -> None:
        self.filters = ""
    
    #returns a query to search for images with conditions  from the member variable. Call this function last
    def buildQuery(self, count: int, fullData: bool = True):
        neededRows = "image.*, artist.name, category.name"
        if not fullData:
            neededRows = "image.idimage, image.title, image.year, image.URL, artist.name, category.name"

        return f"""SELECT {neededRows} FROM scheme_test_similallery.image 
            INNER JOIN artist ON image.artist_id = artist.idartist 
            INNER JOIN category ON category.idcategory = image.category_id
            {self.filters}
            LIMIT {count}"""

    def clearConditions(self):
        self.filters = ""
        return self

    def imgByID(self, id:int):
        self.appendNewFilter(f"image.idimage = {id}")
        return self

    def similarPalette(self, palette: dict):
        H_DIFFERENCE = 15
        S_DIFFERENCE = 10
        L_DIFFERENCE = 10
        MAX_H = 360
        MAX_S = 100
        MAX_L = 100
        SIMILARITY_DEPTH = 3
        for index in range(1, SIMILARITY_DEPTH + 1):
            self.appendNewFilter(f"""(h_{index} BETWEEN {max(palette[f"h_{index}"] - H_DIFFERENCE,0)} AND {min(palette[f"h_{index}"] + H_DIFFERENCE, MAX_H)}) AND 
                (s_{index} BETWEEN {max(palette[f"s_{index}"] - S_DIFFERENCE, 0)} AND {min(palette[f"s_{index}"] + S_DIFFERENCE, MAX_S)}) AND 
                (l_{index} BETWEEN {max(palette[f"l_{index}"] - L_DIFFERENCE, 0)} AND {min(palette[f"l_{index}"] + L_DIFFERENCE, MAX_L)})""")
        return self

    def similarPaletteRatios(self, baseRatios: dict):
        RATIO_DIFF = Decimal(0.1)
        SIMILARITY_DEPTH = 5
        RATIO_MAX = 1
        
        for index in range(1, SIMILARITY_DEPTH + 1):
            colName = f"pal_ratio_{index}"
            self.appendNewFilter(f"({colName} BETWEEN {max(baseRatios[colName] - RATIO_DIFF, 0)} AND {min(baseRatios[colName] + RATIO_DIFF, RATIO_MAX)})""")

        return self

    def similarAngleRatios(self, baseRatios):
        RATIO_DIFF = Decimal(0.1)
        SIMILARITY_DEPTH = 7
        RATIO_MAX = 1

        for index in range(1, SIMILARITY_DEPTH + 1):
            colName = f"angle_ratio_{index}"
            self.appendNewFilter(f"({colName} BETWEEN {max(baseRatios[colName] - RATIO_DIFF,0)} AND {min(baseRatios[colName] + RATIO_DIFF, 1)})")
        pass

    def similarSaliencyCenter(self, baseCenter):
        SALIENCY_DIFF = 3
        self.appendNewFilter(f"(sal_center_x between {max(baseCenter[0] - SALIENCY_DIFF, 0)} and {min(baseCenter[0] + SALIENCY_DIFF, 100)}) and (sal_center_y between {max(baseCenter[1] - SALIENCY_DIFF, 0)} and {min(baseCenter[1] + SALIENCY_DIFF, 100)})")
        return self

    def similarSaliencyRect(self, baseRect):
        RECT_DIFF = 5
        MIN_VAL = 0
        MAX_VAL = 100
        rectXmin = max(baseRect["sal_rect_x"] - RECT_DIFF, MIN_VAL)
        rectXmax = min(baseRect["sal_rect_x"] + RECT_DIFF, MAX_VAL)
        rectYmin = max(baseRect["sal_rect_y"] - RECT_DIFF, MIN_VAL)
        rectYmax = min(baseRect["sal_rect_y"] + RECT_DIFF, MAX_VAL)
        rectWidthMin = max(baseRect["sal_rect_width"] - RECT_DIFF, MIN_VAL)
        rectWidthMax = min(baseRect["sal_rect_width"] + RECT_DIFF, MAX_VAL)
        rectHeightMin = max(baseRect["sal_rect_height"] - RECT_DIFF, MIN_VAL)
        rectHeightMax = min(baseRect["sal_rect_height"] + RECT_DIFF, MAX_VAL)

        self.appendNewFilter(f"(sal_rect_x BETWEEN {rectXmin} AND {rectXmax})")
        self.appendNewFilter(f"(sal_rect_y BETWEEN {rectYmin} AND {rectYmax})")
        self.appendNewFilter(f"(sal_rect_width BETWEEN {rectWidthMin} AND {rectWidthMax})")
        self.appendNewFilter(f"(sal_rect_height BETWEEN {rectHeightMin} AND {rectHeightMax})")

        return self

    def differentMetadata(self, originalMetadata):
        pass

    def notMainImg(self, mainID):
        self.appendNewFilter(f"(NOT idimage = {mainID})")
        return self

    # writes a new where clause to the member variable. 
    def appendNewFilter(self, clause: str):
        if self.filters.strip() == "":
            self.filters = f"WHERE {clause}"
        else:
            self.filters = f"{self.filters} AND {clause}"
    
    def appendNewOrdering(self, clause: str):
        return self








