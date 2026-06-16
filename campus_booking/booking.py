from database import get_bookings

def check_availability(
room_id,
booking_date,
start_time,
end_time
):

bookings = get_bookings()

room_bookings = bookings[
    (
        bookings["room_id"].astype(int)
        == int(room_id)
    )
    &
    (
        bookings["booking_date"].astype(str)
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

if bookings.empty:
    return bookings

return bookings[
    bookings["user_name"]
    .astype(str)
    .str.strip()
    .str.lower()
    ==
    str(username)
    .strip()
    .lower()
]

def get_room_schedule(
room_id,
booking_date
):

bookings = get_bookings()

if bookings.empty:
    return bookings

return bookings[
    (
        bookings["room_id"].astype(int)
        == int(room_id)
    )
    &
    (
        bookings["booking_date"]
        .astype(str)
        ==
        str(booking_date)
    )
]

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

