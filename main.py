from fastapi import FastAPI
from database.searchModel import similaritySearchModel
from database.searchModel import SEARCH_MODES

#start with uvicorn main:app --reload
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/similars/{imageId}")
async def similarFromExisting(imageId: int):
    searcher = similaritySearchModel()
    similars = searcher.getImageListBySimilarity([SEARCH_MODES.PALETTE], 4, imageId)
    return {"message": similars}

