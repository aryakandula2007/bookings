import streamlit as st

from database import (
    create_user,
    authenticate_user
)


def auth_page():

    st.title("🏫 Campus Resource Manager")

    option = st.radio(
        "Select Option",
        [
            "Login",
            "Sign Up"
        ]
    )

    # -------------------------
    # LOGIN
    # -------------------------

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

                st.success(
                    "Login Successful!"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

    # -------------------------
    # SIGN UP
    # -------------------------

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

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("Create Account"):

            if not username:

                st.error(
                    "Username is required"
                )

            elif not email:

                st.error(
                    "Email is required"
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match"
                )

            else:

                success = create_user(
                    username,
                    email,
                    password
                )

                if success:

                    st.success(
                        "Account Created Successfully!"
                    )

                    st.info(
                        "You can now login."
                    )

                else:

                    st.error(
                        "Username or Email already exists."
                    )


def logout():

    st.session_state.logged_in = False

    if "username" in st.session_state:
        del st.session_state["username"]