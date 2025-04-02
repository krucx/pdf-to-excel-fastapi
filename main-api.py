import uvicorn
from fastapi import FastAPI
from app.routes import auth, user, protected, pdf_parser
from app.db.database import Base, engine
from logger_config import get_logger

# Initialize logger
logger = get_logger(__name__)

# Initialize database
logger.info("Creating database tables.")

# Initialize database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()
logger.info("FastAPI application initialized.")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(protected.router, prefix="/protected", tags=["Protected"])
app.include_router(pdf_parser.router, prefix="/pdf", tags=["PDF Parser"])
logger.info("Routers included in the FastAPI application.")


if __name__ == "__main__":
    logger.info("Starting the FastAPI application.")
    uvicorn.run("main-api:app", host="0.0.0.0", port=8081, reload=True)