from database import (
    create_booking,
    get_bookings
)

# ----------------------------------
# CHECK AVAILABILITY
# ----------------------------------

def check_availability(
    room_id,
    booking_date,
    start_time,
    end_time
):

    bookings = get_bookings()

    room_bookings = bookings[
        (
            bookings["room_id"] == room_id
        )
        &
        (
            bookings["booking_date"]
            == str(booking_date)
        )
    ]

    start_time = str(start_time)
    end_time = str(end_time)

    for _, booking in room_bookings.iterrows():

        existing_start = str(
            booking["start_time"]
        )

        existing_end = str(
            booking["end_time"]
        )

        # Overlapping booking
        if (
            start_time < existing_end
            and
            end_time > existing_start
        ):
            return False

    return True


# ----------------------------------
# USER BOOKINGS
# ----------------------------------

def get_user_bookings(
    username
):

    bookings = get_bookings()

    return bookings[
        bookings["user_name"]
        == username
    ]


# ----------------------------------
# ROOM SCHEDULE
# ----------------------------------

def get_room_schedule(
    room_id,
    booking_date
):

    bookings = get_bookings()

    room_bookings = bookings[
        (
            bookings["room_id"]
            == room_id
        )
        &
        (
            bookings["booking_date"]
            == str(booking_date)
        )
    ]

    return room_bookings.sort_values(
        by="start_time"
    )


# ----------------------------------
# AVAILABLE TIME SLOTS
# ----------------------------------

def get_available_slots(
    room_id,
    booking_date
):

    room_bookings = get_room_schedule(
        room_id,
        booking_date
    )

    if room_bookings.empty:

        return [
            "08:00 - 20:00 (Fully Available)"
        ]

    slots = []

    for _, booking in room_bookings.iterrows():

        slots.append(
            f"Booked: {booking['start_time']} - {booking['end_time']}"
        )

    return slots


# ----------------------------------
# EXPORTS
# ----------------------------------

__all__ = [
    "create_booking",
    "check_availability",
    "get_user_bookings",
    "get_room_schedule",
    "get_available_slots"
]
