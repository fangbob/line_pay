from sqlalchemy import Column, Integer, String, DateTime
from modles.database import Base
import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(String(50), primary_key=True)
    created_time = Column(DateTime(), nullable=False)

    def __init__(self, id):
        self.id = id
        self.created_time = datetime.datetime.now()

    def __repr__(self):
        return '<User %r>' % (self.name)
