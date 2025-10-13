import streamlit as st


if not st.user.is_logged_in:
    if st.button("Log in with Google"):
        st.login()
    st.stop()

if st.button("Log out"):
    st.logout()
st.markdown(f"Welcome! {st.user.name}")
st.write(f"Email: {st.user.email}")

st.write("fetquest")


st.write("Welcome to FETQuest OneView")
st.write("App is on construction")
