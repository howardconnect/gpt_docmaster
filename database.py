# database.py

import os
from datetime import datetime
from dotenv import load_dotenv

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Load .env
load_dotenv()

# Get database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

# Create engine and session factory
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base class for models
Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)
    path = Column(String, nullable=False)
    source = Column(String, default="fallback")  # “gpt” or “fallback”
    added_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    thumbnails = relationship("Thumbnail", back_populates="document")
    conflicts = relationship("Conflict", back_populates="document")

class Thumbnail(Base):
    __tablename__ = "thumbnails"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(
        Integer,
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    thumbnail_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document", back_populates="thumbnails")

class Conflict(Base):
    __tablename__ = "conflicts"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(
        Integer,
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    conflict_hash = Column(String, nullable=False)
    status = Column(String, default="unresolved")  # “unresolved” / “resolved”
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document", back_populates="conflicts")

def init_db():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("✅  Database tables created (or already existed).")