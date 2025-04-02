from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.utils.token import decode_access_token
from logger_config import get_logger

# Initialize logger
logger = get_logger(__name__)

router = APIRouter()

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.get("/test_auth")
def protected_route(token: str = Depends(oauth2_scheme)):
    logger.info("Protected route '/test_auth' called.")
    try:
        # Decode and validate the token
        username = decode_access_token(token)
        logger.info(f"Token successfully validated for user: {username}.")
        return {"message": f"Hello, {username}. You are authenticated!"}
    except HTTPException as e:
        logger.error(f"Token validation failed: {e.detail}")
        # Raise 403 Unauthorized if token is invalid
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or expired token"
        )