from sqlalchemy.orm import Session
from . import models, schemas

def get_all_names(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.News.name).offset(skip).limit(limit).all()

def get_news_by_name(db: Session, name: str):
    return db.query(models.News).filter(models.News.name == name).first()

def create_news(db: Session, news: schemas.News):
    db_news = models.News(**news.dict())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news
