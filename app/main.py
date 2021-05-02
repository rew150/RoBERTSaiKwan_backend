from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm.session import Session
from .database import SessionLocal, engine
from . import crud_utils, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/hello")
async def root():
    return {"message": "Hello, World"}

@app.get("/news", response_model=List[schemas.BaseNews])
def get_names(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    names = crud_utils.get_all_names(db, skip=skip, limit=limit)
    return names

@app.get("/news/{name}", response_model=schemas.News)
def get_news(name: str, db: Session = Depends(get_db)):
    db_news = crud_utils.get_news_by_name(db, name=name)
    if db_news is None:
        raise HTTPException(status_code=404, detail='News not found')
    return db_news

@app.post("/news", response_model=schemas.News)
def create_news(news: schemas.News, db: Session = Depends(get_db)):
    db_news = crud_utils.get_news_by_name(db, name=news.name)
    if db_news:
        raise HTTPException(status_code=409, detail='Name conflict')
    return crud_utils.create_news(db, news=news)

app.mount("/", StaticFiles(directory='public', html=True), name="static")
