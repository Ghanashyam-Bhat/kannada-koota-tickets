from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Spacer, Image
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from PIL import Image as PILImage
import tempfile
from io import BytesIO
import PyPDF2
import os

def generate_pdf(id,name,phone,qr_buffer):
    # Create a BytesIO buffer to store the PDF
    
    finalPdf = PyPDF2.PdfWriter()
    finalpdf_buffer = BytesIO()

    # pdf = canvas.Canvas("certificate.pdf", pagesize=letter)

    pdf_buffer = BytesIO()

    # Create the PDF document
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

    # Add background color
    pdf.setFillColorRGB(1, 1, 1)  # White
    pdf.rect(0, 0, letter[0], letter[1], fill=True, stroke=False)

    # Add logo
    template_path = "static/ticket_template.jpg"
    pdf.drawImage(template_path,0,0, letter[0], letter[1])

    pdf.setFont("Helvetica", 14)
    pdf.setFillColor(colors.lightyellow)
    pdf.drawString(73,485, f"Dear {name},")

    # Convert the QR code to a PIL image
    qr_pil_image = PILImage.open(qr_buffer)

    # Create a temporary PNG file to save the QR code
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_qr_file:
        temp_qr_file_path = temp_qr_file.name
        qr_pil_image.save(temp_qr_file_path, format='PNG')

    # Add the QR code image from the temporary file to the PDF
    pdf.drawImage(temp_qr_file_path, 236, 118, width=1.8 * inch, height=1.7 * inch)

    # Close and remove the temporary file
    temp_qr_file.close()
    os.remove(temp_qr_file_path)

    # Save the PDF content to the buffer
    pdf.save()

    # Move the buffer position to the beginning of the PDF
    pdf_buffer.seek(0)

    finalPdf.add_page(pdf_buffer)
    finalPdf.add_page(qr_buffer)
    finalPdf.write(finalpdf_buffer)
    finalpdf_buffer.seek(0)

    return finalpdf_buffer
