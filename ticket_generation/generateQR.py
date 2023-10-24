import qrcode
from io import BytesIO

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