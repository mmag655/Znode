import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_STRING = os.getenv("DB_STRING", "")

# Create the engine for PostgreSQL
engine = create_engine(DB_STRING, pool_pre_ping=True, pool_recycle=3600)

# Create a sessionmaker for working with the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base class for models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
