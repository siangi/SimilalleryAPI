from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.searchModel import similaritySearchModel
from database.searchModel import SEARCH_MODES


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

@app.get("/similars/{imageId}")
async def similarFromExisting(imageId: int):
    searcher = similaritySearchModel()
    similars = searcher.getImageListBySimilarity([SEARCH_MODES.SALIENCY_RECT], 10, imageId)
    return {"message": similars}

