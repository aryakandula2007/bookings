from datetime import datetime
from database import get_connection

# ------------------------------------
# PRIORITY VALUES
# ------------------------------------

PRIORITY = {
    "faculty": 1,
    "staff": 2,
    "student": 3
}

# ------------------------------------
# ADD USER TO WAITLIST
# ------------------------------------

def add_to_waitlist(
    room_id,
    user_name,
    email,
    role="student"
):

    conn = get_connection()
    cursor = conn.cursor()

    priority = PRIORITY.get(
        role.lower(),
        3
    )

    cursor.execute(
        """
        INSERT INTO waitlist
        (
            room_id,
            user_name,
            email,
            request_time
        )
        VALUES
        (
            ?,
            ?,
            ?,
            CURRENT_TIMESTAMP
        )
        """,
        (
            room_id,
            user_name,
            email
        )
    )

    conn.commit()
    conn.close()

    return True


# ------------------------------------
# GET WAITLIST
# ------------------------------------

def get_waitlist():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM waitlist
        ORDER BY request_time ASC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# ------------------------------------
# GET WAITLIST FOR ROOM
# ------------------------------------

def get_room_waitlist(
    room_id
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM waitlist
        WHERE room_id = ?
        ORDER BY request_time ASC
        """,
        (room_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# ------------------------------------
# REMOVE WAITLIST ENTRY
# ------------------------------------

def remove_waitlist_entry(
    waitlist_id
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM waitlist
        WHERE id = ?
        """,
        (waitlist_id,)
    )

    conn.commit()
    conn.close()


# ------------------------------------
# NEXT USER IN QUEUE
# ------------------------------------

def next_user_for_room(
    room_id
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM waitlist
        WHERE room_id = ?
        ORDER BY request_time ASC
        LIMIT 1
        """,
        (room_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


# ------------------------------------
# PROMOTE USER
# ------------------------------------

def promote_user(
    room_id
):

    next_user = next_user_for_room(
        room_id
    )

    if not next_user:
        return None

    waitlist_id = next_user[0]

    remove_waitlist_entry(
        waitlist_id
    )

    return {
        "user_name": next_user[2],
        "email": next_user[3]
    }


# ------------------------------------
# WAIT TIME ESTIMATION
# ------------------------------------

def estimate_wait_time(
    room_id
):

    queue = get_room_waitlist(
        room_id
    )

    avg_booking_minutes = 60

    estimated_minutes = (
        len(queue)
        *
        avg_booking_minutes
    )

    return estimated_minutes


# ------------------------------------
# USER POSITION
# ------------------------------------

def get_position(
    room_id,
    email
):

    queue = get_room_waitlist(
        room_id
    )

    for index, user in enumerate(
        queue,
        start=1
    ):

        if user[3] == email:
            return index

    return None


# ------------------------------------
# WAITLIST COUNT
# ------------------------------------

def waitlist_count():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM waitlist
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


# ------------------------------------
# ROOM WAITLIST COUNT
# ------------------------------------

def room_waitlist_count(
    room_id
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM waitlist
        WHERE room_id = ?
        """,
        (room_id,)
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


# ------------------------------------
# ANALYTICS
# ------------------------------------

def busiest_waitlisted_room():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT room_id,
               COUNT(*) as total

        FROM waitlist

        GROUP BY room_id

        ORDER BY total DESC

        LIMIT 1
        """
    )

    result = cursor.fetchone()

    conn.close()

    return result


# ------------------------------------
# CLEAR WAITLIST
# ------------------------------------

def clear_room_waitlist(
    room_id
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM waitlist
        WHERE room_id = ?
        """,
        (room_id,)
    )

    conn.commit()
    conn.close()


# ------------------------------------
# AUTO NOTIFICATION HOOK
# ------------------------------------

def notify_promoted_user(
    email,
    room_name
):

    """
    Hook for email_service.py

    Example:

    send_email(
        email,
        subject,
        body
    )
    """

    print(
        f"""
        Notification sent to:
        {email}

        Room Available:
        {room_name}
        """
    )


# ------------------------------------
# AUTO PROCESS WAITLIST
# ------------------------------------

def process_waitlist(
    room_id,
    room_name
):

    promoted = promote_user(
        room_id
    )

    if promoted:

        notify_promoted_user(
            promoted["email"],
            room_name
        )

        return promoted

    return None


# ------------------------------------
# WAITLIST DASHBOARD DATA
# ------------------------------------

def waitlist_dashboard():

    conn = get_connection()

    query = """
    SELECT
        room_id,
        COUNT(*) AS queue_length

    FROM waitlist

    GROUP BY room_id
    """

    cursor = conn.cursor()

    cursor.execute(query)

    data = cursor.fetchall()

    conn.close()

    return data
    