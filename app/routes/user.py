from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.utils.hashing import get_password_hash
from logger_config import get_logger

# Initialize logger
logger = get_logger(__name__)

router = APIRouter()

@router.post("/signup")
def signup(username: str, password: str, db: Session = Depends(get_db)):
    """
    Endpoint to create a new user.
    Args:
        username (str): The username of the new user.
        password (str): The password of the new user.
        db (Session): The database session.
    Returns:
        dict: A success message.
    """
    logger.info(f"Signup endpoint called for username: {username}.")
    try:
        # Check if the username already exists
        user = db.query(User).filter(User.username == username).first()
        if user:
            logger.warning(f"Username '{username}' is already registered.")
            raise HTTPException(status_code=400, detail="Username already registered")

        # Hash the password and create a new user
        logger.info(f"Hashing password for username: {username}.")
        hashed_password = get_password_hash(password)
        new_user = User(username=username, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"User '{username}' created successfully.")
        return {"message": "User created successfully"}
    except Exception as e:
        logger.error(f"An error occurred during signup for username '{username}': {e}")
        raise HTTPException(status_code=500, detail="An error occurred during signup.")