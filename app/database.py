from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Setting up SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

# Creating a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for data models
Base = declarative_base()

def init_db():
    # Creating tables if not exist (e.g., using Alembic for migrations)
    Base.metadata.create_all(bind=engine)
