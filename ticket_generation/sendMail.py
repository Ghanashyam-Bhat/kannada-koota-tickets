import os
from dotenv import load_dotenv
import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ticket_generation.generatePdf import generate_pdf
from ticket_generation.generateQR import generateQrCode

def sendMail(id,email,name,contact,hash_val,isVip):
    # Define email sender and receiver
    load_dotenv()
    email_sender = os.environ.get("EMAIL_ADDRESS")
    email_password = os.environ.get("EMAIL_PASSWORD")
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

    qrCode = generateQrCode(hash_val,isVip)
    pdfFile = generate_pdf(id,name,contact,qrCode)


    # Attach the PDF file
    pdf_attachment = MIMEApplication(pdfFile.getvalue(), _subtype="pdf")
    pdf_attachment.add_header("Content-Disposition", f'attachment; filename="{id}.pdf"')
    msg.attach(pdf_attachment)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, msg.as_string())