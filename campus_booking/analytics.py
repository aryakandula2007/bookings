import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from database import (
    get_bookings,
    get_rooms
)

# ----------------------------------
# TOTAL METRICS
# ----------------------------------

def get_kpis():

    bookings = get_bookings()
    rooms = get_rooms()

    total_rooms = len(rooms)

    total_bookings = len(bookings)

    active_bookings = len(
        bookings[
            bookings["status"] == "Booked"
        ]
    )

    return {
        "total_rooms": total_rooms,
        "total_bookings": total_bookings,
        "active_bookings": active_bookings
    }

# ----------------------------------
# POPULAR ROOMS
# ----------------------------------

def room_popularity_chart():

    bookings = get_bookings()

    if bookings.empty:
        return None

    room_counts = (
        bookings
        .groupby("room_name")
        .size()
        .reset_index(
            name="bookings"
        )
    )

    fig = px.bar(
        room_counts,
        x="room_name",
        y="bookings",
        title="Most Popular Rooms"
    )

    return fig

# ----------------------------------
# DAILY BOOKINGS
# ----------------------------------

def daily_bookings_chart():

    bookings = get_bookings()

    if bookings.empty:
        return None

    daily = (
        bookings
        .groupby("booking_date")
        .size()
        .reset_index(
            name="bookings"
        )
    )

    fig = px.line(
        daily,
        x="booking_date",
        y="bookings",
        markers=True,
        title="Daily Booking Trend"
    )

    return fig

# ----------------------------------
# PEAK HOURS
# ----------------------------------

def peak_hour_chart():

    bookings = get_bookings()

    if bookings.empty:
        return None

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

    df = pd.DataFrame(
        {
            "hour": hours
        }
    )

    hourly = (
        df
        .groupby("hour")
        .size()
        .reset_index(
            name="bookings"
        )
    )

    fig = px.bar(
        hourly,
        x="hour",
        y="bookings",
        title="Peak Usage Hours"
    )

    return fig

# ----------------------------------
# UTILIZATION HEATMAP
# ----------------------------------

def generate_heatmap():

    bookings = get_bookings()

    if bookings.empty:

        fig = go.Figure()

        fig.update_layout(
            title="No booking data"
        )

        return fig

    data = []

    for _, row in bookings.iterrows():

        try:

            hour = int(
                str(
                    row["start_time"]
                ).split(":")[0]
            )

            data.append(
                {
                    "room":
                    row["room_name"],

                    "hour":
                    hour
                }
            )

        except:
            pass

    df = pd.DataFrame(data)

    heatmap = (
        df.groupby(
            [
                "room",
                "hour"
            ]
        )
        .size()
        .reset_index(
            name="count"
        )
    )

    fig = px.density_heatmap(
        heatmap,
        x="hour",
        y="room",
        z="count",
        title="Room Utilization Heatmap"
    )

    return fig

# ----------------------------------
# ROOM UTILIZATION %
# ----------------------------------

def utilization_table():

    rooms = get_rooms()
    bookings = get_bookings()

    results = []

    for _, room in rooms.iterrows():

        usage = len(

            bookings[
                bookings["room_id"]
                == room["id"]
            ]

        )

        utilization = (
            usage * 5
        )

        if utilization > 100:
            utilization = 100

        results.append(
            {
                "Room":
                room["room_name"],

                "Utilization (%)":
                utilization
            }
        )

    return pd.DataFrame(
        results
    )

# ----------------------------------
# TOP ROOMS
# ----------------------------------

def most_booked_rooms():

    bookings = get_bookings()

    if bookings.empty:
        return pd.DataFrame()

    result = (
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

    return result

# ----------------------------------
# ADMIN SUMMARY
# ----------------------------------

def admin_summary():

    kpis = get_kpis()

    popular = most_booked_rooms()

    utilization = utilization_table()

    return {
        "kpis": kpis,
        "popular_rooms": popular,
        "utilization": utilization
    }
    