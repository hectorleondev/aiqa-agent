# db/models.py
from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    issue_key = Column(String(255), nullable=False, index=True)
    body = Column(String, nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    start_date = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    end_date = Column(DateTime(timezone=True), nullable=True)

    # Create explicit index on issue_key for better query performance
    __table_args__ = (Index("ix_messages_issue_key", "issue_key"),)

    def __repr__(self):
        return f"<Message(id={self.id}, issue_key='{self.issue_key}', status='{self.status}')>"
