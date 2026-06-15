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

def most_popular_rooms():

    bookings = get_bookings()

    if bookings.empty:
        return pd.DataFrame()

    if "room_name" not in bookings.columns:
        return pd.DataFrame()

    return (
        bookings
        .groupby("room_name")
        .size()
        .reset_index(name="bookings")
        .sort_values(
            "bookings",
            ascending=False
        )
    )


# ----------------------------------
# DAILY BOOKINGS
# ----------------------------------

def daily_booking_stats():

    bookings = get_bookings()

    if bookings.empty:
        return pd.DataFrame()

    if "booking_date" not in bookings.columns:
        return pd.DataFrame()

    return (
        bookings
        .groupby("booking_date")
        .size()
        .reset_index(name="count")
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

        return px.bar(
            title="No Bookings Found"
        )

    if "start_time" not in bookings.columns:

        return px.bar(
            title="start_time column missing"
        )

    bookings = bookings.copy()

    bookings["hour"] = (
        bookings["start_time"]
        .astype(str)
        .str[:2]
    )

    peak = (
        bookings
        .groupby("hour")
        .size()
        .reset_index(name="bookings")
    )

    fig = px.bar(
        peak,
        x="hour",
        y="bookings",
        title="Peak Usage Hours"
    )

    return fig


# ----------------------------------
# BOOKING TREND
# ----------------------------------

def booking_trend_chart():

    daily = daily_booking_stats()

    if daily.empty:

        return px.line(
            title="No Booking Trend Data"
        )

    fig = px.line(
        daily,
        x="booking_date",
        y="count",
        markers=True,
        title="Booking Trend"
    )

    return fig


# ----------------------------------
# UTILIZATION TABLE
# ----------------------------------

def utilization_table():

    bookings = get_bookings()

    if bookings.empty:
        return pd.DataFrame()

    if "room_name" not in bookings.columns:
        return pd.DataFrame()

    return (
        bookings
        .groupby("room_name")
        .size()
        .reset_index(name="bookings")
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
    
    