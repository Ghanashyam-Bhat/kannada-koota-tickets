import qrcode
from io import BytesIO

def generateQrCode(hash_val,isVip):
    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=14,
            border=1,
        )

    qr.add_data("KK-ATTENDEE_PASS-"+hash_val)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="gold" if isVip else "silver")

    # Create a BytesIO buffer for the QR code image
    qr_buffer = BytesIO()
    qr_image.save(qr_buffer, format='PNG')  # Set the format explicitly to PNG
    qr_buffer.seek(0)
    return qr_buffer