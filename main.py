from typing import Annotated
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from database.searchModel import similaritySearchModel
from database.searchModel import SEARCH_MODES
from models.similarsRequest import SimilarsRequest


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
async def similarFromExisting(baseId: int, similarityCriteria: Annotated[list[int]| None, Query()] = None):
    print(baseId, similarityCriteria)
    searcher = similaritySearchModel()
    similars = searcher.getImageListBySimilarity(similarityCriteria, 10, baseId)
    return {"message": similars}