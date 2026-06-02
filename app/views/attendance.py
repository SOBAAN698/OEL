import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.services.student_service import StudentService
from app.services.attendance_service import AttendanceService
from app.utils import styles
from app.utils.logger import get_logger

logger = get_logger()

class AttendanceView:
    def __init__(self, root):
        self.root = root
        
        self.root.title("SMS - Attendance Management")
        self.root.geometry("900x520")
        self.root.configure(bg=styles.BG_COLOR)
        
        self.students_list = []
        self.create_widgets()
        self.load_students_combo()
        self.load_attendance_records()
        
    def create_widgets(self):
        # Left side Form
        self.form_frame = tk.Frame(self.root, bg=styles.CARD_BG)
        self.form_frame.place(x=20, y=20, width=300, height=480)
        styles.apply_card_style(self.form_frame)
        
        self.form_title = tk.Label(self.form_frame, text="Mark Attendance", font=styles.FONT_SUBTITLE, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.form_title.pack(pady=15)
        
        # Student dropdown selection
        self.student_label = tk.Label(self.form_frame, text="Select Student", font=styles.FONT_HEADER, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.student_label.pack(anchor="w", padx=20, pady=(5, 2))
        
        self.student_combo = ttk.Combobox(self.form_frame, state="readonly", font=styles.FONT_BODY)
        self.student_combo.pack(fill="x", padx=20, pady=(0, 15))
        
        # Date field (default to today)
        self.date_label = tk.Label(self.form_frame, text="Date (YYYY-MM-DD)", font=styles.FONT_HEADER, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.date_label.pack(anchor="w", padx=20, pady=(5, 2))
        self.date_entry = tk.Entry(self.form_frame)
        self.date_entry.pack(fill="x", padx=20, pady=(0, 15))
        styles.apply_entry_style(self.date_entry)
        
        # Prepopulate with today's date
        today_str = datetime.today().strftime("%Y-%m-%d")
        self.date_entry.insert(0, today_str)
        
        # Status field
        self.status_label = tk.Label(self.form_frame, text="Attendance Status", font=styles.FONT_HEADER, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.status_label.pack(anchor="w", padx=20, pady=(5, 2))
        
        self.status_combo = ttk.Combobox(self.form_frame, values=["Present", "Absent", "Late"], state="readonly", font=styles.FONT_BODY)
        self.status_combo.pack(fill="x", padx=20, pady=(0, 25))
        self.status_combo.set("Present")
        
        # Action button
        self.save_btn = tk.Button(self.form_frame, text="Save Record", command=self.save_attendance)
        self.save_btn.pack(fill="x", padx=20, pady=10)
        styles.apply_success_button_style(self.save_btn)
        
        # Right side Table and filter
        self.table_frame = tk.Frame(self.root, bg=styles.CARD_BG)
        self.table_frame.place(x=340, y=20, width=540, height=480)
        styles.apply_card_style(self.table_frame)
        
        # Search / Filter Bar
        self.filter_frame = tk.Frame(self.table_frame, bg=styles.CARD_BG)
        self.filter_frame.pack(fill="x", padx=10, pady=10)
        
        self.filter_label = tk.Label(self.filter_frame, text="Filter by Date (YYYY-MM-DD):", font=styles.FONT_HEADER, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.filter_label.pack(side="left", padx=5)
        
        self.filter_entry = tk.Entry(self.filter_frame, width=15)
        self.filter_entry.pack(side="left", padx=5)
        styles.apply_entry_style(self.filter_entry)
        
        self.filter_btn = tk.Button(self.filter_frame, text="Search", command=self.load_attendance_records)
        self.filter_btn.pack(side="left", padx=5)
        styles.apply_button_style(self.filter_btn)
        
        self.clear_filter_btn = tk.Button(self.filter_frame, text="Reset", command=self.reset_filter)
        self.clear_filter_btn.pack(side="left", padx=5)
        styles.apply_button_style(self.clear_filter_btn, bg_color=styles.TEXT_MUTED)
        
        # Configure Table Scrollbar
        self.scroll_y = ttk.Scrollbar(self.table_frame, orient="vertical")
        self.scroll_y.pack(side="right", fill="y")
        
        # Treeview table
        self.attendance_table = ttk.Treeview(
            self.table_frame,
            columns=("id", "student_id", "name", "class", "date", "status"),
            show="headings",
            yscrollcommand=self.scroll_y.set
        )
        self.scroll_y.config(command=self.attendance_table.yview)
        
        self.attendance_table.heading("id", text="Log ID")
        self.attendance_table.heading("student_id", text="Student ID")
        self.attendance_table.heading("name", text="Student Name")
        self.attendance_table.heading("class", text="Class")
        self.attendance_table.heading("date", text="Date")
        self.attendance_table.heading("status", text="Status")
        
        self.attendance_table.column("id", width=60, anchor="center")
        self.attendance_table.column("student_id", width=80, anchor="center")
        self.attendance_table.column("name", width=140, anchor="w")
        self.attendance_table.column("class", width=80, anchor="center")
        self.attendance_table.column("date", width=90, anchor="center")
        self.attendance_table.column("status", width=80, anchor="center")
        
        self.attendance_table.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def load_students_combo(self):
        """Populates the student selection dropdown."""
        try:
            self.students_list = StudentService.get_all_students()
            combo_values = [f"{s.id} - {s.name} ({s.student_class})" for s in self.students_list]
            self.student_combo['values'] = combo_values
            if combo_values:
                self.student_combo.current(0)
        except Exception as e:
            logger.error(f"Error loading students for dropdown: {e}")
            messagebox.showerror("Error", "Could not load students for combobox selection.")

    def load_attendance_records(self):
        """Fetches and displays attendance logs. Can filter by date input."""
        # Clear current rows
        for item in self.attendance_table.get_children():
            self.attendance_table.delete(item)
            
        filter_date = self.filter_entry.get().strip()
        if filter_date == "":
            filter_date = None
            
        try:
            records = AttendanceService.get_attendance_records(date_str=filter_date)
            for r in records:
                self.attendance_table.insert(
                    "", 
                    "end", 
                    values=(r['id'], r['student_id'], r['student_name'], r['student_class'], r['date'], r['status'])
                )
        except Exception as e:
            logger.error(f"Error loading attendance logs: {e}")
            messagebox.showerror("Error", "Could not load attendance logs.")

    def reset_filter(self):
        self.filter_entry.delete(0, tk.END)
        self.load_attendance_records()

    def save_attendance(self):
        selected_index = self.student_combo.current()
        if selected_index < 0:
            messagebox.showwarning("Validation Error", "Please select a student from the dropdown list.")
            return
            
        student_id = self.students_list[selected_index].id
        date_val = self.date_entry.get().strip()
        status_val = self.status_combo.get()
        
        try:
            AttendanceService.mark_attendance(student_id, date_val, status_val)
            messagebox.showinfo("Success", "Attendance record marked successfully!")
            self.load_attendance_records()
        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not save attendance log: {e}")
