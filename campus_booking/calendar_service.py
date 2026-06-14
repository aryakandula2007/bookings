# ----------------------------------
# MOCK CALENDAR SERVICE
# ----------------------------------

def add_calendar_event(
    room_name,
    booking_date,
    start_time,
    end_time
):

    event = {
        "room": room_name,
        "date": str(booking_date),
        "start_time": str(start_time),
        "end_time": str(end_time)
    }

    return event


# ----------------------------------
# EVENT SUMMARY
# ----------------------------------

def get_event_summary(
    room_name,
    booking_date,
    start_time,
    end_time
):

    return (
        f"{room_name} booked on "
        f"{booking_date} from "
        f"{start_time} to "
        f"{end_time}"
    )
    
    