import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from database import (
    get_rooms,
    get_bookings
)

# ----------------------------------
# TRAIN MODEL
# ----------------------------------

def train_model():

    bookings = get_bookings()

    if len(bookings) < 5:
        return None

    data = []

    for _, row in bookings.iterrows():

        try:

            start_hour = int(
                str(
                    row["start_time"]
                ).split(":")[0]
            )

            data.append({
                "hour": start_hour,
                "room_id": row["room_id"]
            })

        except:
            pass

    if len(data) < 5:
        return None

    df = pd.DataFrame(data)

    X = df[["hour"]]
    y = df["room_id"]

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    return model

# ----------------------------------
# AI ROOM RECOMMENDATION
# ----------------------------------

def recommend_room(
    attendees
):

    rooms = get_rooms()

    suitable_rooms = rooms[
        rooms["capacity"] >= attendees
    ]

    if suitable_rooms.empty:

        return (
            "No room available "
            "for that capacity."
        )

    bookings = get_bookings()

    room_scores = {}

    for _, room in suitable_rooms.iterrows():

        room_id = room["id"]

        usage_count = len(

            bookings[
                bookings["room_id"]
                == room_id
            ]

        )

        room_scores[
            room["room_name"]
        ] = usage_count

    recommended = min(
        room_scores,
        key=room_scores.get
    )

    return recommended

# ----------------------------------
# TOP ROOMS
# ----------------------------------

def top_rooms():

    bookings = get_bookings()

    if bookings.empty:
        return []

    popularity = (
        bookings
        .groupby("room_name")
        .size()
        .reset_index(
            name="bookings"
        )
        .sort_values(
            "bookings",
            ascending=False
        )
    )

    return popularity

# ----------------------------------
# PEAK HOURS
# ----------------------------------

def peak_hours():

    bookings = get_bookings()

    if bookings.empty:

        return []

    hours = []

    for _, row in bookings.iterrows():

        try:

            hour = int(
                str(
                    row["start_time"]
                ).split(":")[0]
            )

            hours.append(hour)

        except:
            pass

    if not hours:
        return []

    df = pd.DataFrame(
        {
            "hour": hours
        }
    )

    result = (
        df.groupby("hour")
        .size()
        .reset_index(
            name="bookings"
        )
        .sort_values(
            "bookings",
            ascending=False
        )
    )

    return result

# ----------------------------------
# PREDICT ROOM
# ----------------------------------

def predict_best_room(
    hour
):

    model = train_model()

    if model is None:

        return (
            "Not enough booking "
            "history available."
        )

    prediction = model.predict(
        [[hour]]
    )[0]

    rooms = get_rooms()

    room = rooms[
        rooms["id"]
        == prediction
    ]

    if room.empty:

        return (
            "Prediction unavailable."
        )

    return room.iloc[0][
        "room_name"
    ]

# ----------------------------------
# UTILIZATION SCORE
# ----------------------------------

def utilization_score():

    rooms = get_rooms()

    bookings = get_bookings()

    results = []

    for _, room in rooms.iterrows():

        room_bookings = len(

            bookings[
                bookings["room_id"]
                == room["id"]
            ]

        )

        score = (
            room_bookings * 10
        )

        results.append(
            {
                "room":
                room["room_name"],

                "score":
                score
            }
        )

    return pd.DataFrame(
        results
    )

# ----------------------------------
# ROOM INSIGHTS
# ----------------------------------

def room_insights():

    top = top_rooms()

    peak = peak_hours()

    return {
        "top_rooms": top,
        "peak_hours": peak
    }
    