import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from bot.config import config

os.makedirs("data", exist_ok=True)


engine = create_engine(config.sqlalchemy_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)
