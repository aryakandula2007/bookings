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
            .astype(str)
            ==
            str(booking_date)
        )
    ]

    return room_bookings


# ----------------------------------
# AVAILABLE TIME SLOTS
# ----------------------------------

elif menu == "Availability":

    st.title("🔍 Room Availability")

    rooms = get_rooms()

    selected_date = st.date_input(
        "Select Date"
    )

    for _, room in rooms.iterrows():

        with st.expander(
            room["room_name"]
        ):

            room_schedule = get_room_schedule(
                room["id"],
                selected_date
            )

            if room_schedule.empty:

                st.success(
                    "✅ Available All Day"
                )

                st.write(
                    "08:00 - 20:00"
                )

            else:

                st.warning(
                    "⚠️ Room has bookings"
                )

                st.dataframe(
                    room_schedule[
                        [
                            "user_name",
                            "start_time",
                            "end_time"
                        ]
                    ],
                    use_container_width=True
                )

                st.subheader(
                    "Booked Time Slots"
                )

                for slot in get_available_slots(
                    room["id"],
                    selected_date
                ):

                    st.write(slot)


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
