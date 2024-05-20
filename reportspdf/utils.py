from PyPDF2 import PdfWriter, PdfReader
from io import BytesIO

def merge_pdf_with_watermark(pdf1_content, pdf2_path, output_path):
    # Open the second PDF file
    with open(pdf2_path, 'rb') as pdf2_file:
        pdf2_reader = PdfReader(pdf2_file)

        # Create a PdfFileWriter object to write the output PDF
        pdf_writer = PdfWriter()

        # Iterate through each page of the second PDF and add it to the output
        for page in pdf2_reader.pages:
            pdf_writer.add_page(page)

        # Create a PdfReader for the first PDF from its content
        pdf1_reader = PdfReader(BytesIO(pdf1_content))

        # Iterate through each page of the first PDF and add it to the output
        for page in pdf1_reader.pages:
            pdf_writer.add_page(page)

        # Write the merged PDF to the output file
        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)

# Ensure that you close the PdfReader objects explicitly
def close_pdfs(pdf1_content, pdf2_path):
    PdfReader(BytesIO(pdf1_content)).close()
    PdfReader(pdf2_path).close()
