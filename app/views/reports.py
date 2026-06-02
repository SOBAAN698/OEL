import tkinter as tk
from tkinter import ttk, messagebox
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.services.fee_service import FeeService
from app.services.attendance_service import AttendanceService
from app.utils import styles
from app.utils.logger import get_logger

logger = get_logger()

class ReportsView:
    def __init__(self, root):
        self.root = root
        
        self.root.title("SMS - Reports Dashboard")
        self.root.geometry("800x600")
        self.root.configure(bg=styles.BG_COLOR)
        
        self.create_widgets()
        self.load_report_data()
        
    def create_widgets(self):
        # Header title
        self.title_label = tk.Label(
            self.root,
            text="School Summary & Reports",
            font=styles.FONT_TITLE,
            bg=styles.BG_COLOR,
            fg=styles.TEXT_COLOR
        )
        self.title_label.pack(pady=20)
        
        # Main container with two columns
        self.main_container = tk.Frame(self.root, bg=styles.BG_COLOR)
        self.main_container.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        # --- LEFT SIDE: STATS CARDS & ATTENDANCE SUMMARY ---
        self.left_frame = tk.Frame(self.main_container, bg=styles.BG_COLOR)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        # Core Stats Card
        self.core_stats_card = tk.Frame(self.left_frame)
        self.core_stats_card.pack(fill="x", pady=(0, 20))
        styles.apply_card_style(self.core_stats_card)
        
        self.core_stats_title = tk.Label(
            self.core_stats_card, text="General Statistics", font=styles.FONT_SUBTITLE, bg=styles.CARD_BG, fg=styles.TEXT_COLOR
        )
        self.core_stats_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        self.lbl_students = tk.Label(self.core_stats_card, text="Total Students Registered: Loading...", font=styles.FONT_BODY, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.lbl_students.pack(anchor="w", padx=20, pady=5)
        
        self.lbl_teachers = tk.Label(self.core_stats_card, text="Total Active Teachers: Loading...", font=styles.FONT_BODY, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.lbl_teachers.pack(anchor="w", padx=20, pady=5)
        
        self.lbl_fees = tk.Label(self.core_stats_card, text="Total Fees Collected: Loading...", font=styles.FONT_BODY, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.lbl_fees.pack(anchor="w", padx=20, pady=(5, 15))
        
        # Attendance Report Card
        self.att_card = tk.Frame(self.left_frame)
        self.att_card.pack(fill="both", expand=True)
        styles.apply_card_style(self.att_card)
        
        self.att_title = tk.Label(self.att_card, text="Attendance Performance", font=styles.FONT_SUBTITLE, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.att_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        self.lbl_present = tk.Label(self.att_card, text="Present: 0", font=styles.FONT_BODY, bg=styles.CARD_BG, fg=styles.SUCCESS_COLOR)
        self.lbl_present.pack(anchor="w", padx=20, pady=4)
        
        self.lbl_absent = tk.Label(self.att_card, text="Absent: 0", font=styles.FONT_BODY, bg=styles.CARD_BG, fg=styles.DANGER_COLOR)
        self.lbl_absent.pack(anchor="w", padx=20, pady=4)
        
        self.lbl_late = tk.Label(self.att_card, text="Late: 0", font=styles.FONT_BODY, bg=styles.CARD_BG, fg="#eab308") # Yellow
        self.lbl_late.pack(anchor="w", padx=20, pady=4)
        
        self.lbl_rate = tk.Label(self.att_card, text="Present Rate: 0.0%", font=styles.FONT_HEADER, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.lbl_rate.pack(anchor="w", padx=20, pady=(10, 15))
        
        # --- RIGHT SIDE: CLASS DISTRIBUTION ---
        self.right_frame = tk.Frame(self.main_container, bg=styles.BG_COLOR)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(15, 0))
        
        self.class_card = tk.Frame(self.right_frame)
        self.class_card.pack(fill="both", expand=True)
        styles.apply_card_style(self.class_card)
        
        self.class_title = tk.Label(self.class_card, text="Class-Wise Enrolment", font=styles.FONT_SUBTITLE, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.class_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        # Scrollable list/table for Class Distribution
        self.scroll_y = ttk.Scrollbar(self.class_card, orient="vertical")
        self.scroll_y.pack(side="right", fill="y")
        
        self.class_table = ttk.Treeview(
            self.class_card,
            columns=("class", "count"),
            show="headings",
            yscrollcommand=self.scroll_y.set
        )
        self.scroll_y.config(command=self.class_table.yview)
        
        self.class_table.heading("class", text="Class Grade")
        self.class_table.heading("count", text="Student Count")
        
        self.class_table.column("class", width=150, anchor="center")
        self.class_table.column("count", width=150, anchor="center")
        
        self.class_table.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Close button at bottom
        self.close_btn = tk.Button(self.root, text="Close Report", command=self.root.destroy)
        self.close_btn.pack(pady=(0, 15))
        styles.apply_button_style(self.close_btn, bg_color=styles.TEXT_MUTED)

    def load_report_data(self):
        """Fetches aggregate data and populates labels and tables."""
        logger.info("Computing metrics for reports...")
        try:
            # 1. Core General Stats
            students_count = StudentService.get_student_count()
            teachers_count = TeacherService.get_teacher_count()
            total_fees = FeeService.get_total_fees()
            
            self.lbl_students.config(text=f"Total Students Registered: {students_count}")
            self.lbl_teachers.config(text=f"Total Active Teachers: {teachers_count}")
            self.lbl_fees.config(text=f"Total Fees Collected: ${total_fees:,.2f}")
            
            # 2. Attendance Summary
            att_summary = AttendanceService.get_attendance_summary()
            pres = att_summary.get("Present", 0)
            absent = att_summary.get("Absent", 0)
            late = att_summary.get("Late", 0)
            
            self.lbl_present.config(text=f"Present: {pres}")
            self.lbl_absent.config(text=f"Absent: {absent}")
            self.lbl_late.config(text=f"Late: {late}")
            
            total_days = pres + absent + late
            rate = 0.0
            if total_days > 0:
                rate = (pres / total_days) * 100
                
            self.lbl_rate.config(text=f"Present Rate: {rate:.1f}%")
            
            # 3. Class enrolment table
            for item in self.class_table.get_children():
                self.class_table.delete(item)
                
            distribution = StudentService.get_class_distribution()
            for item in distribution:
                self.class_table.insert("", "end", values=(item['class'], item['count']))
                
        except Exception as e:
            logger.error(f"Error loading report information: {e}")
            messagebox.showerror("Error", "Could not compile statistical reports.")
