from sqlalchemy.orm import sessionmaker, Session
from database.init_database import MAIN_ENGINE


def create_session(default_engine=True, custom_engine=None):
    """
    Creates session for SQLAlchemy
    """
    if default_engine:
        Session = sessionmaker(bind=MAIN_ENGINE)
    else:
        Session = sessionmaker(bind=custom_engine)
    session = Session()
    return session
