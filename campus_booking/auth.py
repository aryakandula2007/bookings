import streamlit as st

def login():

    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username and password:

            st.session_state.logged_in = True
            st.session_state.username = username

            return True

        else:

            st.error(
                "Enter username and password."
            )

    return False


def logout():

    st.session_state.logged_in = False

    if "username" in st.session_state:
        del st.session_state["username"]


def is_logged_in():

    return st.session_state.get(
        "logged_in",
        False
    )
    