# config.py
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

SECRET_KEY = os.getenv("SECRET_KEY", "your_super_secret_key_here") # Default fallback key
USERS_DB = "users.json"
JWT_EXPIRATION_HOURS = 1 # JWT valid for 1 hour