# app.py

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from auth import authenticate_user, register_user
import hashlib

# Load environment variables
load_dotenv()

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

# Function to hash passwords (for additional security if needed)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def main():
    st.title("Secure Excel Viewer")

    menu = ["Home", "Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Welcome to the Secure Excel Viewer")
        if st.session_state.logged_in:
            st.success(f"Logged in as {st.session_state.username}")
            display_excel()
        else:
            st.info("Please login to view the Excel file.")

    elif choice == "Login":
        st.subheader("Login Section")

        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            user = authenticate_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome {username}")
                display_excel()
            else:
                st.error("Invalid Username or Password")

    elif choice == "Register":
        st.subheader("Create New Account")

        new_user = st.text_input("Username")
        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type='password')

        if st.button("Sign Up"):
            success = register_user(new_user, new_email, new_password)
            if success:
                st.success("You have successfully created an account")
                st.info("Go to Login Menu to login")

def display_excel():
    # Path to the Excel file
    excel_file = os.path.join('backend_data', 'data.xlsx')
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
        st.write(df)
    else:
        st.error("Excel file not found.")

if __name__ == '__main__':
    main()
