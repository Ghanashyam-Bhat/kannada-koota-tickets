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
    
    qr_pil_image = PILImage.open(qr_buffer)
    image = Image.open("Rajyotsava.jpg")

# Create a drawing context
    draw = ImageDraw.Draw(image)

    # Define the text, color, and size
    text = "Dear "+ name+","
    text_color = (253, 252, 220)  # RGB color (pale yellow)
    text_size = 300


    # Define the position where you want to add the text
    text_position = (167, 740)
    font = ImageFont.truetype("NotoSansKannada-Regular.ttf", 36)
    # font = ImageFont.load_default()

    # Draw the text on the image with the specified size
    draw.text(text_position, text, fill=text_color, font=font)

    image.paste(qr ,(545,1403))

    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

    # Convert the image to RGB mode
    image = image.convert("RGB")

    # Save the image to the PDF
    image.save(pdf_buffer, format="PDF")

    # Close the PDF canvas
    c.save()

    # Reset the buffer to its beginning
    pdf_buffer.seek(0)

    return pdf_buffer.getvalue()