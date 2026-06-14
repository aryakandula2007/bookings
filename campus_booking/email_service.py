import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ------------------------------------
# EMAIL CONFIGURATION
# ------------------------------------

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"

ADMIN_EMAIL = "admin@university.edu"

# ------------------------------------
# SEND EMAIL
# ------------------------------------

def send_email(
    recipient,
    subject,
    html_body
):

    try:

        msg = MIMEMultipart()

        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient
        msg["Subject"] = subject

        msg.attach(
            MIMEText(
                html_body,
                "html"
            )
        )

        server = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        )

        server.starttls()

        server.login(
            SENDER_EMAIL,
            SENDER_PASSWORD
        )

        server.send_message(msg)

        server.quit()

        return True

    except Exception as e:

        print(
            f"Email Error: {e}"
        )

        return False

# ------------------------------------
# BOOKING CONFIRMATION
# ------------------------------------

def send_booking_confirmation(
    recipient,
    room_name,
    booking_date,
    start_time,
    end_time
):

    subject = (
        "Room Booking Confirmed"
    )

    html = f"""
    <html>
    <body>

    <h2>
    Booking Confirmed
    </h2>

    <p>
    Your room reservation
    has been confirmed.
    </p>

    <table border="1">

        <tr>
            <td>Room</td>
            <td>{room_name}</td>
        </tr>

        <tr>
            <td>Date</td>
            <td>{booking_date}</td>
        </tr>

        <tr>
            <td>Start</td>
            <td>{start_time}</td>
        </tr>

        <tr>
            <td>End</td>
            <td>{end_time}</td>
        </tr>

    </table>

    <br>

    <p>
    Please arrive on time.
    </p>

    </body>
    </html>
    """

    return send_email(
        recipient,
        subject,
        html
    )

# ------------------------------------
# WAITLIST EMAIL
# ------------------------------------

def send_waitlist_notification(
    recipient,
    room_name
):

    subject = (
        "Added to Waitlist"
    )

    html = f"""
    <html>
    <body>

    <h2>
    Waitlist Confirmation
    </h2>

    <p>

    You have been added
    to the waitlist for:

    <b>{room_name}</b>

    </p>

    <p>
    We will notify you
    if a slot becomes
    available.
    </p>

    </body>
    </html>
    """

    return send_email(
        recipient,
        subject,
        html
    )

# ------------------------------------
# WAITLIST PROMOTION
# ------------------------------------

def send_promotion_email(
    recipient,
    room_name
):

    subject = (
        "Room Now Available"
    )

    html = f"""
    <html>
    <body>

    <h2>
    Good News!
    </h2>

    <p>

    A slot is now available
    for:

    <b>{room_name}</b>

    </p>

    <p>
    Login immediately
    to claim your booking.
    </p>

    </body>
    </html>
    """

    return send_email(
        recipient,
        subject,
        html
    )

# ------------------------------------
# BOOKING CANCELLATION
# ------------------------------------

def send_cancellation_email(
    recipient,
    room_name
):

    subject = (
        "Booking Cancelled"
    )

    html = f"""
    <html>
    <body>

    <h2>
    Booking Cancelled
    </h2>

    <p>

    Your booking for

    <b>{room_name}</b>

    has been cancelled.

    </p>

    </body>
    </html>
    """

    return send_email(
        recipient,
        subject,
        html
    )

# ------------------------------------
# BOOKING REMINDER
# ------------------------------------

def send_reminder_email(
    recipient,
    room_name,
    booking_date,
    start_time
):

    subject = (
        "Upcoming Booking Reminder"
    )

    html = f"""
    <html>
    <body>

    <h2>
    Reminder
    </h2>

    <p>

    Your booking starts soon.

    </p>

    <table border="1">

        <tr>
            <td>Room</td>
            <td>{room_name}</td>
        </tr>

        <tr>
            <td>Date</td>
            <td>{booking_date}</td>
        </tr>

        <tr>
            <td>Time</td>
            <td>{start_time}</td>
        </tr>

    </table>

    </body>
    </html>
    """

    return send_email(
        recipient,
        subject,
        html
    )

# ------------------------------------
# ADMIN ALERT
# ------------------------------------

def send_admin_alert(
    message
):

    subject = (
        "Campus Booking Alert"
    )

    html = f"""
    <html>
    <body>

    <h2>
    Admin Alert
    </h2>

    <p>

    {message}

    </p>

    </body>
    </html>
    """

    return send_email(
        ADMIN_EMAIL,
        subject,
        html
    )

# ------------------------------------
# DAILY REPORT
# ------------------------------------

def send_daily_report(
    total_bookings,
    total_waitlist
):

    subject = (
        "Daily Booking Report"
    )

    html = f"""
    <html>
    <body>

    <h2>
    Daily Report
    </h2>

    <table border="1">

        <tr>
            <td>Total Bookings</td>
            <td>{total_bookings}</td>
        </tr>

        <tr>
            <td>Waitlisted Users</td>
            <td>{total_waitlist}</td>
        </tr>

    </table>

    </body>
    </html>
    """

    return send_email(
        ADMIN_EMAIL,
        subject,
        html
    )

# ------------------------------------
# BULK EMAIL
# ------------------------------------

def send_bulk_email(
    recipients,
    subject,
    html
):

    results = []

    for user in recipients:

        success = send_email(
            user,
            subject,
            html
        )

        results.append(
            {
                "email": user,
                "success": success
            }
        )

    return results

# ------------------------------------
# TEST EMAIL
# ------------------------------------

def test_email():

    return send_email(
        SENDER_EMAIL,
        "Email Test",
        "<h1>SMTP Working</h1>"
    )