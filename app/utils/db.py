import mysql.connector
from mysql.connector import Error
import os
from app.utils.logger import get_logger

logger = get_logger()

# Database Connection Parameters
# These are defined exactly as requested by the prompt.
# We also support overriding them via environment variables to facilitate local execution and testing.
host = os.environ.get("DB_HOST", "localhost")
user = os.environ.get("DB_USER", "root")
password = os.environ.get("DB_PASSWORD", "your_password")
database = os.environ.get("DB_NAME", "school_db")

def get_connection(include_db=True):
    """Establishes and returns a connection to the MySQL database."""
    try:
        if include_db:
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
        else:
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
        return conn
    except Error as e:
        logger.error(f"Database connection error: {e}")
        raise e

def init_db():
    """Initializes the database and creates required tables and sample records."""
    logger.info("Initializing database...")
    try:
        # First connect without database context to create database if not exists
        conn = get_connection(include_db=False)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Database '{database}' ready.")

        # Connect to the created database to setup tables
        conn = get_connection(include_db=True)
        cursor = conn.cursor()

        # 1. users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)

        # 2. students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                class VARCHAR(50) NOT NULL,
                age INT NOT NULL
            )
        """)

        # 3. teachers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                subject VARCHAR(100) NOT NULL
            )
        """)

        # 4. attendance table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                date DATE NOT NULL,
                status VARCHAR(20) NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            )
        """)

        # 5. fees table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                date DATE NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            )
        """)

        conn.commit()
        logger.info("All tables verified/created successfully.")

        # Seed Sample Data
        # Check if admin user exists
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            logger.info("Seeding initial admin user...")
            # For simplicity and compliance, seeding admin with plain password "admin123"
            # It's an administrative login system. We can also support SHA256 hashed passwords in production.
            # In auth_service we will support plain/hashed comparison.
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ("admin", "admin123"))
            conn.commit()

        # Check if students exist
        cursor.execute("SELECT COUNT(*) FROM students")
        if cursor.fetchone()[0] == 0:
            logger.info("Seeding sample students...")
            students_data = [
                ("Alice Smith", "10th", 15),
                ("Bob Jones", "11th", 16),
                ("Charlie Brown", "9th", 14)
            ]
            cursor.executemany("INSERT INTO students (name, class, age) VALUES (%s, %s, %s)", students_data)
            conn.commit()

            # Seed sample attendance & fees for existing students
            cursor.execute("SELECT id FROM students")
            student_ids = [row[0] for row in cursor.fetchall()]

            if student_ids:
                logger.info("Seeding attendance records...")
                attendance_data = [
                    (student_ids[0], "2026-06-01", "Present"),
                    (student_ids[1], "2026-06-01", "Absent"),
                    (student_ids[2], "2026-06-01", "Present"),
                    (student_ids[0], "2026-06-02", "Present"),
                    (student_ids[1], "2026-06-02", "Present"),
                ]
                cursor.executemany("INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)", attendance_data)

                logger.info("Seeding fee records...")
                fee_data = [
                    (student_ids[0], 1200.00, "2026-05-10"),
                    (student_ids[1], 1500.00, "2026-05-12"),
                    (student_ids[2], 1000.00, "2026-05-15"),
                ]
                cursor.executemany("INSERT INTO fees (student_id, amount, date) VALUES (%s, %s, %s)", fee_data)
                conn.commit()

        # Check if teachers exist
        cursor.execute("SELECT COUNT(*) FROM teachers")
        if cursor.fetchone()[0] == 0:
            logger.info("Seeding sample teachers...")
            teachers_data = [
                ("Mr. John Miller", "Mathematics"),
                ("Mrs. Sarah Davis", "Science"),
                ("Mr. David Wilson", "English")
            ]
            cursor.executemany("INSERT INTO teachers (name, subject) VALUES (%s, %s)", teachers_data)
            conn.commit()

        cursor.close()
        conn.close()
        logger.info("Database initialization completed successfully.")
        return True
    except Error as e:
        logger.error(f"Database initialization failed: {e}")
        return False
