from flask import render_template, request, redirect, url_for, session, flash, jsonify
from app import app
from functools import wraps
from datetime import datetime

# Import models & services
from app.models.student_model import Student
from app.models.teacher_model import Teacher
from app.services.auth_service import AuthService
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.services.attendance_service import AttendanceService
from app.services.fee_service import FeeService
from app.utils.logger import get_logger

logger = get_logger()

# Login Required Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# --- AUTHENTICATION ROUTES ---

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
        
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        
        try:
            user = AuthService.authenticate(username, password)
            if user:
                session["user_id"] = user.id
                session["username"] = user.username
                logger.info(f"Web user '{username}' logged in successfully.")
                flash(f"Welcome back, {username.capitalize()}!", "success")
                return redirect(url_for("dashboard"))
            else:
                logger.warning(f"Invalid web login attempt for '{username}'.")
                flash("Invalid username or password.", "error")
        except ValueError as ve:
            flash(str(ve), "warning")
        except Exception as e:
            logger.error(f"Database error during login: {e}")
            flash("Database connection error. Verify that MySQL is running.", "error")
            
    return render_template("login.html")

@app.route("/logout")
def logout():
    username = session.get("username", "User")
    session.clear()
    logger.info(f"Web user '{username}' logged out.")
    flash("You have been successfully logged out.", "info")
    return redirect(url_for("login"))

# --- DASHBOARD & REPORTS ---

@app.route("/")
@login_required
def dashboard():
    try:
        total_students = StudentService.get_student_count()
        total_teachers = TeacherService.get_teacher_count()
        total_fees = FeeService.get_total_fees()
        return render_template(
            "dashboard.html",
            total_students=total_students,
            total_teachers=total_teachers,
            total_fees=total_fees
        )
    except Exception as e:
        logger.error(f"Error loading dashboard: {e}")
        flash("Could not retrieve statistics from database.", "error")
        return render_template("dashboard.html", total_students=0, total_teachers=0, total_fees=0.0)

@app.route("/reports")
@login_required
def reports():
    try:
        # General stats
        total_students = StudentService.get_student_count()
        total_teachers = TeacherService.get_teacher_count()
        total_fees = FeeService.get_total_fees()
        
        # Enrolment distribution
        class_distribution = StudentService.get_class_distribution()
        
        # Attendance rates
        att_summary = AttendanceService.get_attendance_summary()
        pres = att_summary.get("Present", 0)
        absent = att_summary.get("Absent", 0)
        late = att_summary.get("Late", 0)
        
        total_att = pres + absent + late
        present_rate = (pres / total_att * 100) if total_att > 0 else 0.0
        
        # Fee history (last 5 records)
        recent_fees = FeeService.get_fee_records()[:5]
        
        return render_template(
            "reports.html",
            total_students=total_students,
            total_teachers=total_teachers,
            total_fees=total_fees,
            class_distribution=class_distribution,
            att_summary=att_summary,
            present_rate=present_rate,
            recent_fees=recent_fees
        )
    except Exception as e:
        logger.error(f"Error loading reports: {e}")
        flash("Error compiling reports: verify database status.", "error")
        return redirect(url_for("dashboard"))

# --- STUDENT CRUD ROUTES ---

@app.route("/students")
@login_required
def students():
    try:
        student_list = StudentService.get_all_students()
        return render_template("students.html", students=student_list)
    except Exception as e:
        logger.error(f"Error listing students: {e}")
        flash("Failed to fetch students from database.", "error")
        return render_template("students.html", students=[])

@app.route("/students/add", methods=["POST"])
@login_required
def add_student():
    name = request.form.get("name", "")
    s_class = request.form.get("class", "")
    age = request.form.get("age", "")
    
    student = Student(name=name, student_class=s_class, age=age)
    try:
        StudentService.add_student(student)
        flash(f"Student '{name}' added successfully!", "success")
    except ValueError as ve:
        flash(str(ve), "warning")
    except Exception as e:
        logger.error(f"Failed to add student: {e}")
        flash("Database error adding student record.", "error")
        
    return redirect(url_for("students"))

@app.route("/students/update", methods=["POST"])
@login_required
def update_student():
    student_id = request.form.get("student_id")
    name = request.form.get("name", "")
    s_class = request.form.get("class", "")
    age = request.form.get("age", "")
    
    student = Student(student_id=student_id, name=name, student_class=s_class, age=age)
    try:
        StudentService.update_student(student)
        flash(f"Student details updated successfully!", "success")
    except ValueError as ve:
        flash(str(ve), "warning")
    except Exception as e:
        logger.error(f"Failed to update student: {e}")
        flash("Database error updating student record.", "error")
        
    return redirect(url_for("students"))

@app.route("/students/delete/<int:student_id>")
@login_required
def delete_student(student_id):
    try:
        StudentService.delete_student(student_id)
        flash("Student record and related entries deleted successfully.", "success")
    except Exception as e:
        logger.error(f"Failed to delete student: {e}")
        flash("Database error deleting student.", "error")
        
    return redirect(url_for("students"))

# --- TEACHER CRUD ROUTES ---

@app.route("/teachers")
@login_required
def teachers():
    try:
        teacher_list = TeacherService.get_all_teachers()
        return render_template("teachers.html", teachers=teacher_list)
    except Exception as e:
        logger.error(f"Error listing teachers: {e}")
        flash("Failed to fetch teachers from database.", "error")
        return render_template("teachers.html", teachers=[])

@app.route("/teachers/add", methods=["POST"])
@login_required
def add_teacher():
    name = request.form.get("name", "")
    subject = request.form.get("subject", "")
    
    teacher = Teacher(name=name, subject=subject)
    try:
        TeacherService.add_teacher(teacher)
        flash(f"Teacher '{name}' added successfully!", "success")
    except ValueError as ve:
        flash(str(ve), "warning")
    except Exception as e:
        logger.error(f"Failed to add teacher: {e}")
        flash("Database error adding teacher record.", "error")
        
    return redirect(url_for("teachers"))

@app.route("/teachers/update", methods=["POST"])
@login_required
def update_teacher():
    teacher_id = request.form.get("teacher_id")
    name = request.form.get("name", "")
    subject = request.form.get("subject", "")
    
    teacher = Teacher(teacher_id=teacher_id, name=name, subject=subject)
    try:
        TeacherService.update_teacher(teacher)
        flash("Teacher details updated successfully!", "success")
    except ValueError as ve:
        flash(str(ve), "warning")
    except Exception as e:
        logger.error(f"Failed to update teacher: {e}")
        flash("Database error updating teacher record.", "error")
        
    return redirect(url_for("teachers"))

@app.route("/teachers/delete/<int:teacher_id>")
@login_required
def delete_teacher(teacher_id):
    try:
        TeacherService.delete_teacher(teacher_id)
        flash("Teacher profile deleted successfully.", "success")
    except Exception as e:
        logger.error(f"Failed to delete teacher: {e}")
        flash("Database error deleting teacher.", "error")
        
    return redirect(url_for("teachers"))

# --- ATTENDANCE MANAGEMENT ROUTES ---

@app.route("/attendance", methods=["GET", "POST"])
@login_required
def attendance():
    try:
        student_list = StudentService.get_all_students()
        
        if request.method == "POST":
            student_id = request.form.get("student_id")
            date_val = request.form.get("date", "")
            status_val = request.form.get("status")
            
            try:
                AttendanceService.mark_attendance(student_id, date_val, status_val)
                flash("Attendance status recorded successfully!", "success")
            except ValueError as ve:
                flash(str(ve), "warning")
            except Exception as e:
                logger.error(f"Failed to mark attendance: {e}")
                flash("Database error marking attendance.", "error")
                
            return redirect(url_for("attendance"))
            
        # GET Request: retrieve filters
        filter_date = request.args.get("filter_date", "").strip()
        if not filter_date:
            filter_date = None
            
        records = AttendanceService.get_attendance_records(date_str=filter_date)
        today_date = datetime.today().strftime("%Y-%m-%d")
        
        return render_template(
            "attendance.html",
            students=student_list,
            records=records,
            today=today_date,
            filter_date=filter_date
        )
    except Exception as e:
        logger.error(f"Error handling attendance page: {e}")
        flash("Error accessing attendance resources.", "error")
        return redirect(url_for("dashboard"))

# --- FEE MANAGEMENT ROUTES ---

@app.route("/fees", methods=["GET", "POST"])
@login_required
def fees():
    try:
        student_list = StudentService.get_all_students()
        
        if request.method == "POST":
            student_id = request.form.get("student_id")
            amount = request.form.get("amount", "")
            date_val = request.form.get("date", "")
            
            try:
                FeeService.add_fee_record(student_id, amount, date_val)
                flash("Student fee payment logged successfully!", "success")
            except ValueError as ve:
                flash(str(ve), "warning")
            except Exception as e:
                logger.error(f"Failed to record fee: {e}")
                flash("Database error logging fee transaction.", "error")
                
            return redirect(url_for("fees"))
            
        # GET Request: retrieve records
        filter_student_id = request.args.get("filter_student_id", "").strip()
        student_id_val = None
        if filter_student_id:
            try:
                student_id_val = int(filter_student_id)
            except ValueError:
                flash("Filter Student ID must be an integer.", "warning")
                
        records = FeeService.get_fee_records(student_id=student_id_val)
        today_date = datetime.today().strftime("%Y-%m-%d")
        
        return render_template(
            "fees.html",
            students=student_list,
            records=records,
            today=today_date,
            filter_student_id=filter_student_id
        )
    except Exception as e:
        logger.error(f"Error loading fees page: {e}")
        flash("Error loading fee details.", "error")
        return redirect(url_for("dashboard"))
