from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from fastapi import HTTPException, status
import os
from dotenv import load_dotenv
from logger_config import get_logger

# Load environment variables
load_dotenv()

# Initialize logger
logger = get_logger(__name__)

# Constants
SECRET_KEY = os.getenv(key="SECRET_KEY")
ALGORITHM = os.getenv(key="ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

def create_access_token(data: dict):
    """
    Creates a JWT access token.
    Args:
        data (dict): The data to encode in the token.
    Returns:
        str: The encoded JWT token.
    """
    logger.info("Creating access token.")
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.info("Access token created successfully.")
        return token
    except Exception as e:
        logger.error(f"An error occurred while creating access token: {e}")
        raise

def decode_access_token(token: str):
    """
    Decodes and validates a JWT access token.
    Args:
        token (str): The JWT token to decode.
    Returns:
        str: The username extracted from the token.
    """
    logger.info("Decoding access token.")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.warning("Token validation failed: 'sub' field is missing.")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
            )
        logger.info(f"Token successfully decoded for user: {username}.")
        return username
    except JWTError as e:
        logger.error(f"Token decoding failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
        )