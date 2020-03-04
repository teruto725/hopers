from sqlalchemy import Column, Integer, String, Text, DateTime
from app.models.database import Base
from datetime import datetime


class Member(Base):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    twitter = Column(String(128), unique=True)

    def __init__(self, name=None, twitter=None):
        self.name = name
        self.twitter = twitter

    def __repr__(self):
        return '<Title %r>' % (self.name)

#以下を追加
class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    date = Column(String(128), unique=True)
    text = Column(String(256), unique=True)

    def __init__(self, date=None, text=None):
        self.date = date
        self.text = text

    def __repr__(self):
        return '<Name %r>' % (self.date)