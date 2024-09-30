import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database_setup import User, Base
import bcrypt
import streamlit as st

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

# Create the engine with check_same_thread=False
engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False}
)
Base.metadata.bind = engine

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

def register_user(username, email, password, is_admin=False):
    session = Session()
    try:
        existing_user = session.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
            st.error("❌ Username or email already exists.")
            return False

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        new_user = User(
            username=username,
            email=email,
            password=hashed_password.decode('utf-8'),
            is_admin=is_admin,
            must_change_password=True
        )

        session.add(new_user)
        session.commit()
        st.success("✅ User registered successfully.")
        return True
    finally:
        session.close()

def authenticate_user(username, password):
    session = Session()
    try:
        user = session.query(User).filter(User.username == username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return user
        else:
            return None
    finally:
        session.close()
