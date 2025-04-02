from passlib.context import CryptContext
from logger_config import get_logger

# Initialize logger
logger = get_logger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    logger.info("Verifying password.")
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    logger.info("Hashing password.")
    return pwd_context.hash(password)