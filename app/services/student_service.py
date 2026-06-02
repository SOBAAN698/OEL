from app.utils.db import get_connection
from app.models.student_model import Student
from app.utils.logger import get_logger

logger = get_logger()

class StudentService:
    @staticmethod
    def add_student(student):
        """
        Adds a student to the database.
        Returns the student object with its new ID if successful.
        """
        if not student.name or not student.name.strip():
            logger.warning("Failed to add student: Empty name field.")
            raise ValueError("Student name cannot be empty.")
            
        if not student.student_class or not student.student_class.strip():
            logger.warning("Failed to add student: Empty class field.")
            raise ValueError("Student class cannot be empty.")
            
        try:
            student.age = int(student.age)
            if student.age <= 0:
                raise ValueError()
        except ValueError:
            logger.warning(f"Failed to add student: Invalid age: {student.age}")
            raise ValueError("Student age must be a positive integer.")
            
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO students (name, class, age) VALUES (%s, %s, %s)",
                (student.name.strip(), student.student_class.strip(), student.age)
            )
            conn.commit()
            student.id = cursor.lastrowid
            logger.info(f"Student added: {student}")
            return student
        except Exception as e:
            logger.error(f"Error in StudentService.add_student: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_all_students():
        """
        Retrieves all students from the database.
        Returns a list of Student objects.
        """
        conn = None
        cursor = None
        students = []
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM students ORDER BY id DESC")
            rows = cursor.fetchall()
            for row in rows:
                students.append(Student(
                    student_id=row['id'],
                    name=row['name'],
                    student_class=row['class'],
                    age=row['age']
                ))
            return students
        except Exception as e:
            logger.error(f"Error in StudentService.get_all_students: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def update_student(student):
        """
        Updates a student's information in the database.
        Returns True if successful.
        """
        if not student.id:
            logger.warning("Failed to update student: Missing ID.")
            raise ValueError("Student ID is required for update.")
            
        if not student.name or not student.name.strip():
            logger.warning("Failed to update student: Empty name field.")
            raise ValueError("Student name cannot be empty.")
            
        if not student.student_class or not student.student_class.strip():
            logger.warning("Failed to update student: Empty class field.")
            raise ValueError("Student class cannot be empty.")
            
        try:
            student.age = int(student.age)
            if student.age <= 0:
                raise ValueError()
        except ValueError:
            logger.warning(f"Failed to update student: Invalid age: {student.age}")
            raise ValueError("Student age must be a positive integer.")
            
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE students SET name = %s, class = %s, age = %s WHERE id = %s",
                (student.name.strip(), student.student_class.strip(), student.age, student.id)
            )
            conn.commit()
            logger.info(f"Student updated: {student}")
            return True
        except Exception as e:
            logger.error(f"Error in StudentService.update_student: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def delete_student(student_id):
        """
        Deletes a student from the database.
        Returns True if successful.
        """
        if not student_id:
            logger.warning("Failed to delete student: Missing ID.")
            raise ValueError("Student ID is required for deletion.")
            
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            conn.commit()
            logger.info(f"Student with ID {student_id} deleted successfully.")
            return True
        except Exception as e:
            logger.error(f"Error in StudentService.delete_student: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_student_count():
        """
        Returns the total count of students.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM students")
            count = cursor.fetchone()[0]
            return count
        except Exception as e:
            logger.error(f"Error in StudentService.get_student_count: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_class_distribution():
        """
        Returns student count grouped by class.
        Returns a list of dicts: [{'class': '10th', 'count': 5}, ...]
        """
        conn = None
        cursor = None
        distribution = []
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT class, COUNT(*) as count FROM students GROUP BY class ORDER BY class")
            distribution = cursor.fetchall()
            return distribution
        except Exception as e:
            logger.error(f"Error in StudentService.get_class_distribution: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

