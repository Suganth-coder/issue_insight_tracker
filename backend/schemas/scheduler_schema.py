from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from pydantic import BaseModel
from typing import Optional

Base = declarative_base()

class SchedulerDBSchema(Base):
    __tablename__ = 'daily_stats'
    
    id = Column(Integer, primary_key=True, autoincrement=True)

    date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    total_issues = Column(Integer, nullable=False, default=0)
    total_issues_open = Column(Integer, nullable=False, default=0)
    total_issues_triaged = Column(Integer, nullable=False, default=0)
    total_issues_in_progress = Column(Integer, nullable=False, default=0)
    total_issues_done = Column(Integer, nullable=False, default=0)

    total_issues_severity_low = Column(Integer, nullable=False, default=0)
    total_issues_severity_medium = Column(Integer, nullable=False, default=0)
    total_issues_severity_high = Column(Integer, nullable=False, default=0)
    total_issues_severity_critical = Column(Integer, nullable=False, default=0)

    