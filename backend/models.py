from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func

from .database import Base


class ScoreResult(Base):
    __tablename__ = "score_results"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    final_score = Column(Float, nullable=False)
    breakdown = Column(JSON, nullable=False)
    job_description = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )