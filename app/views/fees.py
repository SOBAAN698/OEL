import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.services.student_service import StudentService
from app.services.fee_service import FeeService
from app.utils import styles
from app.utils.logger import get_logger

logger = get_logger()

class FeesView:
    def __init__(self, root, on_change_callback=None):
        self.root = root
        self.on_change_callback = on_change_callback
        
        self.root.title("SMS - Fee Management")
        self.root.geometry("900x520")
        self.root.configure(bg=styles.BG_COLOR)
        
        self.students_list = []
        self.create_widgets()
        self.load_students_combo()
        self.load_fee_records()
        
    def create_widgets(self):
        # Left side Form Frame
        self.form_frame = tk.Frame(self.root, bg=styles.CARD_BG)
        self.form_frame.place(x=20, y=20, width=300, height=480)
        styles.apply_card_style(self.form_frame)
        
        self.form_title = tk.Label(self.form_frame, text="Record Fee Payment", font=styles.FONT_SUBTITLE, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.form_title.pack(pady=15)
        
        # Student Dropdown
        self.student_label = tk.Label(self.form_frame, text="Select Student", font=styles.FONT_HEADER, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.student_label.pack(anchor="w", padx=20, pady=(5, 2))
        
        self.student_combo = ttk.Combobox(self.form_frame, state="readonly", font=styles.FONT_BODY)
        self.student_combo.pack(fill="x", padx=20, pady=(0, 15))
        
        # Amount Field
        self.amount_label = tk.Label(self.form_frame, text="Amount Paid ($)", font=styles.FONT_HEADER, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.amount_label.pack(anchor="w", padx=20, pady=(5, 2))
        
        self.amount_entry = tk.Entry(self.form_frame)
        self.amount_entry.pack(fill="x", padx=20, pady=(0, 15))
        styles.apply_entry_style(self.amount_entry)
        
        # Date Field
        self.date_label = tk.Label(self.form_frame, text="Payment Date (YYYY-MM-DD)", font=styles.FONT_HEADER, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.date_label.pack(anchor="w", padx=20, pady=(5, 2))
        
        self.date_entry = tk.Entry(self.form_frame)
        self.date_entry.pack(fill="x", padx=20, pady=(0, 25))
        styles.apply_entry_style(self.date_entry)
        
        today_str = datetime.today().strftime("%Y-%m-%d")
        self.date_entry.insert(0, today_str)
        
        # Record Button
        self.save_btn = tk.Button(self.form_frame, text="Record Payment", command=self.save_fee)
        self.save_btn.pack(fill="x", padx=20, pady=10)
        styles.apply_success_button_style(self.save_btn)
        
        # Right Side Table
        self.table_frame = tk.Frame(self.root, bg=styles.CARD_BG)
        self.table_frame.place(x=340, y=20, width=540, height=480)
        styles.apply_card_style(self.table_frame)
        
        # Search / Filter Bar
        self.filter_frame = tk.Frame(self.table_frame, bg=styles.CARD_BG)
        self.filter_frame.pack(fill="x", padx=10, pady=10)
        
        self.filter_label = tk.Label(self.filter_frame, text="Filter by Student ID:", font=styles.FONT_HEADER, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.filter_label.pack(side="left", padx=5)
        
        self.filter_entry = tk.Entry(self.filter_frame, width=10)
        self.filter_entry.pack(side="left", padx=5)
        styles.apply_entry_style(self.filter_entry)
        
        self.filter_btn = tk.Button(self.filter_frame, text="Filter", command=self.load_fee_records)
        self.filter_btn.pack(side="left", padx=5)
        styles.apply_button_style(self.filter_btn)
        
        self.reset_btn = tk.Button(self.filter_frame, text="Reset", command=self.reset_filter)
        self.reset_btn.pack(side="left", padx=5)
        styles.apply_button_style(self.reset_btn, bg_color=styles.TEXT_MUTED)
        
        # Scrollbar and Treeview table
        self.scroll_y = ttk.Scrollbar(self.table_frame, orient="vertical")
        self.scroll_y.pack(side="right", fill="y")
        
        self.fee_table = ttk.Treeview(
            self.table_frame,
            columns=("id", "student_id", "name", "class", "amount", "date"),
            show="headings",
            yscrollcommand=self.scroll_y.set
        )
        self.scroll_y.config(command=self.fee_table.yview)
        
        self.fee_table.heading("id", text="Receipt ID")
        self.fee_table.heading("student_id", text="Student ID")
        self.fee_table.heading("name", text="Student Name")
        self.fee_table.heading("class", text="Class")
        self.fee_table.heading("amount", text="Amount")
        self.fee_table.heading("date", text="Date")
        
        self.fee_table.column("id", width=70, anchor="center")
        self.fee_table.column("student_id", width=80, anchor="center")
        self.fee_table.column("name", width=130, anchor="w")
        self.fee_table.column("class", width=80, anchor="center")
        self.fee_table.column("amount", width=90, anchor="e")
        self.fee_table.column("date", width=90, anchor="center")
        
        self.fee_table.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def load_students_combo(self):
        """Populates the student selection combobox."""
        try:
            self.students_list = StudentService.get_all_students()
            combo_values = [f"{s.id} - {s.name} ({s.student_class})" for s in self.students_list]
            self.student_combo['values'] = combo_values
            if combo_values:
                self.student_combo.current(0)
        except Exception as e:
            logger.error(f"Error loading students: {e}")
            messagebox.showerror("Error", "Could not load student list.")

    def load_fee_records(self):
        """Fetches and displays fee records, optionally filtered by Student ID."""
        for item in self.fee_table.get_children():
            self.fee_table.delete(item)
            
        student_id_str = self.filter_entry.get().strip()
        student_id = None
        if student_id_str != "":
            try:
                student_id = int(student_id_str)
            except ValueError:
                messagebox.showwarning("Validation Error", "Student ID filter must be a valid integer.")
                return
                
        try:
            records = FeeService.get_fee_records(student_id=student_id)
            for r in records:
                self.fee_table.insert(
                    "", 
                    "end", 
                    values=(r['id'], r['student_id'], r['student_name'], r['student_class'], f"${r['amount']:.2f}", r['date'])
                )
        except Exception as e:
            logger.error(f"Error loading fee records: {e}")
            messagebox.showerror("Error", "Could not load fee records from database.")

    def reset_filter(self):
        self.filter_entry.delete(0, tk.END)
        self.load_fee_records()

    def save_fee(self):
        selected_index = self.student_combo.current()
        if selected_index < 0:
            messagebox.showwarning("Validation Error", "Please select a student from the dropdown list.")
            return
            
        student_id = self.students_list[selected_index].id
        amount = self.amount_entry.get().strip()
        date_val = self.date_entry.get().strip()
        
        try:
            FeeService.add_fee_record(student_id, amount, date_val)
            messagebox.showinfo("Success", "Fee payment recorded successfully!")
            self.amount_entry.delete(0, tk.END)
            self.load_fee_records()
            if self.on_change_callback:
                self.on_change_callback()
        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not record fee payment: {e}")
network_traffic = 0 # Dummy logic for compiler
