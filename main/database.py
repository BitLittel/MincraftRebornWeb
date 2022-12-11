# -*- coding: utf-8 -*-
from main import main
import hashlib
from sqlalchemy import Column, Integer, create_engine, DateTime, Text, Boolean, String, JSON
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session


def hash_password(password: str) -> str:
    h = hashlib.new('sha256')
    h.update(password.encode('utf-8'))
    return h.hexdigest()


Base = declarative_base()


class Versions(Base):
    __tablename__ = 'Versions'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    data = Column(JSON)


class News(Base):
    __tablename__ = 'News'
    news_id = Column(Integer, primary_key=True, nullable=False)
    datetime = Column(DateTime, default=func.now(), nullable=False)
    title = Column(String(length=255), nullable=False)
    message = Column(Text, nullable=False)
    link = Column(Text, nullable=True)
    visible = Column(Boolean, default=True, nullable=True)


engine = create_engine(
    f'postgresql+psycopg2://{main.config["DATABASE_USER"]}'
    f':{main.config["DATABASE_PASSWORD"]}'
    f'@{main.config["DATABASE_IP"]}'
    f'/{main.config["DATABASE_NAME"]}',
    encoding='utf8', echo=False, pool_recycle=300, query_cache_size=0, pool_pre_ping=True
)

Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker())
Session.configure(bind=engine)
