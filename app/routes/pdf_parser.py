from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.security import OAuth2PasswordBearer
from app.utils.token import decode_access_token
from app.utils.pdf_to_excel import convert_pdf_to_excel
from io import BytesIO
from fastapi.responses import StreamingResponse
from logger_config import get_logger

# Initialize logger
logger = get_logger(__name__)

router = APIRouter()

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/pdf2excel")
async def pdf_to_excel(
    token: str = Depends(oauth2_scheme),
    file: UploadFile = File(...)
):
    """
    Endpoint to convert a PDF file to an Excel file.
    Args:
        token (str): Bearer token for authentication.
        file (UploadFile): The uploaded PDF file.
    Returns:
        StreamingResponse: The converted Excel file.
    """
    logger.info("Endpoint '/pdf2excel' called.")
    try:
        # Validate the token
        username = decode_access_token(token)
        logger.info(f"Token successfully validated for user: {username}.")
    except HTTPException:
        logger.error("Token validation failed. Invalid or expired token.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or expired token"
        )

    # Validate file type
    if file.content_type != "application/pdf":
        logger.error(f"Invalid file type: {file.content_type}. Only PDF files are supported.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PDF files are supported."
        )

    try:
        # Convert PDF to Excel
        logger.info(f"Starting PDF to Excel conversion for file: {file.filename}.")
        pdf_file = BytesIO(await file.read())
        excel_file = convert_pdf_to_excel(pdf_file)
        logger.info(f"PDF to Excel conversion completed successfully for file: {file.filename}.")
    except Exception as e:
        logger.error(f"An error occurred during PDF to Excel conversion: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during PDF to Excel conversion."
        )

    # Return the Excel file as a response
    logger.info(f"Returning Excel file for download: {file.filename}.xlsx")
    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={file.filename}.xlsx"}
    )