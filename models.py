from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Robot(Base):
    __tablename__ = "robots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    camera = Column(String, index=True)
    wheels = Column(Boolean, index=True)
    battery = Column(Integer, index=True)
    speed = Column(Integer, index=True)
