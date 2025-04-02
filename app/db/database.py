from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from logger_config import get_logger

# Initialize logger
logger = get_logger(__name__)

DATABASE_URL = "sqlite:///./users.db"

logger.info("Initializing database engine.")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    logger.info("Creating a new database session.")
    db = SessionLocal()
    try:
        yield db
    finally:
        logger.info("Closing the database session.")
        db.close()