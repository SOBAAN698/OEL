import tkinter as tk
from tkinter import ttk, messagebox
from app.models.teacher_model import Teacher
from app.services.teacher_service import TeacherService
from app.utils import styles
from app.utils.logger import get_logger

logger = get_logger()

class TeacherView:
    def __init__(self, root, on_change_callback=None):
        self.root = root
        self.on_change_callback = on_change_callback
        
        self.root.title("SMS - Teacher Management")
        self.root.geometry("850x500")
        self.root.configure(bg=styles.BG_COLOR)
        
        self.selected_teacher_id = None
        self.create_widgets()
        self.load_teachers()
        
    def create_widgets(self):
        # Left Side Form
        self.form_frame = tk.Frame(self.root, bg=styles.CARD_BG)
        self.form_frame.place(x=20, y=20, width=280, height=460)
        styles.apply_card_style(self.form_frame)
        
        self.form_title = tk.Label(self.form_frame, text="Teacher Details", font=styles.FONT_SUBTITLE, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.form_title.pack(pady=15)
        
        # Name field
        self.name_label = tk.Label(self.form_frame, text="Full Name", font=styles.FONT_HEADER, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.name_label.pack(anchor="w", padx=20, pady=(5, 2))
        self.name_entry = tk.Entry(self.form_frame)
        self.name_entry.pack(fill="x", padx=20, pady=(0, 15))
        styles.apply_entry_style(self.name_entry)
        
        # Subject field
        self.sub_label = tk.Label(self.form_frame, text="Subject Specialist", font=styles.FONT_HEADER, bg=styles.CARD_BG, fg=styles.TEXT_COLOR)
        self.sub_label.pack(anchor="w", padx=20, pady=(5, 2))
        self.sub_entry = tk.Entry(self.form_frame)
        self.sub_entry.pack(fill="x", padx=20, pady=(0, 20))
        styles.apply_entry_style(self.sub_entry)
        
        # Action Buttons
        self.add_btn = tk.Button(self.form_frame, text="Add Teacher", command=self.add_teacher)
        self.add_btn.pack(fill="x", padx=20, pady=5)
        styles.apply_success_button_style(self.add_btn)
        
        self.update_btn = tk.Button(self.form_frame, text="Update Details", command=self.update_teacher)
        self.update_btn.pack(fill="x", padx=20, pady=5)
        styles.apply_button_style(self.update_btn)
        
        self.delete_btn = tk.Button(self.form_frame, text="Delete Teacher", command=self.delete_teacher)
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
        
        # Treeview styles
        self.teacher_table = ttk.Treeview(
            self.table_frame,
            columns=("id", "name", "subject"),
            show="headings",
            yscrollcommand=self.scroll_y.set
        )
        self.scroll_y.config(command=self.teacher_table.yview)
        
        self.teacher_table.heading("id", text="ID")
        self.teacher_table.heading("name", text="Name")
        self.teacher_table.heading("subject", text="Subject")
        
        self.teacher_table.column("id", width=60, anchor="center")
        self.teacher_table.column("name", width=240, anchor="w")
        self.teacher_table.column("subject", width=180, anchor="w")
        
        self.teacher_table.pack(fill="both", expand=True, padx=10, pady=10)
        self.teacher_table.bind("<<TreeviewSelect>>", self.on_row_select)

    def load_teachers(self):
        """Fetches all teachers and populates the Table."""
        # Clear current rows
        for item in self.teacher_table.get_children():
            self.teacher_table.delete(item)
            
        try:
            teachers = TeacherService.get_all_teachers()
            for t in teachers:
                self.teacher_table.insert("", "end", values=(t.id, t.name, t.subject))
        except Exception as e:
            logger.error(f"Error loading teachers: {e}")
            messagebox.showerror("Error", "Could not load teachers from database.")

    def on_row_select(self, event):
        """Populates the input entries with the selected teacher's data."""
        selected = self.teacher_table.selection()
        if not selected:
            return
            
        row_data = self.teacher_table.item(selected[0], "values")
        if row_data:
            self.selected_teacher_id = row_data[0]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, row_data[1])
            self.sub_entry.delete(0, tk.END)
            self.sub_entry.insert(0, row_data[2])

    def clear_form(self):
        self.selected_teacher_id = None
        self.name_entry.delete(0, tk.END)
        self.sub_entry.delete(0, tk.END)
        self.teacher_table.selection_remove(self.teacher_table.selection())

    def add_teacher(self):
        name = self.name_entry.get()
        subject = self.sub_entry.get()
        
        teacher = Teacher(name=name, subject=subject)
        try:
            TeacherService.add_teacher(teacher)
            messagebox.showinfo("Success", f"Teacher '{name}' added successfully!")
            self.clear_form()
            self.load_teachers()
            if self.on_change_callback:
                self.on_change_callback()
        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not add teacher: {e}")

    def update_teacher(self):
        if not self.selected_teacher_id:
            messagebox.showwarning("Selection Required", "Please select a teacher from the list to update.")
            return
            
        name = self.name_entry.get()
        subject = self.sub_entry.get()
        
        teacher = Teacher(teacher_id=self.selected_teacher_id, name=name, subject=subject)
        try:
            TeacherService.update_teacher(teacher)
            messagebox.showinfo("Success", "Teacher records updated successfully!")
            self.clear_form()
            self.load_teachers()
            if self.on_change_callback:
                self.on_change_callback()
        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not update teacher: {e}")

    def delete_teacher(self):
        if not self.selected_teacher_id:
            messagebox.showwarning("Selection Required", "Please select a teacher from the list to delete.")
            return
            
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this teacher record?")
        if confirm:
            try:
                TeacherService.delete_teacher(self.selected_teacher_id)
                messagebox.showinfo("Success", "Teacher deleted successfully!")
                self.clear_form()
                self.load_teachers()
                if self.on_change_callback:
                    self.on_change_callback()
            except Exception as e:
                messagebox.showerror("Database Error", f"Could not delete teacher: {e}")
