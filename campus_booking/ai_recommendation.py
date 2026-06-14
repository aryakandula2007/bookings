from database import get_rooms
# ----------------------------------
# RECOMMEND ROOM
# ----------------------------------

def recommend_room(
    attendees
):

    rooms = get_rooms()

    suitable_rooms = rooms[
        rooms["capacity"]
        >= attendees
    ]

    if suitable_rooms.empty:

        return (
            "No suitable room "
            "available for this group size."
        )

    suitable_rooms = (
        suitable_rooms
        .sort_values(
            by="capacity"
        )
    )

    recommended_room = (
        suitable_rooms
        .iloc[0]
    )

    return (
        f"{recommended_room['room_name']} "
        f"(Capacity: "
        f"{recommended_room['capacity']})"
    )


# ----------------------------------
# TOP 3 RECOMMENDATIONS
# ----------------------------------

def recommend_multiple_rooms(
    attendees
):

    rooms = get_rooms()

    suitable_rooms = rooms[
        rooms["capacity"]
        >= attendees
    ]

    if suitable_rooms.empty:

        return []

    suitable_rooms = (
        suitable_rooms
        .sort_values(
            by="capacity"
        )
        .head(3)
    )

    recommendations = []

    for _, room in suitable_rooms.iterrows():

        recommendations.append(
            {
                "room_name":
                room["room_name"],

                "capacity":
                room["capacity"],

                "location":
                room["location"]
            }
        )

    return recommendations

    