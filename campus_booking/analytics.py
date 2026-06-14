import pandas as pd
import plotly.express as px

from database import (
    get_bookings,
    get_rooms
)

# ----------------------------------
# TOTAL METRICS
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

    popularity = (
        bookings
        .groupby("room_name")
        .size()
        .reset_index(name="bookings")
        .sort_values(
            "bookings",
            ascending=False
        )
    )

    return popularity


# ----------------------------------
# DAILY BOOKINGS
# ----------------------------------

def daily_booking_stats():

    bookings = get_bookings()

    if bookings.empty:
        return pd.DataFrame()

    daily = (
        bookings
        .groupby("booking_date")
        .size()
        .reset_index(name="count")
    )

    return daily


# ----------------------------------
# ROOM UTILIZATION CHART
# ----------------------------------

def generate_heatmap():

    bookings = get_bookings()

    if bookings.empty:

        fig = px.bar(
            title="No booking data available"
        )

        return fig

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
# PEAK HOURS CHART
# ----------------------------------

def peak_hours_chart():

    bookings = get_bookings()

    if bookings.empty:

        fig = px.bar(
            title="No booking data available"
        )

        return fig

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
# BOOKING TREND CHART
# ----------------------------------

def booking_trend_chart():

    daily = daily_booking_stats()

    if daily.empty:

        fig = px.line(
            title="No booking data available"
        )

        return fig

    fig = px.line(
        daily,
        x="booking_date",
        y="count",
        markers=True,
        title="Booking Trend"
    )

    return fig


# ----------------------------------
# ROOM UTILIZATION TABLE
# ----------------------------------

def utilization_table():

    bookings = get_bookings()

    if bookings.empty:
        return pd.DataFrame()

    utilization = (
        bookings
        .groupby("room_name")
        .size()
        .reset_index(name="bookings")
    )

    return utilization
    