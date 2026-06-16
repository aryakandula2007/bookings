from icalendar import Calendar, Event
from datetime import datetime
import os


# ----------------------------------
# CALENDAR FOLDER
# ----------------------------------

CALENDAR_FOLDER = "calendar_events"


def create_calendar_folder():

    if not os.path.exists(CALENDAR_FOLDER):
        os.makedirs(CALENDAR_FOLDER)


# ----------------------------------
# CREATE CALENDAR EVENT
# ----------------------------------

def add_calendar_event(
    booking_id,
    room_name,
    booking_date,
    start_time,
    end_time
):

    create_calendar_folder()

    try:

        start_dt = datetime.strptime(
            f"{booking_date} {start_time}",
            "%Y-%m-%d %H:%M:%S"
        )

    except:

        start_dt = datetime.strptime(
            f"{booking_date} {start_time}",
            "%Y-%m-%d %H:%M"
        )

    try:

        end_dt = datetime.strptime(
            f"{booking_date} {end_time}",
            "%Y-%m-%d %H:%M:%S"
        )

    except:

        end_dt = datetime.strptime(
            f"{booking_date} {end_time}",
            "%Y-%m-%d %H:%M"
        )

    cal = Calendar()

    event = Event()

    event.add(
        "summary",
        f"BookWise - {room_name}"
    )

    event.add(
        "description",
        f"Booking ID: {booking_id}"
    )

    event.add(
        "dtstart",
        start_dt
    )

    event.add(
        "dtend",
        end_dt
    )

    cal.add_component(
        event
    )

    file_path = (
        f"{CALENDAR_FOLDER}/booking_{booking_id}.ics"
    )

    with open(
        file_path,
        "wb"
    ) as f:

        f.write(
            cal.to_ical()
        )

    return file_path


# ----------------------------------
# GET CALENDAR FILE
# ----------------------------------

def get_calendar_file(
    booking_id
):

    file_path = (
        f"{CALENDAR_FOLDER}/booking_{booking_id}.ics"
    )

    if os.path.exists(file_path):
        return file_path

    return None