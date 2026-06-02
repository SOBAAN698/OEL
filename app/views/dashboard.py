import tkinter as tk
from tkinter import messagebox
from app.utils import styles
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.services.fee_service import FeeService
from app.utils.logger import get_logger

# Import other view windows
from app.views.student import StudentView
from app.views.teacher import TeacherView
from app.views.attendance import AttendanceView
from app.views.fees import FeesView
from app.views.reports import ReportsView

logger = get_logger()

class DashboardView:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        
        self.root.title("SMS - Dashboard")
        self.root.geometry("800x550")
        self.root.configure(bg=styles.BG_COLOR)
        
        self.center_window()
        self.create_widgets()
        self.refresh_statistics()
        
    def center_window(self):
        self.root.update_idletasks()
        width = 800
        height = 550
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        # --- TOP HEADER BAR ---
        self.header_frame = tk.Frame(self.root, bg=styles.PRIMARY_COLOR, height=70)
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)
        
        self.header_title = tk.Label(
            self.header_frame, 
            text="School Management System", 
            font=styles.FONT_TITLE, 
            fg="#ffffff", 
            bg=styles.PRIMARY_COLOR
        )
        self.header_title.pack(side="left", padx=20, pady=15)
        
        self.user_label = tk.Label(
            self.header_frame, 
            text=f"Welcome, {self.user.username.capitalize()}", 
            font=styles.FONT_HEADER, 
            fg="#e2e8f0", 
            bg=styles.PRIMARY_COLOR
        )
        self.user_label.pack(side="right", padx=20, pady=20)
        
        # --- MAIN BODY FRAME ---
        self.body_frame = tk.Frame(self.root, bg=styles.BG_COLOR)
        self.body_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # --- STATISTICS SECTION ---
        self.stats_title = tk.Label(
            self.body_frame,
            text="System Overview",
            font=styles.FONT_SUBTITLE,
            bg=styles.BG_COLOR,
            fg=styles.TEXT_COLOR
        )
        self.stats_title.pack(anchor="w", pady=(0, 10))
        
        # Stats Cards Container (Frame)
        self.cards_frame = tk.Frame(self.body_frame, bg=styles.BG_COLOR)
        self.cards_frame.pack(fill="x", pady=10)
        self.cards_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")
        
        # Card 1: Total Students
        self.student_card = tk.Frame(self.cards_frame)
        self.student_card.grid(row=0, column=0, padx=10, sticky="nsew")
        styles.apply_card_style(self.student_card)
        
        self.student_label = tk.Label(self.student_card, text="TOTAL STUDENTS", font=styles.FONT_SMALL, fg=styles.TEXT_MUTED, bg=styles.CARD_BG)
        self.student_label.pack(pady=(15, 5))
        self.student_val = tk.Label(self.student_card, text="0", font=styles.FONT_TITLE, fg=styles.PRIMARY_COLOR, bg=styles.CARD_BG)
        self.student_val.pack(pady=(0, 15))
        
        # Card 2: Total Teachers
        self.teacher_card = tk.Frame(self.cards_frame)
        self.teacher_card.grid(row=0, column=1, padx=10, sticky="nsew")
        styles.apply_card_style(self.teacher_card)
        
        self.teacher_label = tk.Label(self.teacher_card, text="TOTAL TEACHERS", font=styles.FONT_SMALL, fg=styles.TEXT_MUTED, bg=styles.CARD_BG)
        self.teacher_label.pack(pady=(15, 5))
        self.teacher_val = tk.Label(self.teacher_card, text="0", font=styles.FONT_TITLE, fg=styles.SECONDARY_COLOR, bg=styles.CARD_BG)
        self.teacher_val.pack(pady=(0, 15))
        
        # Card 3: Fees Collected
        self.fees_card = tk.Frame(self.cards_frame)
        self.fees_card.grid(row=0, column=2, padx=10, sticky="nsew")
        styles.apply_card_style(self.fees_card)
        
        self.fees_label = tk.Label(self.fees_card, text="FEES COLLECTED", font=styles.FONT_SMALL, fg=styles.TEXT_MUTED, bg=styles.CARD_BG)
        self.fees_label.pack(pady=(15, 5))
        self.fees_val = tk.Label(self.fees_card, text="$0.00", font=styles.FONT_TITLE, fg=styles.SUCCESS_COLOR, bg=styles.CARD_BG)
        self.fees_val.pack(pady=(0, 15))
        
        # --- QUICK ACTIONS SECTION ---
        self.actions_title = tk.Label(
            self.body_frame,
            text="Quick Navigation",
            font=styles.FONT_SUBTITLE,
            bg=styles.BG_COLOR,
            fg=styles.TEXT_COLOR
        )
        self.actions_title.pack(anchor="w", pady=(20, 10))
        
        self.actions_frame = tk.Frame(self.body_frame, bg=styles.BG_COLOR)
        self.actions_frame.pack(fill="x", pady=5)
        self.actions_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="equal")
        
        # Define module actions and buttons
        modules = [
            ("Students", self.open_students, styles.PRIMARY_COLOR),
            ("Teachers", self.open_teachers, styles.SECONDARY_COLOR),
            ("Attendance", self.open_attendance, "#0ea5e9"), # Cyan-blue
            ("Fees", self.open_fees, styles.SUCCESS_COLOR),
            ("Reports", self.open_reports, "#f59e0b")      # Amber
        ]
        
        for idx, (name, cmd, col) in enumerate(modules):
            btn = tk.Button(self.actions_frame, text=name, command=cmd)
            btn.grid(row=0, column=idx, padx=5, ipady=12, sticky="ew")
            styles.apply_button_style(btn, bg_color=col)
            
        # Refresh Button
        self.refresh_btn = tk.Button(self.body_frame, text="Refresh Stats", command=self.refresh_statistics)
        self.refresh_btn.pack(pady=20)
        styles.apply_button_style(self.refresh_btn, bg_color=styles.TEXT_MUTED)

    def refresh_statistics(self):
        """Fetches up-to-date summary figures from services and updates labels."""
        logger.info("Refreshing dashboard stats...")
        try:
            total_students = StudentService.get_student_count()
            total_teachers = TeacherService.get_teacher_count()
            total_fees = FeeService.get_total_fees()
            
            self.student_val.config(text=str(total_students))
            self.teacher_val.config(text=str(total_teachers))
            self.fees_val.config(text=f"${total_fees:,.2f}")
        except Exception as e:
            logger.error(f"Error updating dashboard statistics: {e}")
            messagebox.showerror("Stats Error", "Could not fetch updated statistics from database.")

    # Window Management for separate modules
    def open_students(self):
        logger.info("Opening Student Management window")
        student_win = tk.Toplevel(self.root)
        StudentView(student_win, self.refresh_statistics)

    def open_teachers(self):
        logger.info("Opening Teacher Management window")
        teacher_win = tk.Toplevel(self.root)
        TeacherView(teacher_win, self.refresh_statistics)

    def open_attendance(self):
        logger.info("Opening Attendance window")
        attendance_win = tk.Toplevel(self.root)
        AttendanceView(attendance_win)

    def open_fees(self):
        logger.info("Opening Fee Management window")
        fee_win = tk.Toplevel(self.root)
        FeesView(fee_win, self.refresh_statistics)

    def open_reports(self):
        logger.info("Opening Reports window")
        reports_win = tk.Toplevel(self.root)
        ReportsView(reports_win)
