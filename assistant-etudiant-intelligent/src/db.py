from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")

# For SQLite, need check_same_thread=False for FastAPI multi-threaded server
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    # Imported inside to avoid circular import at module load
    from .models_db import Student, Conversation, Message, QuestionMetric, UserSessionDB  # noqa: F401
    Base.metadata.create_all(bind=engine)

