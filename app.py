import os
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User  # Import your SQLAlchemy models (adjust as needed)
import streamlit_authenticator as stauth
import bcrypt

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure the directory for the database exists
db_dir = os.path.join(BASE_DIR, 'data')
os.makedirs(db_dir, exist_ok=True)

# Construct the full path to the database file
db_path = os.path.join(db_dir, 'users.db')

# Update the DATABASE_URL
DATABASE_URL = f"sqlite:///{db_path}"

# Create the database engine
try:
    engine = create_engine(
        DATABASE_URL,
        connect_args={'check_same_thread': False}
    )

    # Create a configured "Session" class
    Session = sessionmaker(bind=engine)

    # Create a Session
    session = Session()

    # Create all tables in the database (if they don't exist)
    Base.metadata.create_all(engine)
except Exception as e:
    st.error(f"Error connecting to the database: {e}")
    st.stop()

# Function to create a default admin user if none exists
def create_default_admin():
    admin_exists = session.query(User).filter_by(username='admin').first()
    if not admin_exists:
        hashed_password = bcrypt.hashpw('admin_password'.encode('utf-8'), bcrypt.gensalt())
        admin_user = User(
            username='admin',
            email='admin@example.com',
            password=hashed_password.decode('utf-8'),
            is_admin=True
        )
        session.add(admin_user)
        session.commit()

create_default_admin()

# Authentication setup
def get_user_credentials():
    users = session.query(User).all()
    usernames = [user.username for user in users]
    names = [user.username.capitalize() for user in users]
    hashed_passwords = [user.password for user in users]
    emails = [user.email for user in users]

    credentials = {
        'usernames': {}
    }

    for username, name, password, email in zip(usernames, names, hashed_passwords, emails):
        credentials['usernames'][username] = {
            'name': name,
            'email': email,
            'password': password
        }

    return credentials

credentials = get_user_credentials()

authenticator = stauth.Authenticate(
    credentials,
    'some_cookie_name',
    'some_signature_key',
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.write(f'Welcome *{name}*')
    st.title('Your Application')

    # Your main application code goes here
    st.write("This is the main content of the app.")

elif authentication_status == False:
    st.error('Username or password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
