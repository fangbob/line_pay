from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from modles.database import Base
import uuid
class Appointment(Base):
    __tablename__ = 'appointment'
    id = Column(String(50), primary_key=True)
    user_id=Column(String(50),ForeignKey('users.id'))
    appointment_service=Column(String(50),nullable=False)
    appointment_datetime=Column(DateTime(),nullable=False)
    def __init__(self,user_id,appointment_service,appointment_datetime):
        self.id = str(uuid.uuid4())
        self.user_id=user_id
        self.appointment_service=appointment_service
        self.appointment_datetime=appointment_datetime
    def __repr__(self):
        return '<User %r>' % (self.name)
