from typing import Annotated
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from models.searchModel import similaritySearchModel
from models.searchModel import SEARCH_MODES

BASE_GROUP_SIZE = 15
#start with uvicorn main:app --reload
app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/similars/")
async def similarFromExisting(baseId: int, imageCount: int, similarityCriteria: Annotated[list[int]| None, Query()] = None):
    countPerCategory = (imageCount / len(similarityCriteria)).__floor__()
    searcher = similaritySearchModel()
    similars = searcher.getImageListBySimilarity(similarityCriteria, countPerCategory, baseId, "singular")
    return {"message": similars}

if __name__ == "__main__":
    model = similaritySearchModel()
    similars = model.getImageListBySimilarity([0], 25, 70717)
    print(len(similars))