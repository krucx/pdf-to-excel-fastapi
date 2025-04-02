import pandas as pd
import pdfplumber
from io import BytesIO
import re
from PIL import Image
import pytesseract
from logger_config import get_logger

# Initialize logger
logger = get_logger(__name__)

def convert_pdf_to_excel(pdf_file: BytesIO) -> BytesIO:
    """
    Converts a PDF file to an Excel file, running table extraction, text extraction, and OCR together.
    Saves results in separate sheets of the same Excel file.
    Args:
        pdf_file (BytesIO): The PDF file as a BytesIO object.
    Returns:
        BytesIO: The Excel file as a BytesIO object.
    """
    logger.info("Starting PDF to Excel conversion.")
    table_data = []
    text_data = []
    ocr_data = []

    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                logger.info(f"Processing page {page_number}.")

                # Extract table data
                table = page.extract_table()
                if table:
                    logger.info(f"Table data found on page {page_number}.")
                    table_data.extend(table)

                # Extract raw text
                raw_text = page.extract_text()
                if raw_text:
                    logger.info(f"Raw text found on page {page_number}.")
                    processed_text_data = process_raw_text_to_table(raw_text)
                    text_data.extend(processed_text_data)

                # Perform OCR
                ocr_page_data = perform_ocr_on_page(page)
                if ocr_page_data:
                    logger.info(f"OCR data found on page {page_number}.")
                    ocr_data.extend(ocr_page_data)

        # Create Excel file with multiple sheets
        excel_file = BytesIO()
        with pd.ExcelWriter(excel_file, engine="xlsxwriter") as writer:
            # Write table data to the first sheet
            if table_data:
                logger.info("Writing table data to Excel.")
                table_df = pd.DataFrame(table_data)
                table_df.to_excel(writer, index=False, header=False, sheet_name="Table Data")

            # Write text data to the second sheet
            if text_data:
                logger.info("Writing text data to Excel.")
                text_df = pd.DataFrame(text_data)
                text_df.to_excel(writer, index=False, header=False, sheet_name="Text Data")

            # Write OCR data to the third sheet
            if ocr_data:
                logger.info("Writing OCR data to Excel.")
                ocr_df = pd.DataFrame(ocr_data)
                ocr_df.to_excel(writer, index=False, header=False, sheet_name="OCR Data")

        excel_file.seek(0)
        logger.info("PDF to Excel conversion completed successfully.")
        return excel_file

    except Exception as e:
        logger.error(f"An error occurred during PDF to Excel conversion: {e}")
        raise


def process_raw_text_to_table(raw_text: str) -> list:
    """
    Processes raw text from a PDF page into a table-like structure.
    Args:
        raw_text (str): The raw text extracted from the PDF page.
    Returns:
        list: A list of rows, where each row is a list of columns.
    """
    logger.info("Processing raw text into table format.")
    rows = []
    for line in raw_text.split("\n"):
        # Split the line into columns using common delimiters or spacing
        columns = re.split(r'\s{2,}|\t|,', line.strip())
        if len(columns) > 1:
            rows.append(columns)
        else:
            # Handle single-column rows by appending as a single cell
            rows.append([line.strip()])
    return rows


def perform_ocr_on_page(page) -> list:
    """
    Performs OCR on a PDF page to extract tabular data.
    Args:
        page: A pdfplumber page object.
    Returns:
        list: A list of rows, where each row is a list of columns.
    """
    logger.info("Performing OCR on page.")
    # pytesseract.pytesseract.tesseract_cmd = os.getenv(key="TESSERACT_PATH")
    rows = []
    try:
        # Convert the PDF page to an image
        image = page.to_image(resolution=300).original

        # Use the image directly as it is already a PIL Image object
        pil_image = image

        # Perform OCR on the image
        raw_text = pytesseract.image_to_string(pil_image)

        # Process the OCR text into rows and columns
        rows = process_raw_text_to_table(raw_text)
        logger.info("OCR processing completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred during OCR processing: {e}")
    return rows