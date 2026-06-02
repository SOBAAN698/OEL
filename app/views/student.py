import tkinter as tk
from tkinter import ttk, messagebox
from app.models.student_model import Student
from app.services.student_service import StudentService
from app.utils import styles
from app.utils.logger import get_logger

logger = get_logger()

class StudentView:
    def __init__(self, root, on_change_callback=None):
        self.root = root
        self.on_change_callback = on_change_callback
        
        self.root.title("SMS - Student Management")
        self.root.geometry("850x500")
        self.root.configure(bg=styles.BG_COLOR)
        
        self.selected_student_id = None
        self.create_widgets()
        self.load_students()
        
    def create_widgets(self):
        # Master Layout (Left Frame: Form, Right Frame: Table)
        # Left Side Form
        self.form_frame = tk.Frame(self.root, bg=styles.CARD_BG)
        self.form_frame.place(x=20, y=20, width=280, height=460)
        styles.apply_card_style(self.form_frame)
        
        self.form_title = tk.Label(self.form_frame, text="Student Details", font=styles.FONT_SUBTITLE, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.form_title.pack(pady=15)
        
        # Name field
        self.name_label = tk.Label(self.form_frame, text="Full Name", font=styles.FONT_HEADER, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.name_label.pack(anchor="w", padx=20, pady=(5, 2))
        self.name_entry = tk.Entry(self.form_frame)
        self.name_entry.pack(fill="x", padx=20, pady=(0, 15))
        styles.apply_entry_style(self.name_entry)
        
        # Class field
        self.class_label = tk.Label(self.form_frame, text="Class (e.g. 10th)", font=styles.FONT_HEADER, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.class_label.pack(anchor="w", padx=20, pady=(5, 2))
        self.class_entry = tk.Entry(self.form_frame)
        self.class_entry.pack(fill="x", padx=20, pady=(0, 15))
        styles.apply_entry_style(self.class_entry)
        
        # Age field
        self.age_label = tk.Label(self.form_frame, text="Age", font=styles.FONT_HEADER, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.age_label.pack(anchor="w", padx=20, pady=(5, 2))
        self.age_entry = tk.Entry(self.form_frame)
        self.age_entry.pack(fill="x", padx=20, pady=(0, 20))
        styles.apply_entry_style(self.age_entry)
        
        # Action Buttons
        self.add_btn = tk.Button(self.form_frame, text="Add Student", command=self.add_student)
        self.add_btn.pack(fill="x", padx=20, pady=5)
        styles.apply_success_button_style(self.add_btn)
        
        self.update_btn = tk.Button(self.form_frame, text="Update Student", command=self.update_student)
        self.update_btn.pack(fill="x", padx=20, pady=5)
        styles.apply_button_style(self.update_btn)
        
        self.delete_btn = tk.Button(self.form_frame, text="Delete Student", command=self.delete_student)
        self.delete_btn.pack(fill="x", padx=20, pady=5)
        styles.apply_danger_button_style(self.delete_btn)
        
        self.clear_btn = tk.Button(self.form_frame, text="Clear Form", command=self.clear_form)
        self.clear_btn.pack(fill="x", padx=20, pady=(5, 10))
        styles.apply_button_style(self.clear_btn, bg_color=styles.TEXT_MUTED)
        
        # Right Side Table
        self.table_frame = tk.Frame(self.root, bg=styles.CARD_BG)
        self.table_frame.place(x=320, y=20, width=510, height=460)
        styles.apply_card_style(self.table_frame)
        
        # Configure Table Scrollbar
        self.scroll_y = ttk.Scrollbar(self.table_frame, orient="vertical")
        self.scroll_y.pack(side="right", fill="y")
        
        # Treeview Styles
        tree_style = ttk.Style()
        tree_style.configure("Treeview.Heading", font=styles.FONT_HEADER)
        tree_style.configure("Treeview", font=styles.FONT_BODY, rowheight=25)
        
        self.student_table = ttk.Treeview(
            self.table_frame,
            columns=("id", "name", "class", "age"),
            show="headings",
            yscrollcommand=self.scroll_y.set
        )
        self.scroll_y.config(command=self.student_table.yview)
        
        self.student_table.heading("id", text="ID")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("class", text="Class")
        self.student_table.heading("age", text="Age")
        
        self.student_table.column("id", width=50, anchor="center")
        self.student_table.column("name", width=200, anchor="w")
        self.student_table.column("class", width=120, anchor="center")
        self.student_table.column("age", width=80, anchor="center")
        
        self.student_table.pack(fill="both", expand=True, padx=10, pady=10)
        self.student_table.bind("<<TreeviewSelect>>", self.on_row_select)

    def load_students(self):
        """Fetches all students and populates the Table."""
        # Clear current rows
        for item in self.student_table.get_children():
            self.student_table.delete(item)
            
        try:
            students = StudentService.get_all_students()
            for s in students:
                self.student_table.insert("", "end", values=(s.id, s.name, s.student_class, s.age))
        except Exception as e:
            logger.error(f"Error loading students: {e}")
            messagebox.showerror("Error", "Could not load students from the database.")

    def on_row_select(self, event):
        """Populates the input entries with the selected student's data."""
        selected = self.student_table.selection()
        if not selected:
            return
            
        row_data = self.student_table.item(selected[0], "values")
        if row_data:
            self.selected_student_id = row_data[0]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, row_data[1])
            self.class_entry.delete(0, tk.END)
            self.class_entry.insert(0, row_data[2])
            self.age_entry.delete(0, tk.END)
            self.age_entry.insert(0, row_data[3])

    def clear_form(self):
        self.selected_student_id = None
        self.name_entry.delete(0, tk.END)
        self.class_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.student_table.selection_remove(self.student_table.selection())

    def add_student(self):
        name = self.name_entry.get()
        s_class = self.class_entry.get()
        age = self.age_entry.get()
        
        student = Student(name=name, student_class=s_class, age=age)
        try:
            StudentService.add_student(student)
            messagebox.showinfo("Success", f"Student '{name}' added successfully!")
            self.clear_form()
            self.load_students()
            if self.on_change_callback:
                self.on_change_callback()
        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not add student: {e}")

    def update_student(self):
        if not self.selected_student_id:
            messagebox.showwarning("Selection Required", "Please select a student from the list to update.")
            return
            
        name = self.name_entry.get()
        s_class = self.class_entry.get()
        age = self.age_entry.get()
        
        student = Student(student_id=self.selected_student_id, name=name, student_class=s_class, age=age)
        try:
            StudentService.update_student(student)
            messagebox.showinfo("Success", "Student records updated successfully!")
            self.clear_form()
            self.load_students()
            if self.on_change_callback:
                self.on_change_callback()
        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not update student: {e}")

    def delete_student(self):
        if not self.selected_student_id:
            messagebox.showwarning("Selection Required", "Please select a student from the list to delete.")
            return
            
        confirm = messagebox.askyesno(
            "Confirm Delete", 
            "Are you sure you want to delete this student? All their attendance and fee records will be lost."
        )
        if confirm:
            try:
                StudentService.delete_student(self.selected_student_id)
                messagebox.showinfo("Success", "Student deleted successfully!")
                self.clear_form()
                self.load_students()
                if self.on_change_callback:
                    self.on_change_callback()
            except Exception as e:
                messagebox.showerror("Database Error", f"Could not delete student: {e}")
