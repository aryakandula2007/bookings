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
# GET ALL WAITLIST ENTRIES
# ----------------------------------

def get_waitlist_entries():

    return get_waitlist()


# ----------------------------------
# GET WAITLIST FOR A ROOM
# ----------------------------------

def get_room_waitlist(room_id):

    waitlist = get_waitlist()

    if waitlist.empty:
        return waitlist

    return waitlist[
        waitlist["room_id"] == room_id
    ]


# ----------------------------------
# WAITLIST COUNT
# ----------------------------------

def waitlist_count():

    waitlist = get_waitlist()

    return len(waitlist)


# ----------------------------------
# CHECK IF USER IS WAITLISTED
# ----------------------------------

def is_user_waitlisted(
    room_id,
    user_name
):

    waitlist = get_waitlist()

    if waitlist.empty:
        return False

    filtered = waitlist[
        (waitlist["room_id"] == room_id)
        &
        (
            waitlist["user_name"]
            .astype(str)
            .str.lower()
            ==
            str(user_name).lower()
        )
    ]

    return len(filtered) > 0


# ----------------------------------
# WAITLIST SUMMARY
# ----------------------------------

def waitlist_summary():

    waitlist = get_waitlist()

    if waitlist.empty:

        return {
            "total_waitlist": 0
        }

    return {
        "total_waitlist": len(waitlist)
    }