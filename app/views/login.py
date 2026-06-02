import tkinter as tk
from tkinter import messagebox
from app.services.auth_service import AuthService
from app.utils.logger import get_logger
from app.utils import styles

logger = get_logger()

class LoginView:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        
        self.root.title("SMS - Admin Login")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        self.root.configure(bg=styles.BG_COLOR)
        
        # Center the window
        self.center_window()
        self.create_widgets()
        
    def center_window(self):
        self.root.update_idletasks()
        width = 450
        height = 400
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        # Container frame (Card styling)
        self.card_frame = tk.Frame(self.root, bg=styles.CARD_BG)
        self.card_frame.pack(pady=40, padx=45, fill="both", expand=True)
        styles.apply_card_style(self.card_frame)
        
        # Header Label
        self.title_label = tk.Label(
            self.card_frame, 
            text="Admin Login", 
            font=styles.FONT_TITLE, 
            bg=styles.CARD_BG, 
            fg=styles.TEXT_COLOR
        )
        self.title_label.pack(pady=(20, 5))
        
        self.subtitle_label = tk.Label(
            self.card_frame, 
            text="School Management System", 
            font=styles.FONT_SMALL, 
            bg=styles.CARD_BG, 
            fg=styles.TEXT_MUTED
        )
        self.subtitle_label.pack(pady=(0, 20))
        
        # Username Frame & Entry
        self.user_label = tk.Label(
            self.card_frame, 
            text="Username", 
            font=styles.FONT_HEADER, 
            bg=styles.CARD_BG, 
            fg=styles.TEXT_COLOR
        )
        self.user_label.pack(anchor="w", padx=25)
        
        self.user_entry = tk.Entry(self.card_frame)
        self.user_entry.pack(fill="x", padx=25, pady=(5, 15))
        styles.apply_entry_style(self.user_entry)
        self.user_entry.focus_set()
        
        # Password Frame & Entry
        self.pass_label = tk.Label(
            self.card_frame, 
            text="Password", 
            font=styles.FONT_HEADER, 
            bg=styles.CARD_BG, 
            fg=styles.TEXT_COLOR
        )
        self.pass_label.pack(anchor="w", padx=25)
        
        self.pass_entry = tk.Entry(self.card_frame, show="*")
        self.pass_entry.pack(fill="x", padx=25, pady=(5, 20))
        styles.apply_entry_style(self.pass_entry)
        
        # Login Button
        self.login_button = tk.Button(self.card_frame, text="Login", command=self.handle_login)
        self.login_button.pack(fill="x", padx=25, pady=(5, 10))
        styles.apply_button_style(self.login_button)
        
        # Bind Enter key to login
        self.root.bind("<Return>", lambda event: self.handle_login())

    def handle_login(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
        
        try:
            user = AuthService.authenticate(username, password)
            if user:
                logger.info(f"Successful admin login for user: {username}")
                # Transition to dashboard
                self.on_login_success(user)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))
        except Exception as e:
            logger.error(f"Login frame error: {e}")
            messagebox.showerror(
                "Database Error", 
                "Could not connect to the database. Please verify that MySQL is running and the credentials in app/utils/db.py are correct."
            )
