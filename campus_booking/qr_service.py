import os
import qrcode


# ----------------------------------
# CREATE QR DIRECTORY
# ----------------------------------

QR_FOLDER = "qrcodes"

os.makedirs(
    QR_FOLDER,
    exist_ok=True
)


# ----------------------------------
# GENERATE QR
# ----------------------------------

def generate_qr(
    booking_id
):

    qr_data = f"""
Campus Resource Booking

Booking ID: {booking_id}

Status: Valid
"""

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )

    qr.add_data(
        qr_data
    )

    qr.make(
        fit=True
    )

    img = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    file_path = (
        f"{QR_FOLDER}/booking_"
        f"{booking_id}.png"
    )

    img.save(
        file_path
    )

    return file_path


# ----------------------------------
# QR INFORMATION
# ----------------------------------

def get_qr_info(
    booking_id
):

    return {
        "booking_id": booking_id,
        "status": "Valid"
    }
    