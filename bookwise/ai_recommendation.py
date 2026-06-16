import pandas as pd
from database import get_rooms


# ----------------------------------
# RECOMMEND BEST ROOM
# ----------------------------------

def recommend_room(attendees):

    rooms = get_rooms()

    if rooms.empty:
        return "No rooms available."

    suitable_rooms = rooms[
        rooms["capacity"] >= attendees
    ].copy()

    if suitable_rooms.empty:
        return (
            f"No room can accommodate "
            f"{attendees} attendees."
        )

    suitable_rooms["extra_space"] = (
        suitable_rooms["capacity"] - attendees
    )

    best_room = suitable_rooms.sort_values(
        by="extra_space"
    ).iloc[0]

    return (
        f"Recommended Room: "
        f"{best_room['room_name']} "
        f"(Capacity: {best_room['capacity']})"
    )


# ----------------------------------
# RECOMMEND MULTIPLE ROOMS
# ----------------------------------

def recommend_multiple_rooms(attendees):

    rooms = get_rooms()

    if rooms.empty:
        return pd.DataFrame()

    suitable_rooms = rooms[
        rooms["capacity"] >= attendees
    ].copy()

    if suitable_rooms.empty:
        return pd.DataFrame()

    suitable_rooms["extra_space"] = (
        suitable_rooms["capacity"] - attendees
    )

    suitable_rooms = suitable_rooms.sort_values(
        by="extra_space"
    )

    return suitable_rooms[
        [
            "room_name",
            "capacity"
        ]
    ]


# ----------------------------------
# RECOMMEND ROOM CATEGORY
# ----------------------------------

def recommend_room_type(attendees):

    if attendees <= 4:
        return "Library Study Room"

    elif attendees <= 10:
        return "Discussion Room"

    elif attendees <= 20:
        return "Conference Room"

    elif attendees <= 40:
        return "Computer Lab"

    else:
        return "Seminar Hall"


# ----------------------------------
# SMART RECOMMENDATION
# ----------------------------------

def smart_recommendation(attendees):

    room = recommend_room(attendees)

    category = recommend_room_type(
        attendees
    )

    return {
        "recommended_room": room,
        "suggested_category": category
    }
    