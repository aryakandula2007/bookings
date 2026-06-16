import streamlit as st
from datetime import datetime

from database import (
    initialize_db,
    get_rooms,
    get_bookings
)

from auth import (
    auth_page,
    logout
)

from booking import (
    create_booking,
    check_availability,
    get_user_bookings,
    get_room_schedule,
    get_available_slots
)

from waitlist import (
    add_to_waitlist
)

from qr_service import (
    generate_qr
)

from analytics import (
    generate_heatmap,
    peak_hours_chart,
    booking_trend_chart,
    most_popular_rooms_chart,
    user_activity_chart,
    best_time_to_visit
)


from ai_recommendation import (
    recommend_room,
    recommend_multiple_rooms
)

from email_service import (
    send_booking_confirmation
)

from calendar_service import (
    add_calendar_event
)

# ----------------------------------
# PAGE CONFIG
# ----------------------------------

st.set_page_config(
    page_title="Campus Resource Manager",
    layout="wide"
)

# ----------------------------------
# DATABASE INIT
# ----------------------------------

initialize_db()

# ----------------------------------
# LOGIN
# ----------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    auth_page()
    st.stop()

# ----------------------------------
# SIDEBAR
# ----------------------------------

st.sidebar.title(
    "🏫 Campus Resource Manager"
)

st.sidebar.success(
    f"Logged in as: {st.session_state.username}"
)

if st.sidebar.button(
    "Logout"
):
    logout()
    st.rerun()

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Book Resource",
        "Availability",
        "AI Recommendation",
        "My Bookings",
        "Analytics"
    ]
)

# ----------------------------------
# DASHBOARD
# ----------------------------------

if menu == "Dashboard":

    st.title(
        "🏫 Campus Resource Dashboard"
    )

    rooms = get_rooms()
    bookings = get_bookings()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Rooms",
        len(rooms)
    )

    col2.metric(
        "Total Bookings",
        len(bookings)
    )

    available_today = len(rooms)

    col3.metric(
        "Rooms Available",
        available_today
    )

    st.subheader(
        "Available Resources"
    )

    st.dataframe(
        rooms,
        use_container_width=True
    )

# ----------------------------------
# BOOK RESOURCE
# ----------------------------------

elif menu == "Book Resource":

    st.title(
        "📅 Book a Resource"
    )

    rooms = get_rooms()

    user = st.session_state.username

    email = st.text_input(
        "Email"
    )

    room_name = st.selectbox(
        "Select Room",
        rooms["room_name"]
    )

    booking_date = st.date_input(
        "Booking Date"
    )

    start_time = st.time_input(
        "Start Time"
    )

    end_time = st.time_input(
        "End Time"
    )

    if st.button(
        "Book Now"
    ):

        room_id = rooms[
            rooms["room_name"]
            == room_name
        ]["id"].values[0]

        available = check_availability(
            room_id,
            booking_date,
            start_time,
            end_time
        )

        if available:

            booking_id = create_booking(
                room_id,
                user,
                email,
                booking_date,
                start_time,
                end_time
            )

            qr_path = generate_qr(
                booking_id
            )

            send_booking_confirmation(
                email,
                room_name,
                booking_date,
                start_time,
                end_time
            )

            add_calendar_event(
                room_name,
                booking_date,
                start_time,
                end_time
            )

            st.success(
                "Booking Successful!"
            )

            st.write(
                f"Booking ID: {booking_id}"
            )

            st.image(
                qr_path,
                width=250
            )

        else:

            add_to_waitlist(
                room_id,
                user,
                email
            )

            st.warning(
                "Room unavailable. Added to waitlist."
            )

# ----------------------------------
# AVAILABILITY
# ----------------------------------

elif menu == "Availability":

    st.title("🔍 Room Availability")

    rooms = get_rooms()

    selected_date = st.date_input(
        "Select Date"
    )

    bookings = get_bookings()

    for _, room in rooms.iterrows():

    with st.expander(
        room["room_name"]
    ):

        st.write(
            "Selected Date:",
            selected_date
        )

        if not bookings.empty:

            st.write(
                bookings[
                    [
                        "room_id",
                        "booking_date"
                    ]
                ]
            )

        room_schedule = bookings[
            bookings["room_id"]
            == room["id"]
        ]

            if room_schedule.empty:

                st.success(
                    "✅ Available All Day"
                )

            else:

                st.warning(
                    "⚠️ Room Booked"
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
                
# ----------------------------------
# AI RECOMMENDATION
# ----------------------------------

elif menu == "AI Recommendation":

    st.title(
        "🤖 Smart Room Recommendation"
    )

    attendees = st.number_input(
        "Group Size",
        min_value=1,
        value=1
    )

    if st.button(
        "Recommend Room"
    ):

        recommendation = recommend_room(
            attendees
        )

        st.success(
            recommendation
        )

        alternatives = (
            recommend_multiple_rooms(
                attendees
            )
        )

        if alternatives:

            st.subheader(
                "Alternative Rooms"
            )

            st.dataframe(
                alternatives,
                use_container_width=True
            )

# ----------------------------------
# MY BOOKINGS
# ----------------------------------

elif menu == "My Bookings":

    st.title("📖 My Bookings")

    current_user = st.session_state.username

    bookings = get_bookings()

    user_bookings = bookings[
        bookings["user_name"]
        .astype(str)
        .str.strip()
        .str.lower()
        ==
        str(current_user)
        .strip()
        .lower()
    ]

    if user_bookings.empty:

        st.warning(
            "No bookings found."
        )

    else:

        st.dataframe(
            user_bookings,
            use_container_width=True
        )
# ----------------------------------
# ANALYTICS
# ----------------------------------

elif menu == "Analytics":

    st.title("📊 Resource Analytics")

    st.metric(
        "Recommended Time",
        best_time_to_visit()
    )

    st.subheader(
        "Room Utilization"
    )

    st.plotly_chart(
        generate_heatmap(),
        use_container_width=True,
        key="utilization"
    )

    st.subheader(
        "Most Popular Rooms"
    )

    st.plotly_chart(
        most_popular_rooms_chart(),
        use_container_width=True,
        key="popular_rooms"
    )

    st.subheader(
        "Peak Usage Hours"
    )

    st.plotly_chart(
        peak_hours_chart(),
        use_container_width=True,
        key="peak_hours"
    )

    st.subheader(
        "Booking Trends"
    )

    st.plotly_chart(
        booking_trend_chart(),
        use_container_width=True,
        key="booking_trends"
    )

    st.subheader(
        "User Activity"
    )

    st.plotly_chart(
        user_activity_chart(),
        use_container_width=True,
        key="user_activity"
    )

    st.subheader(
        "All Bookings"
    )

    st.dataframe(
        get_bookings(),
        use_container_width=True
    )