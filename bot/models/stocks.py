from sqlalchemy import Column, Integer, String, Float, Time
from database.base import Base


class Stocks(Base):
    __tablename__ = "stocks"

    # Table columns
    id = Column(Integer, primary_key=True)
    time = Column(Integer)
    BTC = Column(Float(4))
    ETH = Column(Float(4))
    XRP = Column(Float(4))

    def __repr__(self):
        repr_str = (
            f"Stocks(id={self.id}, time={self.time}), "
            + f"btc={self.btc}, eth={self.eth}"
            + f"xrp={self.xrp})"
        )
        return repr_str
