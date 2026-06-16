import streamlit as st
from database import (
    create_user,
    authenticate_user
)

# ----------------------------------
# LOGIN PAGE
# ----------------------------------

def login_page():

    st.markdown(
        """
        <div style='text-align:center;'>
            <h1>📚 BookWise</h1>
            <h4>Smart Campus Resource Booking System</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Login")

    username = st.text_input(
        "Username",
        key="login_username"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button("Login"):

        if authenticate_user(
            username,
            password
        ):

            st.session_state.logged_in = True
            st.session_state.username = username

            st.success(
                "Login successful!"
            )

            st.rerun()

        else:

            st.error(
                "Invalid username or password."
            )


# ----------------------------------
# REGISTER PAGE
# ----------------------------------

def register_page():

    st.markdown(
        """
        <div style='text-align:center;'>
            <h1>📚 BookWise</h1>
            <h4>Create a New Account</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

    username = st.text_input(
        "Choose Username",
        key="register_username"
    )

    password = st.text_input(
        "Choose Password",
        type="password",
        key="register_password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="confirm_password"
    )

    if st.button("Register"):

        if not username or not password:

            st.warning(
                "Please fill all fields."
            )

        elif password != confirm_password:

            st.error(
                "Passwords do not match."
            )

        else:

            success = create_user(
                username,
                password
            )

            if success:

                st.success(
                    "Account created successfully! Please login."
                )

            else:

                st.error(
                    "Username already exists."
                )


# ----------------------------------
# AUTH PAGE
# ----------------------------------

def auth_page():

    choice = st.radio(
        "Select Option",
        [
            "Login",
            "Register"
        ],
        horizontal=True
    )

    if choice == "Login":

        login_page()

    else:

        register_page()


# ----------------------------------
# LOGOUT
# ----------------------------------

def logout():

    st.session_state.logged_in = False

    if "username" in st.session_state:
        del st.session_state["username"]
        