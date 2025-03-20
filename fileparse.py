## File Reading

# This code is for reading files in the CSM project that are in a table format.

import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
import pandas as pd

# Set path to Tesseract OCR (Change this if necessary)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_table_from_scanned_pdf(pdf_path, output_csv, dpi=300):
    # Convert PDF to images
    images = convert_from_path(pdf_path, dpi=dpi)
    
    extracted_data = []
    
    for i, image in enumerate(images):
        # Convert image to grayscale
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        
        # Apply threshold to improve OCR accuracy
        _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Use Tesseract OCR with table mode
        custom_config = r'--psm 6'  # Page segmentation mode 6 is good for tables
        extracted_text = pytesseract.image_to_string(thresh, config=custom_config)
        
        # Convert text to structured format (basic parsing for tabular data)
        lines = extracted_text.split("\n")
        table_data = [line.split() for line in lines if line.strip()]
        extracted_data.extend(table_data)

    # Convert extracted data to DataFrame
    df = pd.DataFrame(extracted_data)

    # Save to CSV
    df.to_csv(output_csv, index=False, header=False)
    print(f"Table data saved to {output_csv}")

    return df

# Example usage
pdf_file = "scanned_table.pdf"  # Replace with your file
csv_output = "extracted_table.csv"
table_df = extract_table_from_scanned_pdf(pdf_file, csv_output)

# Display the extracted table
print(table_df)
