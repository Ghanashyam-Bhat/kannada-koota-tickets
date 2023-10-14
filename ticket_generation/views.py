from django.http import JsonResponse
import json
from authentication.views import auth
from .models import attendee as Attendee
from django.contrib.auth import get_user_model
from hashlib import sha256
import time
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Spacer, Image
from reportlab.pdfgen import canvas
import qrcode
from io import BytesIO
from PIL import Image as PILImage
import tempfile
import os

import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Create your views here.    
def ticketSubmissions(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    data = json.loads(req_body)
    User = get_user_model()
    if status!=200:
        response =  JsonResponse({'message': 'REDIRECT'}, status=401)
        return response
    try:
        if request.method == 'POST':
            hash_val = generateUniqueData(data["universityId"],data["email"],data["name"],data["contact"])
            newAttendee = Attendee(
                id = data["universityId"],
                email = data["email"],
                name = data["name"],
                phone = data["contact"],
                isCash = True if "Cash"==data["paymentMethod"] else False,
                handledBy = User.objects.get(pk=message["id"]),
                hash_val = hash_val
            )
            newAttendee.save()
            try:
                sendMail(data["universityId"],data["email"],data["name"],data["contact"],hash_val)
            except Exception as e:
                print("Error:",e)
                response =  JsonResponse({'message': 'Email Failed'}, status=200)
            response =  JsonResponse({'message': 'SUCCESS'}, status=201)
            
            return response
    except Exception as err:
        print(f"Server Error in ticket submission.\nRequest -> {request}\nError -> {err}")
        response =  JsonResponse({'message': 'ERROR'}, status=500)
        return response


def generateUniqueData(id,email,name,phone):
    hash_val = sha256((id+name+email+phone+str(time.time())).encode('utf-8')).hexdigest()
    return hash_val

def generateQrCode(hash_val):
    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

    qr.add_data(hash_val)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Create a BytesIO buffer for the QR code image
    qr_buffer = BytesIO()
    qr_image.save(qr_buffer, format='PNG')  # Set the format explicitly to PNG
    qr_buffer.seek(0)
    return qr_buffer


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

def sendMail(id,email,name,contact,hash_val):
        
    EMAIL_ADDRESS = 'developerhitesh29@gmail.com'
    EMAIL_PASSWORD = 'xvlslgftplqijjyv'

    # Define email sender and receiver
    email_sender = EMAIL_ADDRESS
    email_password = EMAIL_PASSWORD
    email_receiver = email

    # Set the subject and body of the email
    subject = "Karnataka Rajyotsava ticket by Kannada Koota"
    body = """
    <html>
    <head>
    <style>
    .container {
    text-align: center;
    }
    body {
    background-color: #f4f4f4;
    margin: 0;
    padding: 0;
    }
    h1 {
    color: #333;
    font-size: 36px;
    font-weight: bold;
    margin-bottom: 10px;
    }
    p {
    color: #555;
    font-size: 16px;
    margin-bottom: 10px;
    }
    </style>
    </head>
    <body>
    <div class="container">
        <h1>ಕನ್ನಡ ಕೂಟ</h1>
        <p>This is your automatically generated Ticket for """+name+"""</p>
    </div>
    </body>
    </html>
    """

    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = email_sender
    msg["To"] = email_receiver
    msg["Subject"] = subject

    # Attach the HTML content as part of the email
    html_part = MIMEText(body, "html")
    msg.attach(html_part)

    qrCode = generateQrCode(hash_val)
    pdfFile = generate_pdf(id,name,contact,qrCode)


    # Attach the PDF file
    pdf_attachment = MIMEApplication(pdfFile, _subtype="pdf")
    pdf_attachment.add_header("Content-Disposition", f'attachment; filename="{id}.pdf"')
    msg.attach(pdf_attachment)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, msg.as_string())