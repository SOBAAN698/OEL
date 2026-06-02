# School Management System

A complete, professional desktop application built with Python (Tkinter) and MySQL to manage school records, track student and teacher profiles, mark daily attendance, log fee payments, and view real-time graphical statistical reports.

---

## Features

1. **Secure Admin Login System**
   - Username/Password authentication for system administrators.
   - Comprehensive error checking and logging of login activities.

2. **Student Profile Management (CRUD)**
   - Add new students with auto-increment IDs.
   - View list of enrolled students in a styled table (Treeview).
   - Update student records (Name, Class, Age).
   - Delete students (with automatic cascade deletion of corresponding attendance and fee logs).

3. **Teacher Profile Management (CRUD)**
   - Add teachers with specialized subjects.
   - View, update, or remove teacher details.

4. **Daily Attendance Tracking**
   - Mark students as *Present*, *Absent*, or *Late* for any date.
   - Look up historical attendance records by date.

5. **Student Fee Payments Logging**
   - Record student payment amounts and dates.
   - Browse financial histories filtered by specific Student ID.

6. **Interactive Summary Dashboard & Reports**
   - Displays real-time aggregate statistics (Total Students, Total Teachers, Total Fees Collected).
   - Presents detailed metrics, attendance percentage ratios, and student counts grouped by grade.

---

## Technologies Used

- **Programming Language**: Python 3.x
- **GUI Framework**: Tkinter (built-in)
- **Database Engine**: MySQL
- **Database Connector**: `mysql-connector-python`
- **Testing Framework**: `pytest`
- **Logging**: Python `logging` library

---

## Project Structure

The project strictly adheres to a layered MVC/Service architecture:

```text
project/
│── app/
│   │── __init__.py
│   │── main.py
│   │── views/
│   │   │── login.py
│   │   │── dashboard.py
│   │   │── student.py
│   │   │── teacher.py
│   │   │── attendance.py
│   │   │── fees.py
│   │   │── reports.py
│   │── models/
│   │   │── student_model.py
│   │   │── teacher_model.py
│   │   │── user_model.py
│   │── services/
│   │   │── auth_service.py
│   │   │── student_service.py
│   │   │── teacher_service.py
│   │   │── attendance_service.py
│   │   │── fee_service.py
│   │── utils/
│   │   │── db.py
│   │   │── styles.py
│   │   │── logger.py
│── tests/
│   │── test_auth.py
│   │── test_student.py
│── requirements.txt
│── README.md
```

---

## Database Setup Instructions

1. Make sure you have a local **MySQL Server** installed and running on your machine.
2. Open `app/utils/db.py` and adjust the connection parameters to match your MySQL server credentials:
   - `host = "localhost"`
   - `user = "root"`
   - `password = "your_password"`
3. The application will **automatically create** the database named `school_db` and all of the required tables (`users`, `students`, `teachers`, `attendance`, `fees`) the first time it is run!
4. The database initialization script also seeds default dummy test records and the initial administrator account:
   - **Default Admin Username**: `admin`
   - **Default Admin Password**: `admin123`

---

## Installation & How to Run Project

### 1. Install Dependencies
Ensure you have Python installed, then run the following command in the project root directory:
```bash
pip install -r requirements.txt
```

### 2. Launch the Application
Run the main startup entry point script:
```bash
python app/main.py
```

### 3. Run Automated Tests
Execute the unit test suites using `pytest`:
```bash
python -m pytest
```

---

## Git & Collaboration

- Repository initialized locally.
- Development branch strategy executed:
  - `feature-login`: Core shell and auth mechanisms.
  - `feature-student`: Student data structures and screens.
  - `feature-teacher`: Teacher management.
  - All branches successfully merged back into `main`.

### GitHub Collaborators
- **shah7008**
