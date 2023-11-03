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
import os

import qrcode
from io import BytesIO

def generateQrCode(hash_val):
    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=14,
            border=1,
        )

    qr.add_data("KK-ATTENDEE_PASS-"+hash_val)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="silver")

    # Create a BytesIO buffer for the QR code image
    qr_buffer = BytesIO()
    qr_image.save(qr_buffer, format='PNG')  # Set the format explicitly to PNG
    qr_buffer.seek(0)
    return qr_buffer

def generate_pdf(id,name,contact,qrCode,isVip):
    # Create a BytesIO buffer to store the PDF

    # pdf = canvas.Canvas("certificate.pdf", pagesize=letter)

    pdf_buffer = BytesIO()

    # Create the PDF document
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

    # Add background color
    pdf.setFillColorRGB(1, 1, 1)  # White
    pdf.rect(0, 0, letter[0], letter[1], fill=True, stroke=False)

    # Add logo
    template_path = "static/ticket_template_vip.jpg" if isVip else "static/ticket_template_general.jpg"
    pdf.drawImage(template_path,0,0, letter[0], letter[1])

    pdf.setFont("Helvetica", 12)
    pdf.setFillColor(colors.white)

    # pdf.drawString(80,340, f"Dear {name},")
    pdf.drawString(125,340, f"{name},")


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
    # Assuming pdf_buffer contains the PDF content
    # with open('output.pdf', 'wb') as output_file:
    #     output_file.write(pdf_buffer.read())

    return pdf_buffer
# generate_pdf("hitesh",True)