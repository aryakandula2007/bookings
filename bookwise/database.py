import sqlite3
import pandas as pd

DB_NAME = "bookwise.db"


# ----------------------------------
# CONNECTION
# ----------------------------------

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


# ----------------------------------
# INITIALIZE DATABASE
# ----------------------------------

def initialize_db():

    conn = get_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # Rooms Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_name TEXT,
        capacity INTEGER
    )
    """)

    # Bookings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id INTEGER,
        user_name TEXT,
        email TEXT,
        booking_date TEXT,
        start_time TEXT,
        end_time TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Waitlist Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS waitlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id INTEGER,
        user_name TEXT,
        email TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Default Rooms
    cursor.execute("SELECT COUNT(*) FROM rooms")
    count = cursor.fetchone()[0]

    if count == 0:

        rooms = [
            ("Library Study Room", 4),
            ("Conference Room", 12),
            ("Seminar Hall", 50),
            ("Computer Lab", 30),
            ("Discussion Room", 8)
        ]

        cursor.executemany(
            """
            INSERT INTO rooms(room_name, capacity)
            VALUES (?,?)
            """,
            rooms
        )

    conn.commit()
    conn.close()


# ----------------------------------
# USER FUNCTIONS
# ----------------------------------

def create_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users(username,password)
            VALUES (?,?)
            """,
            (username, password)
        )

        conn.commit()
        return True

    except Exception:
        return False

    finally:
        conn.close()


def authenticate_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username=? AND password=?
        """,
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    return user is not None


# ----------------------------------
# ROOM FUNCTIONS
# ----------------------------------

def get_rooms():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM rooms
        ORDER BY room_name
        """,
        conn
    )

    conn.close()

    return df


def get_room_by_id(room_id):

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM rooms
        WHERE id=?
        """,
        conn,
        params=(room_id,)
    )

    conn.close()

    return df


# ----------------------------------
# BOOKING FUNCTIONS
# ----------------------------------

def add_booking(
    room_id,
    user_name,
    email,
    booking_date,
    start_time,
    end_time
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO bookings(
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
        )
    )

    booking_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return booking_id


def get_bookings():

    conn = get_connection()

    query = """
    SELECT
        b.id,
        r.room_name,
        b.room_id,
        b.user_name,
        b.email,
        b.booking_date,
        b.start_time,
        b.end_time,
        b.created_at
    FROM bookings b
    JOIN rooms r
    ON b.room_id = r.id
    ORDER BY b.booking_date DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def get_room_bookings(room_id, booking_date):

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM bookings
        WHERE room_id=?
        AND booking_date=?
        ORDER BY start_time
        """,
        conn,
        params=(room_id, str(booking_date))
    )

    conn.close()

    return df


def delete_booking(booking_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM bookings
        WHERE id=?
        """,
        (booking_id,)
    )

    conn.commit()
    conn.close()


# ----------------------------------
# WAITLIST FUNCTIONS
# ----------------------------------

def add_waitlist(
    room_id,
    user_name,
    email
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO waitlist(
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
        )
    )

    conn.commit()
    conn.close()


def get_waitlist():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM waitlist
        ORDER BY created_at DESC
        """,
        conn
    )

    conn.close()

    return df


# ----------------------------------
# DASHBOARD HELPERS
# ----------------------------------

def total_rooms():
    return len(get_rooms())


def total_bookings():
    return len(get_bookings())


def total_users():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM users
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count
    