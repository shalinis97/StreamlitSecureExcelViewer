import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access variables
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

# Print the variables to verify they are loaded
print("SMTP_SERVER:", SMTP_SERVER)
print("SMTP_PORT:", SMTP_PORT)
print("EMAIL_ADDRESS:", EMAIL_ADDRESS)
print("EMAIL_PASSWORD:", EMAIL_PASSWORD)
print("DATABASE_URL:", DATABASE_URL)
print("SECRET_KEY:", SECRET_KEY)
