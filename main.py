from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/similars/{imageId}")
async def similarFromExisting(imageId: int):
    return {"message": str(imageId)}
