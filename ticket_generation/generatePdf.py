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
    qr_pil_image = PILImage.open(qr_buffer)

    # Create a temporary PNG file to save the QR code
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_qr_file:
        temp_qr_file_path = temp_qr_file.name
        qr_pil_image.save(temp_qr_file_path, format='PNG')

    image = PILImage.open("Rajyotsava.jpg")

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Define the text, color, and size
    text = "Dear " + name + ","
    text_color = (253, 252, 220)  # RGB color (pale yellow)
    text_size = 300

    # Define the position where you want to add the text
    text_position = (167, 740)
    font = ImageFont.truetype("NotoSansKannada-Regular.ttf", 36)

    # Draw the text on the image with the specified size
    draw.text(text_position, text, fill=text_color, font=font)

    # Open the QR code image from the temporary file
    qr_code_img = PILImage.open(temp_qr_file_path)

    # Paste the QR code image onto the existing image
    image.paste(qr_code_img, (545, 1403))

    # Create a PDF buffer
    pdf_buffer = BytesIO()

    # Create the PDF document
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

    # Define the size to fit the full page
    image_size = (letter[0], letter[1])

    # Use ImageReader to read the PIL image and insert it into the PDF
    pdf.drawImage(ImageReader(image), 0, 0, width=image_size[0], height=image_size[1])

    pdf.save()

    # Move the buffer position to the beginning of the PDF
    pdf_buffer.seek(0)

    return pdf_buffer