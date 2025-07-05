from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class IssueSchema(Base):
    __tablename__ = 'issues'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    issue_id = Column(String, unique=True, nullable=False)
    created_by = Column(String, nullable=False)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False)
    severity = Column(String, nullable=True)
    s3_object_key = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
