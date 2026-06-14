from database import (
    add_waitlist,
    get_waitlist
)

# ----------------------------------
# ADD USER TO WAITLIST
# ----------------------------------

def add_to_waitlist(
    room_id,
    user_name,
    email
):

    add_waitlist(
        room_id,
        user_name,
        email
    )

    return True


# ----------------------------------
# GET ROOM WAITLIST
# ----------------------------------

def get_room_waitlist(
    room_id
):

    waitlist = get_waitlist()

    room_waitlist = waitlist[
        waitlist["room_id"]
        == room_id
    ]

    return room_waitlist


# ----------------------------------
# CHECK POSITION
# ----------------------------------

def get_waitlist_position(
    room_id,
    user_name
):

    room_waitlist = get_room_waitlist(
        room_id
    )

    for index, row in room_waitlist.iterrows():

        if row["user_name"] == user_name:

            return index + 1

    return None


# ----------------------------------
# COUNT WAITLIST USERS
# ----------------------------------

def waitlist_count(
    room_id
):

    room_waitlist = get_room_waitlist(
        room_id
    )

    return len(room_waitlist)


# ----------------------------------
# EXPORTS
# ----------------------------------

__all__ = [
    "add_to_waitlist",
    "get_room_waitlist",
    "get_waitlist_position",
    "waitlist_count"
]
