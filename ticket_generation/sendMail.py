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
        <html>
        <head>
            <title>Full Page Image</title>
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    overflow: hidden;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }

                img {
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                }

                @media (max-width: 768px) {
                    body {
                        justify-content: flex-start; /* Align image to the top for screens with a width of 768px or less */
                    }
                }
            </style>
        </head>
        <body>
            <img src="https://lh3.googleusercontent.com/pw/ADCreHco5zSPu3z5M00lAPbgaIWaQS4LSf491q4aK3SXTpU3JO7KU7P3_HMf9xfnLO6vFyR_IQMxVJUcI3xMVWV5DWM5mjABCNBbV4z1Yo1_mpng89-crbQ7g2aHkGGCCVhuf-fkZiedO1xy-oiM7vCZz3k=w618-h878-s-no-gm?authuser=0" alt="Full Page Invitation">
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