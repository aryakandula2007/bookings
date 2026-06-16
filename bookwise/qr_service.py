booking_id = create_booking(
    room_id,
    user,
    email,
    booking_date,
    start_time,
    end_time
)

qr_path = generate_booking_qr(
    booking_id,
    room_name,
    booking_date,
    start_time,
    end_time
)

st.success(
    f"Booking Successful! ID: {booking_id}"
)

st.image(
    qr_path,
    caption="Booking QR Code"
)
