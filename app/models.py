from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from .database import Base

class News(Base):
    __tablename__ = "news"

    name = Column(String, primary_key=True, index=True)
    textbody = Column(String)
    summary = Column(String)
