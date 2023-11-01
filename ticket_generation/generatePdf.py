from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Spacer, Image
from reportlab.pdfgen import canvas
from PIL import Image as PILImage
import tempfile
from io import BytesIO
import os

def generate_pdf(id,name,phone,qr_buffer):
    # Create a BytesIO buffer to store the PDF
    pdf_buffer = BytesIO()

    # Create the PDF document
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

    # Add background color
    pdf.setFillColorRGB(1, 1, 1)  # White
    pdf.rect(0, 0, letter[0], letter[1], fill=True, stroke=False)

    # Add border
    pdf.setStrokeColor(colors.black)
    pdf.rect(50, 50, letter[0] - 100, letter[1] - 100, fill=False, stroke=True)

    # Add logo
    logo_path = "static/logo.jpg"
    pdf.drawImage(logo_path, 60, letter[1] - 160, width=100, height=100)

    # Set up the certificate content
    pdf.setFont("Helvetica-Bold", 24)
    pdf.setFillColor(colors.black)
    pdf.drawString(180, 500, "Kannada Rajyotsava")
    pdf.setFont("Helvetica", 18)
    pdf.drawString(180, 450, "Ticket Confirmation")
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(180, 400, name)
    pdf.setFont("Helvetica", 18)
    pdf.drawString(180, 350,id)
    # pdf.setFont("Helvetica-Bold", 20)
    # pdf.drawString(180, 300, event_name)

    # Convert the QR code to a PIL image
    qr_pil_image = PILImage.open(qr_buffer)

    # Create a temporary PNG file to save the QR code
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_qr_file:
        temp_qr_file_path = temp_qr_file.name
        qr_pil_image.save(temp_qr_file_path, format='PNG')

    # Add the QR code image from the temporary file to the PDF
    pdf.drawImage(temp_qr_file_path, 450, 55, width=1.5 * inch, height=1.5 * inch)

    # Close and remove the temporary file
    temp_qr_file.close()
    os.remove(temp_qr_file_path)

    # Save the PDF content to the buffer
    pdf.save()

    # Move the buffer position to the beginning of the PDF
    pdf_buffer.seek(0)

    return pdf_buffer