import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# -----------------------
# DATABASE SETUP
# -----------------------

conn = sqlite3.connect("campus_resources.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS rooms(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_name TEXT UNIQUE,
    capacity INTEGER,
    resource_type TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS bookings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER,
    user_name TEXT,
    booking_date TEXT,
    start_time TEXT,
    end_time TEXT
)
""")

conn.commit()

# -----------------------
# SAMPLE ROOMS
# -----------------------

sample_rooms = [
    ("Study Room A", 6, "Study Room"),
    ("Study Room B", 8, "Study Room"),
    ("Library Conference Hall", 25, "Conference"),
    ("Projector Room", 15, "Projector"),
    ("Computer Lab", 40, "Computer Lab")
]

for room in sample_rooms:
    try:
        c.execute(
            "INSERT INTO rooms(room_name, capacity, resource_type) VALUES(?,?,?)",
            room
        )
    except:
        pass

conn.commit()

# -----------------------
# FUNCTIONS
# -----------------------

def get_rooms():
    return pd.read_sql_query(
        "SELECT * FROM rooms",
        conn
    )

def get_bookings():
    return pd.read_sql_query(
        """
        SELECT b.id,
               r.room_name,
               b.user_name,
               b.booking_date,
               b.start_time,
               b.end_time
        FROM bookings b
        JOIN rooms r
        ON b.room_id = r.id
        """,
        conn
    )

def room_available(room_id, date, start_time, end_time):

    query = """
    SELECT *
    FROM bookings
    WHERE room_id=?
    AND booking_date=?
    """

    existing = c.execute(
        query,
        (room_id, date)
    ).fetchall()

    for booking in existing:

        existing_start = booking[4]
        existing_end = booking[5]

        if (
            start_time < existing_end and
            end_time > existing_start
        ):
            return False

    return True

# -----------------------
# UI
# -----------------------

st.set_page_config(
    page_title="Campus Resource Booking System",
    layout="wide"
)

st.title("🏫 Campus Resource Booking System")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Check Availability",
        "Book Resource",
        "My Bookings",
        "Admin Dashboard"
    ]
)

# -----------------------
# CHECK AVAILABILITY
# -----------------------

if menu == "Check Availability":

    st.header("Available Resources")

    rooms = get_rooms()

    selected_date = st.date_input(
        "Select Date"
    )

    bookings = get_bookings()

    for _, room in rooms.iterrows():

        room_bookings = bookings[
            (bookings["room_name"] == room["room_name"])
            &
            (bookings["booking_date"]
             == str(selected_date))
        ]

        with st.expander(room["room_name"]):

            st.write(
                f"Type: {room['resource_type']}"
            )

            st.write(
                f"Capacity: {room['capacity']}"
            )

            if room_bookings.empty:
                st.success("Available all day")
            else:
                st.warning("Booked Slots")

                st.dataframe(
                    room_bookings[
                        [
                            "user_name",
                            "start_time",
                            "end_time"
                        ]
                    ]
                )

# -----------------------
# BOOK RESOURCE
# -----------------------

elif menu == "Book Resource":

    st.header("Reserve a Resource")

    user_name = st.text_input(
        "Your Name"
    )

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

    if st.button("Book Now"):

        room_id = rooms[
            rooms["room_name"] == room_name
        ]["id"].iloc[0]

        start = start_time.strftime("%H:%M")
        end = end_time.strftime("%H:%M")

        if start >= end:
            st.error(
                "End time must be after start time."
            )

        elif room_available(
            room_id,
            str(booking_date),
            start,
            end
        ):

            c.execute(
                """
                INSERT INTO bookings
                (
                room_id,
                user_name,
                booking_date,
                start_time,
                end_time
                )
                VALUES(?,?,?,?,?)
                """,
                (
                    room_id,
                    user_name,
                    str(booking_date),
                    start,
                    end
                )
            )

            conn.commit()

            st.success(
                "Booking Confirmed!"
            )

        else:
            st.error(
                "Room already booked during that period."
            )

# -----------------------
# MY BOOKINGS
# -----------------------

elif menu == "My Bookings":

    st.header("View Your Reservations")

    user = st.text_input(
        "Enter Your Name"
    )

    if user:

        data = pd.read_sql_query(
            """
            SELECT r.room_name,
                   b.booking_date,
                   b.start_time,
                   b.end_time
            FROM bookings b
            JOIN rooms r
            ON b.room_id=r.id
            WHERE b.user_name=?
            """,
            conn,
            params=(user,)
        )

        st.dataframe(
            data,
            use_container_width=True
        )

# -----------------------
# ADMIN DASHBOARD
# -----------------------

elif menu == "Admin Dashboard":

    st.header("Admin Dashboard")

    st.subheader("Add New Resource")

    room_name = st.text_input(
        "Room Name"
    )

    capacity = st.number_input(
        "Capacity",
        min_value=1
    )

    resource_type = st.selectbox(
        "Resource Type",
        [
            "Study Room",
            "Computer Lab",
            "Projector Room",
            "Library Facility"
        ]
    )

    if st.button("Add Resource"):

        try:

            c.execute(
                """
                INSERT INTO rooms
                (
                room_name,
                capacity,
                resource_type
                )
                VALUES(?,?,?)
                """,
                (
                    room_name,
                    capacity,
                    resource_type
                )
            )

            conn.commit()

            st.success(
                "Resource Added Successfully"
            )

        except:
            st.error(
                "Room already exists."
            )

    st.subheader("Current Resources")

    st.dataframe(
        get_rooms(),
        use_container_width=True
    )

    st.subheader("All Bookings")

    st.dataframe(
        get_bookings(),
        use_container_width=True
    )