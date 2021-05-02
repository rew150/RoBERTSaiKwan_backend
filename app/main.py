from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm.session import Session
from dotenv import load_dotenv

load_dotenv()

from .database import SessionLocal, engine
from . import crud_utils, models, schemas
from .model.wangchanberta_qa import predict

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

@app.get('/ex')
def ex():
    aaa = '''ราชกิจจานุเบกษา เผยแพร่ข้อกำหนด-มาตรการควบคุมพื้นที่ทั่วประเทศใหม่ พื้นที่ควบคุมสูงสุดและเข้มงวด 6 จังหวัดหนักสุด มีผลบังคับใช้ตั้งแต่ 1 พ.ค. นี้เป็นต้นไป เผยกรณีพบคนไม่สวมใส่หน้ากาก เจ้าหน้าที่สามารถกล่าวตักเตือนได้ ก่อนที่จะใช้กฎหมายตามพระราชบัญญัติโรคติดต่อ พ.ศ.2558

เมื่อวันที่ 29 เมษายน 2564  ผู้สื่อข่าวรายงานว่า เว็บไชต์ราชกิจจานุเษกษาได้ เผยแพร่ ข้อกำหนดออกตาความในมาตรา 9 แห่งพระราชกำหนดการบริหารราชการในสถานการณ์ฉุกเฉิน พ.ศ.2548 (ฉบับที่ 22)

ประกาศฉบับดังกล่าวมีสาระสำคัญตามที่ ศูนย์บริหารสถานการณ์แพร่ระบาดของโรคติดต่อเชื้อไวรัสโคโรนา 2019 (ศบค.) ศบค.แถลงในวันนี้ โดยยกระดับมาตรการการควบคุมการแพร่ระบาดของโรคโควิด-19 ใหม่ หลังสถานการณ์การแพร่ระบาดยังเพิ่มขึ้นอย่างต่อเนื่อง โดยเฉพาะพื้นที่กทม.และปริมณฑล

โดยกำหนดพื้นที่ควบคุมใหม่ เพื่อปรับระดับการกำหนดพื้นที่และ มาตรการการบังคับใช้ คือ 1.พื้นที่ควบคุมสูงสุดและเข้มงวด 6 จังหวัด (สีแดงเข้ม) ได้แก่พื้นที่กรุงเทพมหานคร(กทม.) ชลบุรี นนทบุรี เชียงใหม่ สมุทรปราการ ปทุมธานี 2.พื้นที่ควบคุมสูงสุด (สีแดง) 45 จังหวัด และ 3.พื้นที่ควบคุม (สีส้ม) 26 จังหวัด
'''
    return predict(aaa)

app.mount("/", StaticFiles(directory='public', html=True), name="static")
