import tkinter as tk
import sys
import os

# Add project root directory to python path to resolve imports properly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.db import init_db
from app.views.login import LoginView
from app.views.dashboard import DashboardView
from app.utils.logger import get_logger

logger = get_logger()

def main():
    logger.info("Starting School Management System...")
    
    # Initialize the database schema & seed data
    # If connection fails, the user will be alerted via the UI, but we still run the GUI.
    db_initialized = False
    try:
        db_initialized = init_db()
    except Exception as e:
        logger.error(f"Failed to auto-initialize DB: {e}")

    root = tk.Tk()
    
    def on_login_success(user):
        # Destroy current login view and open the dashboard
        root.destroy()
        
        # Start dashboard in a new tk.Tk() window
        dashboard_root = tk.Tk()
        app = DashboardView(dashboard_root, user)
        dashboard_root.mainloop()

    # Instantiate login view on root window
    login_app = LoginView(root, on_login_success)
    root.mainloop()

if __name__ == "__main__":
    main()
