import streamlit as st
from supabase import create_client, Client, AuthApiError

url = st.secrets["db_url"]
key = st.secrets["db_key"]
REDIRECT_URI = st.secrets["auth"]["redirect_uri"]
supabase: Client = create_client(url, key)
st.write(REDIRECT_URI)
if st.button("Login with Google", type="primary"):
    res = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {"redirect_to": REDIRECT_URI}
        })

    auth_url = res.url
    st.markdown(f"[Click here to log in with Google]({auth_url})")
    st.stop()
    
    session = supabase.auth.get_session()
    
    if session and session.user:
        st.session_state.user = session.user
        st.success(f"👋 Welcome {session.user.email}")
    else:
        st.info("Please log in to continue.")





#--------------------------------------#
# import streamlit as st


# # if not st.user.is_logged_in:
# #     if st.button("Log in with Google"):
# #         st.login()
# #     st.stop()

# # if st.button("Log out"):
# #     st.logout()
# # st.markdown(f"Welcome! {st.user.name}")
# # st.write(f"Email: {st.user.email}")

# # st.write("fetquest")


# # st.write("Welcome to FETQuest OneView")
# # st.write("App is on construction")


# import streamlit as st
# from supabase import create_client, Client
# from postgrest.exceptions import APIError

# # --- Setup Supabase ---
# url = st.secrets["db_url"]
# key = st.secrets["db_key"]
# supabase: Client = create_client(url, key)

# # --- Google Login ---
# # if not st.user.is_logged_in:
# #     st.login("google")
# #     st.stop()

# if not st.user.is_logged_in:
#     if st.button("Log in with Google"):
#         st.login()
#     st.stop()

# if st.button("Log out"):
#     st.logout()

# st.markdown(f"### Welcome, {st.user.name} 👋")
# st.write(f"Email: {st.user.email}")

# # Handle login automatically using built-in Google SSO
# # if not st.user.is_logged_in:
# #     st.login("google")   # Streamlit handles the button and OAuth flow
# #     st.stop()

# # if st.button("Log out"):
# #     st.logout()

# # Display user info
# st.markdown(f"### Welcome, {st.user.name} 👋")
# st.write(f"Email: {st.user.email}")

# guser_name = st.user.name
# guser_email = st.user.email

# # Check if user exists in your DB
# try:
#     ret_user = (
#         supabase.table("fet_portfolio_users")
#         .select("user_id", "username")
#         .eq("email", guser_email)
#         .execute()
#     )
# except APIError as e:
#     st.error(f"Database error: {e}")
#     st.stop()

# # Insert new user if not exists
# if not ret_user.data:
#     try:
#         supabase.table("fet_portfolio_users").insert({
#             "username": guser_name,
#             "password_hash": "GOOGLE_SSO",
#             "email": guser_email
#         }).execute()
#         st.info("New Google user added to database.")
#         # Fetch new record
#         ret_user = (
#             supabase.table("fet_portfolio_users")
#             .select("user_id", "username")
#             .eq("email", guser_email)
#             .execute()
#         )
#     except APIError as e:
#         st.error(f"Error inserting user: {e}")
#         st.stop()

# # Store user in session
# if ret_user.data:
#     user_data = ret_user.data[0]
#     st.session_state.logged_in = True
#     st.session_state.u_id = user_data["user_id"]
#     st.session_state.u_name = user_data["username"]
#     st.session_state.user = {
#         "id": user_data["user_id"],
#         "name": user_data["username"],
#         "email": guser_email
#     }

#     st.success(f"Logged in as {user_data['username']}")
#     st.switch_page("pages/portfolio_view.py")
