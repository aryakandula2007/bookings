import os
import qrcode

QR_FOLDER = "qr_codes"


def create_qr_folder():
    if not os.path.exists(QR_FOLDER):
        os.makedirs(QR_FOLDER)


def generate_qr(data):

    create_qr_folder()

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )

    qr.add_data(str(data))
    qr.make(fit=True)

    img = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    filename = f"{QR_FOLDER}/qr.png"

    img.save(filename)

    return filename


def generate_booking_qr(
    booking_id,
    room_name,
    booking_date,
    start_time,
    end_time
):

    qr_content = f"""
Booking ID: {booking_id}
Room: {room_name}
Date: {booking_date}
Start Time: {start_time}
End Time: {end_time}
"""

    return generate_qr(qr_content)