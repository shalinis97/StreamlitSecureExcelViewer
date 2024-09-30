# database_setup.py

"""
Database Setup Script for StreamlitSecureExcelViewer

This script defines the database models using SQLAlchemy and initializes the SQLite database.
It also creates an initial admin user for managing the application.

Prerequisites:
- Ensure that the .env file is correctly configured with DATABASE_URL and other necessary variables.
- The virtual environment is activated, and all required packages are installed.

Usage:
    python database_setup.py
"""

import os
import sys
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import bcrypt

# ----------------------------
# Step 1: Load Environment Variables
# ----------------------------

# Load environment variables from the .env file
load_dotenv()

# Fetch the DATABASE_URL from environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("Error: DATABASE_URL not found in the .env file.")
    sys.exit(1)  # Exit the script with an error code

# ----------------------------
# Step 2: Define the Database Model
# ----------------------------

Base = declarative_base()

class User(Base):
    """
    User Model

    Represents a user in the application with authentication details.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # Hashed password
    is_admin = Column(Boolean, default=False)
    must_change_password = Column(Boolean, default=True)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', is_admin={self.is_admin})>"

# ----------------------------
# Step 3: Create the Database Engine and Session Factory
# ----------------------------

# Create the SQLAlchemy engine with check_same_thread=False
engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False},
    echo=True  # Enable SQL query logging
)

# Create all tables defined by the Base's subclasses (i.e., User)
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# ----------------------------
# Step 4: Create an Initial Admin User
# ----------------------------

def create_initial_admin():
    """
    Creates an initial admin user if no users exist in the database.
    """
    session = Session()  # Create a new session
    try:
        # Check if any users already exist
        existing_user = session.query(User).first()
        if existing_user:
            print("Admin user already exists. Skipping creation.")
            return

        print("No users found in the database. Creating an initial admin user.")

        # Prompt for admin user details
        print("Please enter details for the initial admin user:")
        username = input("Username: ").strip()
        email = input("Email: ").strip()
        password = input("Password: ").strip()

        if not username or not email or not password:
            print("Error: All fields are required to create an admin user.")
            sys.exit(1)

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create a new User instance
        admin_user = User(
            username=username,
            email=email,
            password=hashed_password.decode('utf-8'),  # Store as string
            is_admin=True,
            must_change_password=True
        )

        # Add the admin user to the session and commit to the database
        session.add(admin_user)
        session.commit()

        print(f"✅ Admin user '{username}' created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        # Close the session
        session.close()

# ----------------------------
# Step 5: Execute the Script
# ----------------------------

if __name__ == "__main__":
    create_initial_admin()
