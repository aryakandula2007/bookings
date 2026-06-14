import qrcode
import uuid
import hashlib
import os
from datetime import datetime, timedelta

from database import (
    get_connection,
    check_in,
    check_out
)

# ------------------------------------
# CONFIG
# ------------------------------------

QR_FOLDER = "qrcodes"

if not os.path.exists(QR_FOLDER):
    os.makedirs(QR_FOLDER)

SECRET_KEY = "CAMPUS_RESOURCE_SECRET"

# ------------------------------------
# TOKEN GENERATION
# ------------------------------------

def generate_secure_token(
    booking_id
):

    raw = (
        f"{booking_id}"
        f"{SECRET_KEY}"
        f"{datetime.now()}"
    )

    return hashlib.sha256(
        raw.encode()
    ).hexdigest()


# ------------------------------------
# SAVE TOKEN
# ------------------------------------

def save_qr_token(
    booking_id,
    token
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS qr_tokens(
        booking_id INTEGER,
        token TEXT,
        created_at TIMESTAMP
    )
    """)

    cursor.execute(
        """
        INSERT INTO qr_tokens
        VALUES
        (
            ?,
            ?,
            CURRENT_TIMESTAMP
        )
        """,
        (
            booking_id,
            token
        )
    )

    conn.commit()
    conn.close()


# ------------------------------------
# GENERATE QR
# ------------------------------------

def generate_qr(
    booking_id
):

    token = generate_secure_token(
        booking_id
    )

    save_qr_token(
        booking_id,
        token
    )

    qr_data = f"""
    Campus Resource Booking

    Booking ID: {booking_id}

    Student:
    Reserved Room

    Status: Valid
    """
    

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )

    qr.add_data(qr_data)
    qr.make(fit=True)

    image = qr.make_image()

    file_path = (
        f"{QR_FOLDER}/"
        f"booking_{booking_id}.png"
    )

    image.save(file_path)

    return file_path


# ------------------------------------
# TOKEN VALIDATION
# ------------------------------------

def validate_token(
    booking_id,
    token
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT token,
               created_at

        FROM qr_tokens

        WHERE booking_id = ?

        ORDER BY created_at DESC

        LIMIT 1
        """,
        (booking_id,)
    )

    record = cursor.fetchone()

    conn.close()

    if not record:
        return False

    stored_token = record[0]

    if stored_token != token:
        return False

    return True


# ------------------------------------
# CHECK-IN
# ------------------------------------

def qr_check_in(
    booking_id,
    token
):

    valid = validate_token(
        booking_id,
        token
    )

    if not valid:

        return {
            "success": False,
            "message":
            "Invalid QR token."
        }

    check_in(
        booking_id
    )

    return {
        "success": True,
        "message":
        "Check-in successful."
    }


# ------------------------------------
# CHECK-OUT
# ------------------------------------

def qr_check_out(
    booking_id,
    token
):

    valid = validate_token(
        booking_id,
        token
    )

    if not valid:

        return {
            "success": False,
            "message":
            "Invalid QR token."
        }

    check_out(
        booking_id
    )

    return {
        "success": True,
        "message":
        "Check-out successful."
    }


# ------------------------------------
# ATTENDANCE STATUS
# ------------------------------------

def get_attendance_status(
    booking_id
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            checkin_time,
            checkout_time

        FROM checkins

        WHERE booking_id = ?
        """,
        (booking_id,)
    )

    result = cursor.fetchone()

    conn.close()

    if not result:

        return "Not Checked In"

    if result[0] and not result[1]:
        return "Checked In"

    if result[0] and result[1]:
        return "Completed"

    return "Unknown"


# ------------------------------------
# VERIFY BOOKING EXISTS
# ------------------------------------

def booking_exists(
    booking_id
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM bookings
        WHERE id = ?
        """,
        (booking_id,)
    )

    booking = cursor.fetchone()

    conn.close()

    return booking is not None


# ------------------------------------
# EXPIRE OLD TOKENS
# ------------------------------------

def cleanup_expired_tokens():

    conn = get_connection()

    cursor = conn.cursor()

    expiry = (
        datetime.now()
        - timedelta(days=30)
    )

    cursor.execute(
        """
        DELETE FROM qr_tokens
        WHERE created_at < ?
        """,
        (expiry,)
    )

    conn.commit()
    conn.close()


# ------------------------------------
# GENERATE SCAN URL
# ------------------------------------

def generate_scan_url(
    booking_id,
    token
):

    return (
        "https://campusbooking.edu/"
        f"checkin?"
        f"id={booking_id}"
        f"&token={token}"
    )


# ------------------------------------
# ADMIN QR STATS
# ------------------------------------

def total_checkins():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM checkins
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def active_users_inside():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)

        FROM checkins

        WHERE checkout_time IS NULL
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


# ------------------------------------
# QR DETAILS
# ------------------------------------

def get_qr_details(
    booking_id
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM qr_tokens
        WHERE booking_id = ?
        """,
        (booking_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return result
