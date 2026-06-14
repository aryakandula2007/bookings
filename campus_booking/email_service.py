# ----------------------------------
# EMAIL SERVICE
# ----------------------------------

def send_booking_confirmation(
    email,
    room_name,
    booking_date,
    start_time,
    end_time
):

    message = f"""
Booking Confirmation

Email: {email}

Room: {room_name}

Date: {booking_date}

Time: {start_time} - {end_time}

Status: Confirmed
"""

    print(message)

    return True


# ----------------------------------
# WAITLIST EMAIL
# ----------------------------------

def send_waitlist_notification(
    email,
    room_name
):

    message = f"""
Waitlist Notification

Email: {email}

Room: {room_name}

You have been added to the waitlist.
"""

    print(message)

    return True


# ----------------------------------
# CANCELLATION EMAIL
# ----------------------------------

def send_cancellation_email(
    email,
    room_name
):

    message = f"""
Booking Cancelled

Email: {email}

Room: {room_name}
"""

    print(message)

    return True
    