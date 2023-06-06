from enum import Enum

class FILTER_MODES(Enum):
    CATEGORY: str = "category_name"
    ORIGIN_YEAR: str = "year"
    NATIONALITY: str = "artist_nationality"
    ARTIST: str = "artist_name"

class baseSelectionModel:
    def getMostDifferentImages(baseData: dict, inputList: list, goalLength: int):
        pass