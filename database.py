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
    Index,
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    sessionmaker,
)

# Load .env
load_dotenv()

# Configurable via .env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")
SQL_ECHO     = os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"

# Engine & Session factory
engine = create_engine(DATABASE_URL, echo=SQL_ECHO, future=True)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    __table_args__ = (
        # composite index on filename + title for search
        Index("ix_documents_filename_title", "filename", "title"),
    )

    id         = Column(Integer, primary_key=True, index=True)
    filename   = Column(String, unique=True, index=True, nullable=False)
    title      = Column(String, index=True, nullable=True)
    summary    = Column(Text, nullable=True)
    keywords   = Column(Text, nullable=True)
    path       = Column(String, nullable=False)
    source     = Column(String, default="fallback")  # “gpt” or “fallback”
    added_at   = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    thumbnails = relationship(
        "Thumbnail",
        back_populates="document",
        cascade="all, delete-orphan",
        order_by="Thumbnail.created_at",
    )
    conflicts = relationship(
        "Conflict",
        back_populates="document",
        cascade="all, delete-orphan",
        order_by="Conflict.created_at",
    )

class Thumbnail(Base):
    __tablename__ = "thumbnails"
    __table_args__ = (
        Index("ix_thumbnails_docid_created", "document_id", "created_at"),
    )

    id             = Column(Integer, primary_key=True, index=True)
    document_id    = Column(
        Integer,
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    thumbnail_path = Column(String, nullable=False)
    created_at     = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document", back_populates="thumbnails")

class Conflict(Base):
    __tablename__ = "conflicts"
    __table_args__ = (
        Index("ix_conflicts_docid_status", "document_id", "status"),
    )

    id            = Column(Integer, primary_key=True, index=True)
    document_id   = Column(
        Integer,
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    conflict_hash = Column(String, index=True, nullable=False)
    status        = Column(String, default="unresolved")  # “unresolved” / “resolved”
    created_at    = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document", back_populates="conflicts")

def init_db():
    """Create all tables in the database (use Alembic for production!)."""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("✅  Database tables created (or already existed).")
