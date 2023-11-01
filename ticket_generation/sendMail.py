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
    <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Full-Screen Image</title>
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    background-image: url('https://kannada-koota-tickets.vercel.app/media/your-image.jpg'); /* Replace 'your-image.jpg' with the image URL or path */
                    background-size: cover;
                    background-position: center;
                    background-attachment: fixed;
                    background-repeat: no-repeat;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }

                /* Optional: Add styles for text or other content on the image */
                .content {
                    text-align: center;
                    color: #ffffff;
                    background-color: rgba(0, 0, 0, 0.5);
                    padding: 20px;
                    border-radius: 10px;
                }
            </style>
        </head>
        <body>
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
    pdfFile = generate_pdf(id,name,contact,qrCode,isVip)


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