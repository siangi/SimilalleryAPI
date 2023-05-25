from enum import Enum

class FILTER_MODES(Enum):
    CATEGORY: str = "category_name"
    ORIGIN_YEAR: int = "year"
    NATIONALITY: int = "artist_nationality"
    ARTIST: int = "artist_name"

class baseSelectionModel:
    def getMostDifferentImages(baseData: dict, inputList: list, goalLength: int):
        pass