from pydantic import BaseModel

class BaseNews(BaseModel):
    name: str

class News(BaseNews):
    textbody: str
    summary: str

    class Config:
        orm_mode = True
