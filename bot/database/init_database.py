import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker, Session
from database.base import Base
from models import article, stocks, users

load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
MAIN_ENGINE = create_engine(SQLALCHEMY_DATABASE_URI, echo=True, future=True)

if __name__ == "__main__":
    Base.metadata.create_all(MAIN_ENGINE, checkfirst=True)
