from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from .database import Base
import time

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    object_id = Column(Integer)
    duration = Column(Integer)
    timestamp = Column(Integer, default=round(time.time()))
    status = Column(String, default="PENDDING")
