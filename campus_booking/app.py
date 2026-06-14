import streamlit as st
import pandas as pd
from datetime import datetime
from auth import auth_page


from database import (
    initialize_db,
    get_rooms,
    get_bookings
)

from booking import (
    create_booking,
    check_availability
)

from waitlist import (
    add_to_waitlist
)

from ai_recommendation import (
    recommend_room
)

from analytics import (
    generate_heatmap
)

from qr_service import (
    generate_qr
)

from email_service import (
    send_booking_confirmation
)

from calendar_service import (
    add_calendar_event
)

# ----------------------------------
# INITIALIZATION
# ----------------------------------

st.set_page_config(
    page_title="Campus Resource Manager",
    layout="wide"
)
# -------------------------
# LOGIN SYSTEM
# -------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    auth_page()

    st.stop()

# ----------------------------------
# SIDEBAR
# ----------------------------------
from auth import logout
if st.sidebar.button("Logout"):

    logout()

    st.rerun()


st.sidebar.title("Campus Resource Manager")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Book Resource",
        "Availability",
        "AI Recommendation",
        "My Bookings",
        "Admin Analytics"
    ]
)

# ----------------------------------
# DASHBOARD
# ----------------------------------

if menu == "Dashboard":

    st.title("🏫 Campus Resource Dashboard")

    rooms = get_rooms()
    bookings = get_bookings()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Rooms",
        len(rooms)
    )

    col2.metric(
        "Active Bookings",
        len(bookings)
    )

    available = len(rooms) - len(
        bookings[
            bookings["booking_date"]
            == str(datetime.now().date())
        ]
    )

    col3.metric(
        "Available Today",
        available
    )

    st.subheader("Room Overview")
    st.dataframe(rooms)

# ----------------------------------
# BOOK RESOURCE
# ----------------------------------

elif menu == "Book Resource":

    st.title("📅 Book a Resource")

    user = st.session_state.username

    st.write(f"Booking as: {user}")

    email = st.text_input("Email")

    rooms = get_rooms()

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

    attendees = st.number_input(
        "Expected Attendees",
        min_value=1,
        value=1
    )

    if st.button("Book Now"):

        room_id = rooms[
            rooms["room_name"] == room_name
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

        room_bookings = bookings[
            (
                bookings["room_id"]
                == room["id"]
            )
            &
            (
                bookings["booking_date"]
                == str(selected_date)
            )
        ]

        with st.expander(
            room["room_name"]
        ):

            if room_bookings.empty:
                st.success(
                    "Available"
                )
            else:
                st.dataframe(
                    room_bookings
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
        min_value=1
    )

    room = recommend_room(
        attendees
    )

    st.success(
        f"Recommended Room: {room}"
    )

# ----------------------------------
# BOOKINGS
# ----------------------------------

elif menu == "My Bookings":

    st.title("📖 My Bookings")

    bookings = get_bookings()

    current_user = st.session_state.username

    # DEBUG
    st.write("Logged in user:", current_user)

    st.write("All bookings:")
    st.dataframe(bookings)

    user_bookings = bookings[
        bookings["user_name"] == current_user
    ]
# ----------------------------------
# ANALYTICS
# ----------------------------------

elif menu == "Admin Analytics":

    st.title(
        "📊 Utilization Analytics"
    )

    fig = generate_heatmap()

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        get_bookings()
    )
    import pandas as pd
from database import get_connection

conn = get_connection()

df = pd.read_sql_query(
    "PRAGMA table_info(users)",
    conn
)

st.dataframe(df)

conn.close()
