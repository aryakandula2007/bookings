import sqlite3
import pandas as pd

DB_NAME = "campus.db"

# ------------------------------------
# CONNECTION
# ------------------------------------

def get_connection():
    return sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )

# ------------------------------------
# DATABASE INITIALIZATION
# ------------------------------------

def initialize_db():

    conn = get_connection()
    cursor = conn.cursor()

    # ---------------- USERS ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT DEFAULT 'student'
    )
    """)

    # ---------------- ROOMS ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_name TEXT UNIQUE,
        capacity INTEGER,
        resource_type TEXT,
        location TEXT
    )
    """)

    # ---------------- BOOKINGS ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id INTEGER,
        user_name TEXT,
        email TEXT,
        booking_date TEXT,
        start_time TEXT,
        end_time TEXT,
        status TEXT DEFAULT 'Booked',

        FOREIGN KEY(room_id)
        REFERENCES rooms(id)
    )
    """)

    # ---------------- WAITLIST ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS waitlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id INTEGER,
        user_name TEXT,
        email TEXT,
        request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(room_id)
        REFERENCES rooms(id)
    )
    """)

    # ---------------- CHECK INS ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS checkins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id INTEGER,
        checkin_time TIMESTAMP,
        checkout_time TIMESTAMP,

        FOREIGN KEY(booking_id)
        REFERENCES bookings(id)
    )
    """)

    # ---------------- RESOURCE USAGE ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usage_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id INTEGER,
        booking_id INTEGER,
        usage_date TEXT,

        FOREIGN KEY(room_id)
        REFERENCES rooms(id)
    )
    """)

    conn.commit()

    # ------------------------------------
    # DEFAULT ROOMS
    # ------------------------------------

    default_rooms = [

        (
            "Study Room A",
            4,
            "Study Room",
            "Library Floor 1"
        ),

        (
            "Study Room B",
            8,
            "Study Room",
            "Library Floor 2"
        ),

        (
            "Computer Lab 1",
            40,
            "Computer Lab",
            "Engineering Block"
        ),

        (
            "Projector Room",
            20,
            "Projector Facility",
            "Admin Building"
        ),

        (
            "Conference Hall",
            50,
            "Conference",
            "Main Campus"
        )

    ]

    for room in default_rooms:

        try:

            cursor.execute("""
            INSERT INTO rooms
            (
                room_name,
                capacity,
                resource_type,
                location
            )
            VALUES (?,?,?,?)
            """, room)

        except:
            pass

    conn.commit()
    conn.close()

# ------------------------------------
# ROOM FUNCTIONS
# ------------------------------------

def get_rooms():

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM rooms",
        conn
    )

    conn.close()

    return df

def add_room(
    room_name,
    capacity,
    resource_type,
    location
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO rooms
    (
        room_name,
        capacity,
        resource_type,
        location
    )
    VALUES (?,?,?,?)
    """,
    (
        room_name,
        capacity,
        resource_type,
        location
    ))

    conn.commit()
    conn.close()

# ------------------------------------
# USER FUNCTIONS
# ------------------------------------

def add_user(
    name,
    email,
    role="student"
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO users
    (
        name,
        email,
        role
    )
    VALUES (?,?,?)
    """,
    (
        name,
        email,
        role
    ))

    conn.commit()
    conn.close()

def get_users():

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM users",
        conn
    )

    conn.close()

    return df

# ------------------------------------
# BOOKING FUNCTIONS
# ------------------------------------

def create_booking(
    room_id,
    user_name,
    email,
    booking_date,
    start_time,
    end_time
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO bookings
    (
        room_id,
        user_name,
        email,
        booking_date,
        start_time,
        end_time
    )
    VALUES (?,?,?,?,?,?)
    """,
    (
        room_id,
        user_name,
        email,
        str(booking_date),
        str(start_time),
        str(end_time)
    ))

    booking_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return booking_id

def get_bookings():

    conn = get_connection()

    query = """
    SELECT
        b.id,
        b.room_id,
        r.room_name,
        b.user_name,
        b.email,
        b.booking_date,
        b.start_time,
        b.end_time,
        b.status

    FROM bookings b

    JOIN rooms r
    ON b.room_id = r.id
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df

# ------------------------------------
# WAITLIST FUNCTIONS
# ------------------------------------

def add_waitlist(
    room_id,
    user_name,
    email
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO waitlist
    (
        room_id,
        user_name,
        email
    )
    VALUES (?,?,?)
    """,
    (
        room_id,
        user_name,
        email
    ))

    conn.commit()
    conn.close()

def get_waitlist():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM waitlist
        ORDER BY request_time ASC
        """,
        conn
    )

    conn.close()

    return df

# ------------------------------------
# CHECK-IN FUNCTIONS
# ------------------------------------

def check_in(
    booking_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO checkins
    (
        booking_id,
        checkin_time
    )
    VALUES
    (
        ?,
        CURRENT_TIMESTAMP
    )
    """,
    (booking_id,)
    )

    conn.commit()
    conn.close()

def check_out(
    booking_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE checkins
    SET checkout_time =
    CURRENT_TIMESTAMP
    WHERE booking_id = ?
    """,
    (booking_id,)
    )

    conn.commit()
    conn.close()

# ------------------------------------
# ANALYTICS
# ------------------------------------

def get_usage_logs():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM usage_logs
        """,
        conn
    )

    conn.close()

    return df

# ------------------------------------
# DELETE BOOKING
# ------------------------------------

def cancel_booking(
    booking_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM bookings
    WHERE id = ?
    """,
    (booking_id,)
    )

    conn.commit()
    conn.close()
def create_user(
    username,
    email,
    password
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                email,
                password
            )
            VALUES (?,?,?)
            """,
            (
                username,
                email,
                password
            )
        )

        conn.commit()

        return True

    except:

        return False

    finally:

        conn.close()
def authenticate_user(
    username,
    password
):

    conn = get_connection()

    cursor = conn.cursor()
    try:

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username=?
        AND password=?
        """,
        (
            username,
            password
        )
    )

    user = cursor.fetchone()

    

    return user
    except Exception as e:

        print("DATABASE ERROR:", e)
        raise

    finally:

        conn.close()
