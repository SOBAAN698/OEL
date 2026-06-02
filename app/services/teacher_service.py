from app.utils.db import get_connection
from app.models.teacher_model import Teacher
from app.utils.logger import get_logger

logger = get_logger()

class TeacherService:
    @staticmethod
    def add_teacher(teacher):
        """
        Adds a teacher record to the database.
        Returns the teacher object with its new ID if successful.
        """
        if not teacher.name or not teacher.name.strip():
            logger.warning("Failed to add teacher: Empty name field.")
            raise ValueError("Teacher name cannot be empty.")
            
        if not teacher.subject or not teacher.subject.strip():
            logger.warning("Failed to add teacher: Empty subject field.")
            raise ValueError("Teacher subject cannot be empty.")
            
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO teachers (name, subject) VALUES (%s, %s)",
                (teacher.name.strip(), teacher.subject.strip())
            )
            conn.commit()
            teacher.id = cursor.lastrowid
            logger.info(f"Teacher added: {teacher}")
            return teacher
        except Exception as e:
            logger.error(f"Error in TeacherService.add_teacher: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_all_teachers():
        """
        Retrieves all teachers from the database.
        Returns a list of Teacher objects.
        """
        conn = None
        cursor = None
        teachers = []
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM teachers ORDER BY id DESC")
            rows = cursor.fetchall()
            for row in rows:
                teachers.append(Teacher(
                    teacher_id=row['id'],
                    name=row['name'],
                    subject=row['subject']
                ))
            return teachers
        except Exception as e:
            logger.error(f"Error in TeacherService.get_all_teachers: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def update_teacher(teacher):
        """
        Updates a teacher's information in the database.
        Returns True if successful.
        """
        if not teacher.id:
            logger.warning("Failed to update teacher: Missing ID.")
            raise ValueError("Teacher ID is required for update.")
            
        if not teacher.name or not teacher.name.strip():
            logger.warning("Failed to update teacher: Empty name field.")
            raise ValueError("Teacher name cannot be empty.")
            
        if not teacher.subject or not teacher.subject.strip():
            logger.warning("Failed to update teacher: Empty subject field.")
            raise ValueError("Teacher subject cannot be empty.")
            
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE teachers SET name = %s, subject = %s WHERE id = %s",
                (teacher.name.strip(), teacher.subject.strip(), teacher.id)
            )
            conn.commit()
            logger.info(f"Teacher updated: {teacher}")
            return True
        except Exception as e:
            logger.error(f"Error in TeacherService.update_teacher: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def delete_teacher(teacher_id):
        """
        Deletes a teacher from the database.
        Returns True if successful.
        """
        if not teacher_id:
            logger.warning("Failed to delete teacher: Missing ID.")
            raise ValueError("Teacher ID is required for deletion.")
            
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM teachers WHERE id = %s", (teacher_id,))
            conn.commit()
            logger.info(f"Teacher with ID {teacher_id} deleted successfully.")
            return True
        except Exception as e:
            logger.error(f"Error in TeacherService.delete_teacher: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_teacher_count():
        """
        Returns the total count of teachers.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM teachers")
            count = cursor.fetchone()[0]
            return count
        except Exception as e:
            logger.error(f"Error in TeacherService.get_teacher_count: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
