import numpy as np
from decimal import *

class imageQueryBuilder:
    columns: list
    filters: list
    sorting: list

    def __init__(self) -> None:
        self.filters = []
        self.columns = []
        self.sorting = []
    
    #returns a query to search for images with conditions  from the member variable. Call this function last
    def buildQuery(self, count: int, fullData: bool = True):
        if fullData:
            self.columns.extend(["image.*", "artist.name as artist_name" , "artist.nationalityID as artist_nationality","category.name as category_name"])
        if not fullData:
            self.columns.extend(["image.idimage","image.title","image.year","image.URL","artist.name as artist_name", "artist.nationalityID as artist_nationality","category.name as category_name"])

        return f"""SELECT {",".join(self.columns)} FROM scheme_test_similallery.image 
            INNER JOIN artist ON image.artist_id = artist.idartist 
            INNER JOIN category ON category.idcategory = image.category_id
            {"WHERE " + "AND".join(self.filters) if len(self.filters) > 0 else "" }
            {'ORDER BY ' + ', '.join(self.sorting) if len(self.sorting) > 0 else 'ORDER BY image.idimage'}
            LIMIT {count}"""

    def clearConditions(self):
        self.filters = []
        self.sorting = []
        return self

    def imgByID(self, id:int):
        self.filters.append(f"image.idimage = {id}")
        return self

    def similarPalette(self, palette: dict):
        H_DIFFERENCE = 20
        S_DIFFERENCE = 20
        L_DIFFERENCE = 20
        MAX_H = 360
        MAX_S = 100
        MAX_L = 100
        SIMILARITY_DEPTH = 3

        for index in range(1, SIMILARITY_DEPTH + 1):
            h_min = max(palette[f"h_{index}"] - H_DIFFERENCE,0)
            h_max = min(palette[f"h_{index}"] + H_DIFFERENCE, MAX_H)
            s_min = max(palette[f"s_{index}"] - S_DIFFERENCE, 0)
            s_max = min(palette[f"s_{index}"] + S_DIFFERENCE, MAX_S)
            l_min = max(palette[f"l_{index}"] - L_DIFFERENCE, 0)
            l_max = min(palette[f"l_{index}"] + L_DIFFERENCE, MAX_L)
            self.filters.append(f"""(h_{index} BETWEEN {h_min} AND {h_max}) AND 
                (s_{index} BETWEEN {s_min} AND {s_max}) AND 
                (l_{index} BETWEEN {l_min} AND {l_max})""")
            
        return self
    
    def paletteSorting(self, palette: dict):
        SIMILARITY_DEPTH = 3

        for index in range(1, SIMILARITY_DEPTH + 1):
            COL_NAME = f"palette_similarity_{index}"
            self.euclidianDistanceFakeColumn(
                [palette[f"h_{index}"], palette[f"s_{index}"], palette[f"l_{index}"]],
                [f"h_{index}", f"s_{index}", f"l_{index}"],
                COL_NAME
            )
            self.appendNewSorting(COL_NAME, True)

        return self

    def similarPaletteRatios(self, baseRatios: dict):
        RATIO_DIFF = Decimal(0.1)
        SIMILARITY_DEPTH = 5
        RATIO_MAX = 1
        
        for index in range(1, SIMILARITY_DEPTH + 1):
            colName = f"pal_ratio_{index}"
            ratio_min = round(max(baseRatios[colName] - RATIO_DIFF, 0), 3)  
            ratio_max = round(min(baseRatios[colName] + RATIO_DIFF, RATIO_MAX), 3)
            self.filters.append(f"({colName} BETWEEN {ratio_min} AND {ratio_max})""")

        return self
    
    
    def paletteRatioSorting(self, baseRatios: dict):
        COL_NAME = "palette_ratio_similarity"
        self.euclidianDistanceFakeColumn(
            [baseRatios["pal_ratio_1"], baseRatios["pal_ratio_2"], baseRatios["pal_ratio_3"], baseRatios["pal_ratio_4"], baseRatios["pal_ratio_5"]],
            ["pal_ratio_1", "pal_ratio_2", "pal_ratio_3", "pal_ratio_4", "pal_ratio_5"],
            COL_NAME)
        self.appendNewSorting(COL_NAME, True)


    def similarAngleRatios(self, baseRatios):
        RATIO_DIFF = Decimal(0.1)
        SIMILARITY_DEPTH = 7

        for index in range(1, SIMILARITY_DEPTH + 1):
            colName = f"angle_ratio_{index}"
            minRatio = round(max(baseRatios[colName] - RATIO_DIFF,0), 3 )
            maxRatio = round(min(baseRatios[colName] + RATIO_DIFF, 1), 3)
            self.filters.append(f"({colName} BETWEEN {minRatio} AND {maxRatio})")
        
        return self

    def angleRatioSorting(self, baseRatios):
        COL_NAME = "angle_ratio_similarity"
        self.euclidianDistanceFakeColumn([
            baseRatios["angle_ratio_1"],
            baseRatios["angle_ratio_2"],
            baseRatios["angle_ratio_3"],
            baseRatios["angle_ratio_4"],
            baseRatios["angle_ratio_5"],
            baseRatios["angle_ratio_6"],
            baseRatios["angle_ratio_7"],
            baseRatios["angle_ratio_8"],
        ], 
        ["angle_ratio_1", "angle_ratio_2", "angle_ratio_3", "angle_ratio_4", "angle_ratio_5", "angle_ratio_6", "angle_ratio_7", "angle_ratio_8"],
        "angle_ratio_similarity")
        self.appendNewSorting(COL_NAME, True)
        return self
    
    def similarSaliencyCenter(self, baseCenter: tuple):
        SALIENCY_DIFF = 3
        x_min = max(baseCenter[0] - SALIENCY_DIFF, 0)
        x_max = min(baseCenter[0] + SALIENCY_DIFF, 100)
        y_min = max(baseCenter[1] - SALIENCY_DIFF, 0)
        y_max = min(baseCenter[1] + SALIENCY_DIFF, 100)
        self.filters.append(f"(sal_center_x between {x_min} and {x_max}) and (sal_center_y between {y_min} and {y_max})")
        return self
    
    def saliencyCenterSorting(self, baseCenter: tuple):
        COL_NAME = "sal_center_similarity"
        self.euclidianDistanceFakeColumn(baseCenter, ["sal_center_x", "sal_center_y"], COL_NAME)
        self.appendNewSorting(COL_NAME, True)
        return self

    def similarSaliencyRect(self, baseRect: dict):
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

        self.filters.append(f"(sal_rect_x BETWEEN {rectXmin} AND {rectXmax})")
        self.filters.append(f"(sal_rect_y BETWEEN {rectYmin} AND {rectYmax})")
        self.filters.append(f"(sal_rect_width BETWEEN {rectWidthMin} AND {rectWidthMax})")
        self.filters.append(f"(sal_rect_height BETWEEN {rectHeightMin} AND {rectHeightMax})")
    
        return self
    
    def saliencyRectSorting(self, baseRect: dict):
        COL_NAME = "sal_rect_similarity"
        self.euclidianDistanceFakeColumn([baseRect["sal_rect_x"], baseRect["sal_rect_y"], baseRect["sal_rect_width"], baseRect["sal_rect_height"]],
            ["sal_rect_x", "sal_rect_y", "sal_rect_width", "sal_rect_height"], COL_NAME)
        self.appendNewSorting(COL_NAME, True)
        return self
        
    def randomIdSorting(self):
        self.appendNewSorting("RAND()", True)
        return self

    # creates a fake column for with a euclidian distance value. Columns are compared with an explicit value,
    # so values and columns need to correlate. Outputname is the Name of the fake column.
    def euclidianDistanceFakeColumn(self, values, columns, outputName):
        if (len(values) != len(columns)):
            raise Exception("unequal Values and Columns in euclidian Distance" + str(values) + str(columns))

        factors = []
        for idx in range(0, len(values)):
            factors.append(f"pow({values[idx]} - {columns[idx]}, 2)")

        self.columns.append(f"round(sqrt({' + '.join(factors)}), 2) as {outputName}")
        return self


    def notMainImg(self, mainID):
        self.filters.append(f"(NOT idimage = {mainID})")
        return self

    # writes a new where clause to the member variable.     
    def appendNewSorting(self, col: str, isAscending: bool):
        if isAscending:
            self.sorting.append(col + " ASC")
        else:
            self.sorting.append(col + " DESC")

        return self

if __name__ == "__main__":
    builder = imageQueryBuilder()
    print(builder
          .similarSaliencyCenter((35, 35))
          .euclidianDistanceFakeColumn([35, 35], ["sal_center_x", "sal_center_y"], "saliency_distance")
          .appendNewSorting("saliency_distance", True)
          .buildQuery(15, True))




