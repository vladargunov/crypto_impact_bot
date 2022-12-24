from sqlalchemy import Column, Integer, String, Float, Time
from database.base import Base


class Article(Base):
    __tablename__ = "articles"

    # Table columns
    id = Column(Integer, primary_key=True)
    news_url = Column(String(200))
    title = Column(String(200))
    time = Column(Integer)
    source_name = Column(String(30))
    tickers = Column(String(200))

    def __repr__(self):
        repr_str = (
            f"Article(id={self.id}, news_url={self.news_url}), "
            + f"title={self.title}, source_name={self.source_name}"
            + f"time={self.time}, tickers={self.tickers}"
        )
        return repr_str
