import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from database import get_bookings


# ----------------------------------
# LOAD BOOKINGS
# ----------------------------------

def load_bookings():

    try:
        bookings = get_bookings()

        if bookings is None:
            return pd.DataFrame()

        return bookings

    except Exception:
        return pd.DataFrame()


# ----------------------------------
# BEST TIME TO VISIT
# ----------------------------------

def best_time_to_visit():

    bookings = load_bookings()

    if bookings.empty:
        return "No booking data available"

    try:

        bookings["hour"] = (
            bookings["start_time"]
            .astype(str)
            .str[:2]
            .astype(int)
        )

        hour_counts = (
            bookings.groupby("hour")
            .size()
            .reset_index(name="count")
        )

        least_busy = hour_counts.sort_values(
            "count"
        ).iloc[0]["hour"]

        return f"{least_busy:02d}:00"

    except Exception:
        return "Not enough data"


# ----------------------------------
# ROOM UTILIZATION HEATMAP
# ----------------------------------

def generate_heatmap():

    bookings = load_bookings()

    if bookings.empty:

        fig = go.Figure()

        fig.add_annotation(
            text="No Booking Data Available",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=20)
        )

        return fig

    bookings["hour"] = (
        bookings["start_time"]
        .astype(str)
        .str[:2]
        .astype(int)
    )

    heatmap_data = (
        bookings.groupby(
            ["room_name", "hour"]
        )
        .size()
        .reset_index(name="count")
    )

    pivot = heatmap_data.pivot(
        index="room_name",
        columns="hour",
        values="count"
    ).fillna(0)

    fig = px.imshow(
        pivot,
        text_auto=True,
        aspect="auto",
        title="Room Utilization Heatmap"
    )

    fig.update_layout(
        height=500
    )

    return fig


# ----------------------------------
# PEAK HOURS CHART
# ----------------------------------

def peak_hours_chart():

    bookings = load_bookings()

    if bookings.empty:

        return px.bar(
            title="No Booking Data Available"
        )

    bookings["hour"] = (
        bookings["start_time"]
        .astype(str)
        .str[:2]
        .astype(int)
    )

    hourly = (
        bookings.groupby("hour")
        .size()
        .reset_index(name="bookings")
    )

    fig = px.bar(
        hourly,
        x="hour",
        y="bookings",
        title="Peak Booking Hours"
    )

    return fig


# ----------------------------------
# BOOKING TREND CHART
# ----------------------------------

def booking_trend_chart():

    bookings = load_bookings()

    if bookings.empty:

        return px.line(
            title="No Booking Data Available"
        )

    trend = (
        bookings.groupby("booking_date")
        .size()
        .reset_index(name="bookings")
    )

    fig = px.line(
        trend,
        x="booking_date",
        y="bookings",
        markers=True,
        title="Booking Trend"
    )

    return fig


# ----------------------------------
# MOST POPULAR ROOMS
# ----------------------------------

def most_popular_rooms_chart():

    bookings = load_bookings()

    if bookings.empty:

        return px.bar(
            title="No Booking Data Available"
        )

    room_counts = (
        bookings.groupby("room_name")
        .size()
        .reset_index(name="bookings")
        .sort_values(
            by="bookings",
            ascending=False
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
# USER ACTIVITY CHART
# ----------------------------------

def user_activity_chart():

    bookings = load_bookings()

    if bookings.empty:

        return px.bar(
            title="No Booking Data Available"
        )

    users = (
        bookings.groupby("user_name")
        .size()
        .reset_index(name="bookings")
        .sort_values(
            by="bookings",
            ascending=False
        )
    )

    fig = px.bar(
        users,
        x="user_name",
        y="bookings",
        title="User Activity"
    )

    return fig


# ----------------------------------
# KPI METRICS
# ----------------------------------

def total_bookings():

    bookings = load_bookings()

    return len(bookings)


def total_users():

    bookings = load_bookings()

    if bookings.empty:
        return 0

    return bookings["user_name"].nunique()


def total_rooms_used():

    bookings = load_bookings()

    if bookings.empty:
        return 0

    return bookings["room_name"].nunique()


# ----------------------------------
# DASHBOARD SUMMARY
# ----------------------------------

def dashboard_summary():

    return {
        "total_bookings": total_bookings(),
        "total_users": total_users(),
        "total_rooms_used": total_rooms_used(),
        "best_time": best_time_to_visit()
    }
    