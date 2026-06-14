import streamlit as st

from database import (
    create_user,
    authenticate_user
)

def auth_page():

    option = st.radio(
        "Choose",
        [
            "Login",
            "Sign Up"
        ]
    )

    if option == "Login":

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            user = authenticate_user(
                username,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.rerun()

            else:

                st.error(
                    "Invalid credentials"
                )

    else:

        username = st.text_input(
            "Choose Username"
        )

        email = st.text_input(
            "Email"
        )

        password = st.text_input(
            "Choose Password",
            type="password"
        )

        if st.button("Create Account"):

            success = create_user(
                username,
                email,
                password
            )

            if success:

                st.success(
                    "Account Created"
                )

            else:

                st.error(
                    "Username already exists"
                )
                