from flask import Flask
import os
import sys

# Ensure project root path is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.db import init_db
from app.utils.logger import get_logger

logger = get_logger()

# Initialize Database Schema & Seed Data at app load
try:
    init_db()
except Exception as e:
    logger.error(f"Error auto-initializing DB: {e}")

# Create Flask App Instance
app = Flask(__name__)

# Config secret key for sessions
app.secret_key = os.environ.get("SECRET_KEY", "school_system_web_secret_glowing_key_9988")

# Import routes to register them with Flask
from app import routes
