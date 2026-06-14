from datetime import datetime, timedelta
from database import (
    get_connection,
    create_booking,
    add_waitlist
)

# ----------------------------------
# CONFIGURATION
# ----------------------------------

MAX_BOOKING_HOURS = 4
MIN_BOOKING_MINUTES = 30

# ----------------------------------
# TIME HELPERS
# ----------------------------------

def to_datetime(date_value, time_value):
    """
    Converts booking date and time
    into a single datetime object.
    """

    return datetime.strptime(
        f"{date_value} {time_value}",
        "%Y-%m-%d %H:%M:%S"
    )


def booking_duration_hours(
    booking_date,
    start_time,
    end_time
):

    start_dt = to_datetime(
        str(booking_date),
        str(start_time)
    )

    end_dt = to_datetime(
        str(booking_date),
        str(end_time)
    )

    duration = end_dt - start_dt

    return duration.total_seconds() / 3600


# ----------------------------------
# CHECK ROOM CAPACITY
# ----------------------------------

def validate_capacity(
    room_capacity,
    attendees
):

    return attendees <= room_capacity


# ----------------------------------
# AVAILABILITY CHECK
# ----------------------------------

def check_availability(
    room_id,
    booking_date,
    start_time,
    end_time
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT start_time,
               end_time
        FROM bookings

        WHERE room_id = ?
        AND booking_date = ?
        """,
        (
            room_id,
            str(booking_date)
        )
    )

    existing_bookings = cursor.fetchall()

    conn.close()

    requested_start = datetime.strptime(
        str(start_time),
        "%H:%M:%S"
    )

    requested_end = datetime.strptime(
        str(end_time),
        "%H:%M:%S"
    )

    for booking in existing_bookings:

        existing_start = datetime.strptime(
            booking[0],
            "%H:%M:%S"
        )

        existing_end = datetime.strptime(
            booking[1],
            "%H:%M:%S"
        )

        overlap = (
            requested_start < existing_end
            and
            requested_end > existing_start
        )

        if overlap:
            return False

    return True


# ----------------------------------
# VALIDATE BOOKING
# ----------------------------------

def validate_booking(
    booking_date,
    start_time,
    end_time
):

    duration = booking_duration_hours(
        booking_date,
        start_time,
        end_time
    )

    if duration <= 0:
        return (
            False,
            "End time must be after start time."
        )

    if duration > MAX_BOOKING_HOURS:
        return (
            False,
            f"Maximum booking is {MAX_BOOKING_HOURS} hours."
        )

    if duration < (
        MIN_BOOKING_MINUTES / 60
    ):
        return (
            False,
            f"Minimum booking is {MIN_BOOKING_MINUTES} minutes."
        )

    return (
        True,
        "Valid booking."
    )


# ----------------------------------
# CREATE BOOKING LOGIC
# ----------------------------------

def book_room(
    room_id,
    user_name,
    email,
    booking_date,
    start_time,
    end_time
):

    valid, message = validate_booking(
        booking_date,
        start_time,
        end_time
    )

    if not valid:

        return {
            "success": False,
            "message": message
        }

    available = check_availability(
        room_id,
        booking_date,
        start_time,
        end_time
    )

    if not available:

        add_waitlist(
            room_id,
            user_name,
            email
        )

        return {
            "success": False,
            "message":
            "Room unavailable. Added to waitlist."
        }

    booking_id = create_booking(
        room_id,
        user_name,
        email,
        booking_date,
        start_time,
        end_time
    )

    return {
        "success": True,
        "booking_id": booking_id,
        "message": "Booking confirmed."
    }


# ----------------------------------
# CANCEL BOOKING
# ----------------------------------

def cancel_booking(
    booking_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM bookings
        WHERE id = ?
        """,
        (booking_id,)
    )

    conn.commit()
    conn.close()

    promote_waitlist_user()


# ----------------------------------
# WAITLIST PROMOTION
# ----------------------------------

def promote_waitlist_user():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM waitlist
        ORDER BY request_time ASC
        LIMIT 1
        """
    )

    next_user = cursor.fetchone()

    if not next_user:

        conn.close()
        return

    waitlist_id = next_user[0]

    cursor.execute(
        """
        DELETE FROM waitlist
        WHERE id = ?
        """,
        (waitlist_id,)
    )

    conn.commit()
    conn.close()

    print(
        f"Promoted waitlist user: "
        f"{next_user[2]}"
    )


# ----------------------------------
# EXPIRE NO-SHOW BOOKINGS
# ----------------------------------

def release_no_show_bookings():

    conn = get_connection()

    cursor = conn.cursor()

    current_time = datetime.now()

    cursor.execute(
        """
        SELECT id,
               booking_date,
               start_time

        FROM bookings
        """
    )

    bookings = cursor.fetchall()

    for booking in bookings:

        booking_id = booking[0]

        start_dt = datetime.strptime(
            f"{booking[1]} {booking[2]}",
            "%Y-%m-%d %H:%M:%S"
        )

        grace_period = (
            start_dt +
            timedelta(minutes=15)
        )

        if current_time > grace_period:

            cursor.execute(
                """
                SELECT *
                FROM checkins
                WHERE booking_id = ?
                """,
                (booking_id,)
            )

            checked_in = cursor.fetchone()

            if not checked_in:

                cursor.execute(
                    """
                    DELETE FROM bookings
                    WHERE id = ?
                    """,
                    (booking_id,)
                )

    conn.commit()
    conn.close()


# ----------------------------------
# GET AVAILABLE ROOMS
# ----------------------------------

def get_available_rooms(
    booking_date,
    start_time,
    end_time
):

    conn = get_connection()

    rooms = conn.execute(
        """
        SELECT *
        FROM rooms
        """
    ).fetchall()

    available_rooms = []

    for room in rooms:

        room_id = room[0]

        if check_availability(
            room_id,
            booking_date,
            start_time,
            end_time
        ):
            available_rooms.append(room)

    conn.close()

    return available_rooms


# ----------------------------------
# BOOKING STATISTICS
# ----------------------------------

def total_bookings():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM bookings
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def total_waitlisted():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM waitlist
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count