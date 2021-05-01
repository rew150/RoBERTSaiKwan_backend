from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get("/hello")
async def root():
    return {"message": "Hello, World"}

app.mount("/", StaticFiles(directory='public', html=True), name="static")
