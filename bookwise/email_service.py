import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# ----------------------------------
# CONFIGURATION
# ----------------------------------

SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"


# ----------------------------------
# SEND EMAIL
# ----------------------------------

def send_email(
    recipient_email,
    subject,
    body
):

    try:

        msg = MIMEMultipart()

        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient_email
        msg["Subject"] = subject

        msg.attach(
            MIMEText(
                body,
                "plain"
            )
        )

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            SENDER_EMAIL,
            SENDER_PASSWORD
        )

        server.sendmail(
            SENDER_EMAIL,
            recipient_email,
            msg.as_string()
        )

        server.quit()

        return True

    except Exception as e:

        print(
            f"Email Error: {e}"
        )

        return False


# ----------------------------------
# BOOKING CONFIRMATION
# ----------------------------------

def send_booking_confirmation(
    recipient_email,
    booking_id,
    room_name,
    booking_date,
    start_time,
    end_time
):

    subject = (
        f"BookWise Booking Confirmation #{booking_id}"
    )

    body = f"""
Hello,

Your booking has been confirmed.

Booking ID: {booking_id}

Room: {room_name}

Date: {booking_date}

Time:
{start_time} - {end_time}

Thank you for using BookWise.

Regards,
BookWise Team
"""

    return send_email(
        recipient_email,
        subject,
        body
    )


# ----------------------------------
# WAITLIST EMAIL
# ----------------------------------

def send_waitlist_notification(
    recipient_email,
    room_name
):

    subject = (
        "BookWise Waitlist Notification"
    )

    body = f"""
Hello,

The room you requested is currently unavailable.

You have been added to the waitlist.

Room:
{room_name}

We will notify you if it becomes available.

Regards,
BookWise Team
"""

    return send_email(
        recipient_email,
        subject,
        body
    )


# ----------------------------------
# BOOKING CANCELLATION EMAIL
# ----------------------------------

def send_cancellation_email(
    recipient_email,
    booking_id
):

    subject = (
        f"BookWise Booking Cancelled #{booking_id}"
    )

    body = f"""
Hello,

Your booking has been cancelled.

Booking ID:
{booking_id}

Regards,
BookWise Team
"""

    return send_email(
        recipient_email,
        subject,
        body
    )