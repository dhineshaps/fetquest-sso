import streamlit as st


# if not st.user.is_logged_in:
#     if st.button("Log in with Google"):
#         st.login()
#     st.stop()

# if st.button("Log out"):
#     st.logout()
# st.markdown(f"Welcome! {st.user.name}")
# st.write(f"Email: {st.user.email}")

# st.write("fetquest")


# st.write("Welcome to FETQuest OneView")
# st.write("App is on construction")


import streamlit as st
from supabase import create_client, Client
from postgrest.exceptions import APIError

# --- Setup Supabase ---
url = st.secrets["db_url"]
key = st.secrets["db_key"]
supabase: Client = create_client(url, key)

# --- Google Login ---
if not st.user.is_logged_in:
    st.login("google")
    st.stop()

if st.button("Log out"):
    st.logout()

st.markdown(f"### Welcome, {st.user.name} 👋")
st.write(f"Email: {st.user.email}")

guser_name = st.user.name
guser_email = st.user.email

# --- Check if user exists ---
try:
    ret_user = (
        supabase.table("fet_portfolio_users")
        .select("email")
        .eq("email", guser_email)
        .execute()
    )
except APIError as e:
    st.error(f"Database error: {e}")
    st.stop()

# --- Insert new user if not exists ---
if not ret_user.data:
    try:
        supabase.table("fet_portfolio_users").insert(
            {
                "username": guser_name,
                "password_hash": None,
                "email": guser_email
            }
        ).execute()
        st.info("New Google user added to database.")
    except APIError as e:
        msg = e.message.split(" ")[-1].split("_")[-2].upper() if "already" in e.message else e.message
        st.error(f"{msg} already exists, try to login with it.")
        st.stop()

# --- Fetch user info ---
try:
    user_id = (
        supabase.table("fet_portfolio_users")
        .select("user_id", "username")
        .eq("email", guser_email)
        .execute()
    )
except APIError as e:
    st.error("Error in fetching user data, please retry later.")
    st.stop()

if user_id.data:
    u_id = user_id.data[0]['user_id']
    u_name = user_id.data[0]['username']

    st.session_state.logged_in = True
    st.session_state.u_id = u_id
    st.session_state.u_name = u_name
    st.session_state.user = {"id": u_id, "name": u_name, "email": guser_email}

    st.write(f"User ID: {u_id}")
    st.write(f"Username: {u_name}")

    st.switch_page("pages/portfolio_view.py")
