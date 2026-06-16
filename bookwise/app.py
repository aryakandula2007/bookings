import streamlit as st
import pandas as pd
import base64
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



from analytics import (
    generate_heatmap,
    peak_hours_chart,
    booking_trend_chart,
    most_popular_rooms_chart,
    user_activity_chart,
    best_time_to_visit,
    dashboard_summary
)

from ai_recommendation import (
    recommend_room,
    recommend_multiple_rooms
)

from email_service import (
    send_booking_confirmation,
    send_waitlist_notification
)

from calendar_service import (
    add_calendar_event
)

# ----------------------------------
# PAGE CONFIG
# ----------------------------------

st.set_page_config(
    page_title="BookWise",
    page_icon="📚",
    layout="wide"
)

# ----------------------------------
# DATABASE INIT
# ----------------------------------

initialize_db()

# ----------------------------------
# BACKGROUND IMAGE
# ----------------------------------

def set_background():

    st.markdown(
        """
        <style>

        .stApp{
            background: linear-gradient(
            135deg,
            #f5f7fa,
            #c3cfe2
            );
        }

        [data-testid="stSidebar"]{
            background:#1e3a5f;
        }

        [data-testid="stSidebar"] *{
            color:white;
        }

        .metric-card{
            padding:20px;
            border-radius:15px;
            background:white;
            box-shadow:0px 4px 12px rgba(0,0,0,0.15);
        }

        </style>
        """,
        unsafe_allow_html=True
    )

set_background()

# ----------------------------------
# SESSION
# ----------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ----------------------------------
# LOGIN
# ----------------------------------

if not st.session_state.logged_in:

    auth_page()
    st.stop()

# ----------------------------------
# SIDEBAR
# ----------------------------------

st.sidebar.title("📚 BookWise")

st.sidebar.success(
    f"Welcome, {st.session_state.username}"
)

if st.sidebar.button("Logout"):

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

    st.markdown(
        """
        <h1 style='text-align:center;'>
        📚 BookWise
        </h1>

        <h4 style='text-align:center;'>
        Smart Campus Resource Booking
        </h4>
        """,
        unsafe_allow_html=True
    )

    summary = dashboard_summary()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Bookings",
        summary["total_bookings"]
    )

    col2.metric(
        "Users",
        summary["total_users"]
    )

    col3.metric(
        "Rooms Used",
        summary["total_rooms_used"]
    )

    col4.metric(
        "Best Time",
        summary["best_time"]
    )

    st.divider()

    st.subheader("Available Rooms")

    rooms = get_rooms()

    st.dataframe(
        rooms,
        use_container_width=True
    )

    st.divider()

    st.subheader("Recent Bookings")

    bookings = get_bookings()

    st.dataframe(
        bookings.tail(10),
        use_container_width=True
    )

# ----------------------------------
# BOOK RESOURCE
# ----------------------------------

elif menu == "Book Resource":

    st.title("📅 Book a Resource")

    rooms = get_rooms()

    user = st.session_state.username

    email = st.text_input(
        "Email Address"
    )

    room_name = st.selectbox(
        "Select Room",
        rooms["room_name"]
    )

    room_id = int(
        rooms[
            rooms["room_name"] == room_name
        ]["id"].iloc[0]
    )

    st.info(
        f"Selected Room: {room_name}"
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

    st.subheader(
        "Available Slots"
    )

    slots = get_available_slots(
        room_id,
        booking_date
    )

    if len(slots) == 0:

        st.error(
            "No slots available"
        )

    else:

        for start, end in slots:

            st.success(
                f"🟢 Available: {start} - {end}"
            )

    if st.button("Book Now"):

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

            st.balloons()

            st.success(
                f"Booking Successful! ID: {booking_id}"
            )

            

            try:

                send_booking_confirmation(
                    email,
                    booking_id,
                    room_name,
                    booking_date,
                    start_time,
                    end_time
                )

                st.success(
                    "Confirmation email sent."
                )

            except:
                pass

            try:

                calendar_file = add_calendar_event(
                    booking_id,
                    room_name,
                    booking_date,
                    start_time,
                    end_time
                )

                with open(
                    calendar_file,
                    "rb"
                ) as file:

                    st.download_button(
                        "📅 Download Calendar Event",
                        data=file,
                        file_name=f"booking_{booking_id}.ics",
                        mime="text/calendar"
                    )

            except:
                pass

        else:

            add_to_waitlist(
                room_id,
                user,
                email
            )

            try:

                send_waitlist_notification(
                    email,
                    room_name
                )

            except:
                pass

            st.warning(
                "Room already booked. Added to waitlist."
            )
 # ----------------------------------
# AVAILABILITY
# ----------------------------------

elif menu == "Availability":

    st.title("🔍 Room Availability")

    rooms = get_rooms()

    selected_date = st.date_input(
        "Select Date",
        key="availability_date"
    )

    for _, room in rooms.iterrows():

        with st.expander(
            f"🏢 {room['room_name']}",
            expanded=False
        ):

            room_schedule = get_room_schedule(
                room["id"],
                selected_date
            )

            available_slots = get_available_slots(
                room["id"],
                selected_date
            )

            st.subheader("Booked Slots")

            if room_schedule.empty:

                st.success(
                    "✅ No bookings for this day"
                )

            else:

                for _, booking in room_schedule.iterrows():

                    st.error(
                        f"🔴 Booked: "
                        f"{booking['start_time']} "
                        f"- "
                        f"{booking['end_time']}"
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
                "Available Slots"
            )

            if len(available_slots) == 0:

                st.warning(
                    "No available slots."
                )

            else:

                for start, end in available_slots:

                    st.success(
                        f"🟢 Available: {start} - {end}"
                    )

# ----------------------------------
# AI RECOMMENDATION
# ----------------------------------

elif menu == "AI Recommendation":

    st.title(
        "🤖 Smart Room Recommendation"
    )

    attendees = st.number_input(
        "Number of Attendees",
        min_value=1,
        value=5
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

        if (
            alternatives is not None
            and
            not alternatives.empty
        ):

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

    st.title(
        "📖 My Bookings"
    )

    current_user = (
        st.session_state.username
    )

    user_bookings = (
        get_user_bookings(
            current_user
        )
    )

    if user_bookings.empty:

        st.warning(
            "No bookings found."
        )

    else:

        st.dataframe(
            user_bookings,
            use_container_width=True
        )

        st.metric(
            "Total My Bookings",
            len(user_bookings)
        )

# ----------------------------------
# ANALYTICS
# ----------------------------------

elif menu == "Analytics":

    st.title(
        "📊 Analytics Dashboard"
    )

    summary = dashboard_summary()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Bookings",
        summary["total_bookings"]
    )

    col2.metric(
        "Active Users",
        summary["total_users"]
    )

    col3.metric(
        "Rooms Used",
        summary["total_rooms_used"]
    )

    col4.metric(
        "Best Time",
        summary["best_time"]
    )

    st.divider()

    st.subheader(
        "🔥 Room Utilization Heatmap"
    )

    try:

        st.plotly_chart(
            generate_heatmap(),
            use_container_width=True
        )

    except Exception as e:

        st.warning(
            f"Heatmap Error: {e}"
        )

    st.divider()

    st.subheader(
        "🏆 Most Popular Rooms"
    )

    try:

        st.plotly_chart(
            most_popular_rooms_chart(),
            use_container_width=True
        )

    except Exception as e:

        st.warning(
            f"Chart Error: {e}"
        )

    st.divider()

    st.subheader(
        "⏰ Peak Usage Hours"
    )

    try:

        st.plotly_chart(
            peak_hours_chart(),
            use_container_width=True
        )

    except Exception as e:

        st.warning(
            f"Chart Error: {e}"
        )

    st.divider()

    st.subheader(
        "📈 Booking Trends"
    )

    try:

        st.plotly_chart(
            booking_trend_chart(),
            use_container_width=True
        )

    except Exception as e:

        st.warning(
            f"Chart Error: {e}"
        )

    st.divider()

    st.subheader(
        "👤 User Activity"
    )

    try:

        st.plotly_chart(
            user_activity_chart(),
            use_container_width=True
        )

    except Exception as e:

        st.warning(
            f"Chart Error: {e}"
        )

    st.divider()

    st.subheader(
        "📋 All Bookings"
    )

    bookings = get_bookings()

    if bookings.empty:

        st.info(
            "No bookings available."
        )

    else:

        st.dataframe(
            bookings,
            use_container_width=True
        )     