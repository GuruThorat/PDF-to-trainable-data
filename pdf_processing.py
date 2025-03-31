import os
import PyPDF2
import pytesseract
from pdf2image import convert_from_path
import pdfplumber
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
import logging
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"



# TESTING FOR ORDINARY IMAGES----------------------------------------------------------------------------------------------------------

# import pytesseract
# from PIL import Image

# img = Image.open()  # Replace with your image file
# text = pytesseract.image_to_string(img)

# print(text)  # This should output the text extracted from the image



# TESTING FOR PDF FILES----------------------------------------------------------------------------------------------------------

# import pytesseract
# from PIL import Image
# from pdf2image import convert_from_path

# # Path to your PDF file
# pdf_path = '/Users/gururaj/Downloads/scan_sample.pdf'

# # Convert PDF to images (each page becomes an image)
# images = convert_from_path(pdf_path)

# # Process each page with OCR
# text = ""
# for img in images:
#     text += pytesseract.image_to_string(img) + "\n"

# # Print the extracted text
# print(text)

# ----------------------------------------------------------------------------------------------------------------------

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Path to your PDF directory
pdf_dir = "/Users/gururaj/Downloads/meditation"
output_dir = "/Users/gururaj/Downloads/parse-output"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

def process_pdf(pdf_path):
    """Process a single PDF file (text-based or scanned)."""
    try:
        file_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_file = os.path.join(output_dir, f"{file_name}.txt")
        
        # Try extracting text directly first (faster for text-based PDFs)
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"
                else:
                    # If no text is extracted, assume it's scanned and use OCR
                    images = convert_from_path(pdf_path)
                    for img in images:
                        text += pytesseract.image_to_string(img) + "\n"
        
        # Save the extracted text
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        logging.info(f"Processed: {pdf_path}")
    except Exception as e:
        logging.error(f"Error processing {pdf_path}: {str(e)}")

def process_all_pdfs(pdf_dir):
    """Process all PDFs in parallel."""
    pdf_files = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
    logging.info(f"Found {len(pdf_files)} PDFs to process.")
    
    # Use ProcessPoolExecutor for parallel processing
    with ProcessPoolExecutor() as executor:
        list(tqdm(executor.map(process_pdf, pdf_files), total=len(pdf_files)))

if __name__ == "__main__":
    process_all_pdfs(pdf_dir)