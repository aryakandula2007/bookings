import pandas as pd
import plotly.express as px

from database import (
    get_bookings,
    get_rooms
)

# ----------------------------------
# DASHBOARD METRICS
# ----------------------------------

def get_dashboard_metrics():

    rooms = get_rooms()
    bookings = get_bookings()

    return {
        "total_rooms": len(rooms),
        "total_bookings": len(bookings)
    }


# ----------------------------------
# POPULAR ROOMS
# ----------------------------------

def most_popular_rooms_chart():

    bookings = get_bookings()

    if bookings.empty:
        return px.bar(title="No Booking Data")

    popular = (
        bookings
        .groupby("room_name")
        .size()
        .reset_index(name="bookings")
    )

    return px.bar(
        popular,
        x="room_name",
        y="bookings",
        title="Most Popular Rooms"
    )

# ----------------------------------
# ROOM UTILIZATION
# ----------------------------------

def generate_heatmap():

    bookings = get_bookings()

    if bookings.empty:

        return px.bar(
            title="No Bookings Found"
        )

    if "room_name" not in bookings.columns:

        return px.bar(
            title="room_name column missing"
        )

    room_usage = (
        bookings
        .groupby("room_name")
        .size()
        .reset_index(name="bookings")
    )

    fig = px.bar(
        room_usage,
        x="room_name",
        y="bookings",
        title="Room Utilization"
    )

    return fig


# ----------------------------------
# PEAK HOURS
# ----------------------------------

def peak_hours_chart():

    bookings = get_bookings()

    if bookings.empty:
        return px.bar(title="No Booking Data")

    bookings["hour"] = (
        bookings["start_time"]
        .astype(str)
        .str[:2]
        .astype(int)
    )

    peak = (
        bookings
        .groupby("hour")
        .size()
        .reset_index(name="bookings")
    )

    return px.bar(
        peak,
        x="hour",
        y="bookings",
        title="Peak Usage Hours"
    )


# ----------------------------------
# BOOKING TREND
# ----------------------------------

def booking_trend_chart():

    bookings = get_bookings()

    if bookings.empty:
        return px.line(title="No Booking Data")

    trend = (
        bookings
        .groupby("booking_date")
        .size()
        .reset_index(name="bookings")
    )

    return px.line(
        trend,
        x="booking_date",
        y="bookings",
        markers=True,
        title="Booking Trend Over Time"
    )

def user_activity_chart():

    bookings = get_bookings()

    if bookings.empty:
        return px.bar(title="No Booking Data")

    users = (
        bookings
        .groupby("user_name")
        .size()
        .reset_index(name="bookings")
        .sort_values(
            "bookings",
            ascending=False
        )
    )

    return px.bar(
        users,
        x="user_name",
        y="bookings",
        title="Top Users by Bookings"
    )

# ----------------------------------
# DEBUG FUNCTION
# ----------------------------------

def booking_debug():

    bookings = get_bookings()

    return {
        "rows": len(bookings),
        "columns": list(bookings.columns)
    }
    
    