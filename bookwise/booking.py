import pandas as pd
from datetime import datetime, time

from database import (
    add_booking,
    get_bookings,
    get_room_bookings
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

    bookings = get_room_bookings(
        room_id,
        booking_date
    )

    if bookings.empty:
        return True

    new_start = str(start_time)
    new_end = str(end_time)

    for _, booking in bookings.iterrows():

        existing_start = booking["start_time"]
        existing_end = booking["end_time"]

        overlap = (
            new_start < existing_end
            and new_end > existing_start
        )

        if overlap:
            return False

    return True


# ----------------------------------
# CREATE BOOKING
# ----------------------------------

def create_booking(
    room_id,
    user_name,
    email,
    booking_date,
    start_time,
    end_time
):

    available = check_availability(
        room_id,
        booking_date,
        start_time,
        end_time
    )

    if not available:
        return None

    booking_id = add_booking(
        room_id,
        user_name,
        email,
        booking_date,
        start_time,
        end_time
    )

    return booking_id


# ----------------------------------
# USER BOOKINGS
# ----------------------------------

def get_user_bookings(user_name):

    bookings = get_bookings()

    if bookings.empty:
        return bookings

    return bookings[
        bookings["user_name"]
        .astype(str)
        .str.lower()
        ==
        str(user_name).lower()
    ]


# ----------------------------------
# ROOM SCHEDULE
# ----------------------------------

def get_room_schedule(
    room_id,
    booking_date
):

    return get_room_bookings(
        room_id,
        booking_date
    )


# ----------------------------------
# AVAILABLE SLOTS
# ----------------------------------

def get_available_slots(
    room_id,
    booking_date
):

    bookings = get_room_bookings(
        room_id,
        booking_date
    )

    day_start = time(8, 0)
    day_end = time(20, 0)

    if bookings.empty:

        return [
            (
                day_start.strftime("%H:%M"),
                day_end.strftime("%H:%M")
            )
        ]

    bookings = bookings.sort_values(
        by="start_time"
    )

    available_slots = []

    current_start = day_start

    for _, booking in bookings.iterrows():

        booked_start = datetime.strptime(
            booking["start_time"][:5],
            "%H:%M"
        ).time()

        booked_end = datetime.strptime(
            booking["end_time"][:5],
            "%H:%M"
        ).time()

        if current_start < booked_start:

            available_slots.append(
                (
                    current_start.strftime("%H:%M"),
                    booked_start.strftime("%H:%M")
                )
            )

        current_start = booked_end

    if current_start < day_end:

        available_slots.append(
            (
                current_start.strftime("%H:%M"),
                day_end.strftime("%H:%M")
            )
        )

    return available_slots


# ----------------------------------
# BOOKED SLOTS
# ----------------------------------

def get_booked_slots(
    room_id,
    booking_date
):

    bookings = get_room_bookings(
        room_id,
        booking_date
    )

    slots = []

    if bookings.empty:
        return slots

    for _, booking in bookings.iterrows():

        slots.append(
            (
                booking["start_time"],
                booking["end_time"]
            )
        )

    return slots


# ----------------------------------
# ROOM STATUS SUMMARY
# ----------------------------------

def room_status_summary(
    room_id,
    booking_date
):

    booked = get_booked_slots(
        room_id,
        booking_date
    )

    available = get_available_slots(
        room_id,
        booking_date
    )

    return {
        "booked": booked,
        "available": available
    }


# ----------------------------------
# NEXT AVAILABLE SLOT
# ----------------------------------

def next_available_slot(
    room_id,
    booking_date
):

    available = get_available_slots(
        room_id,
        booking_date
    )

    if len(available) == 0:
        return None

    return available[0]


# ----------------------------------
# BOOKING STATISTICS
# ----------------------------------

def total_bookings_count():

    bookings = get_bookings()

    return len(bookings)


def bookings_by_room():

    bookings = get_bookings()

    if bookings.empty:
        return pd.DataFrame()

    return (
        bookings
        .groupby("room_name")
        .size()
        .reset_index(name="count")
        .sort_values(
            by="count",
            ascending=False
        )
    )


def bookings_by_user():

    bookings = get_bookings()

    if bookings.empty:
        return pd.DataFrame()

    return (
        bookings
        .groupby("user_name")
        .size()
        .reset_index(name="count")
        .sort_values(
            by="count",
            ascending=False
        )
    )
    