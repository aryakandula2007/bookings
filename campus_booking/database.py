import sqlite3
import pandas as pd

DB_NAME = "campus.db"


# -----------------------------
# CONNECTION
# -----------------------------

def get_connection():
    return sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )


# -----------------------------
# INITIALIZE DATABASE
# -----------------------------

def initialize_db():

    conn = get_connection()
    cursor = conn.cursor()

    # USERS

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'student'
    )
    """)

    # ROOMS

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rooms(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_name TEXT UNIQUE,
        capacity INTEGER,
        resource_type TEXT,
        location TEXT
    )
    """)

    # BOOKINGS

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
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

    # WAITLIST

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS waitlist(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id INTEGER,
        user_name TEXT,
        email TEXT,
        request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    # DEFAULT ROOMS

    rooms = [

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
            "Computer Lab",
            40,
            "Lab",
            "Engineering Block"
        ),

        (
            "Projector Room",
            20,
            "Presentation",
            "Admin Building"
        )
    ]

    for room in rooms:

        try:

            cursor.execute(
                """
                INSERT INTO rooms
                (
                    room_name,
                    capacity,
                    resource_type,
                    location
                )
                VALUES (?,?,?,?)
                """,
                room
            )

        except:
            pass

    conn.commit()
    conn.close()


# -----------------------------
# AUTH FUNCTIONS
# -----------------------------

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

    except Exception as e:

        print("SIGNUP ERROR:", e)

        return False

    finally:

        conn.close()


def authenticate_user(
    username,
    password
):

    conn = get_connection()
    cursor = conn.cursor()

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

    conn.close()

    return user


# -----------------------------
# ROOMS
# -----------------------------

def get_rooms():

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM rooms",
        conn
    )

    conn.close()

    return df


# -----------------------------
# BOOKINGS
# -----------------------------

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

    cursor.execute(
        """
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
        )
    )

    booking_id = cursor.lastrowid
    print(
    "BOOKING INSERTED:",
    room_id,
    user_name,
    booking_date
)

    conn.commit()
    conn.close()

    return booking_id


def get_bookings():

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM bookings",
        conn
    )

    print("BOOKINGS TABLE:")
    print(df)

    conn.close()

    return df

# -----------------------------
# WAITLIST
# -----------------------------

def add_waitlist(
    room_id,
    user_name,
    email
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
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
        ORDER BY request_time
        """,
        conn
    )

    conn.close()

    return df