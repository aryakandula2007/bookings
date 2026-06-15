from database import (
    create_booking,
    get_bookings
)

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

        if (
            start_time < existing_end
            and
            end_time > existing_start
        ):
            return False

    return True


def get_user_bookings(
    username
):

    bookings = get_bookings()

    username = (
        str(username)
        .strip()
        .lower()
    )

    bookings["user_name"] = (
        bookings["user_name"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    return bookings[
        bookings["user_name"]
        == username
    ]


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

    return room_bookings


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
    
