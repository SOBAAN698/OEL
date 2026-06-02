from app.utils.db import get_connection
from app.utils.logger import get_logger
from datetime import datetime

logger = get_logger()

class AttendanceService:
    @staticmethod
    def mark_attendance(student_id, date_str, status):
        """
        Marks attendance for a student.
        If an attendance record already exists for the student on that date, updates it.
        Otherwise, inserts a new record.
        """
        if not student_id:
            raise ValueError("Student ID is required.")
        if not date_str:
            raise ValueError("Date is required.")
        if status not in ["Present", "Absent", "Late"]:
            raise ValueError("Status must be Present, Absent, or Late.")

        # Validate date format (YYYY-MM-DD)
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Check if student exists
            cursor.execute("SELECT id FROM students WHERE id = %s", (student_id,))
            if not cursor.fetchone():
                raise ValueError("Student does not exist.")

            # Check if record already exists
            cursor.execute(
                "SELECT id FROM attendance WHERE student_id = %s AND date = %s",
                (student_id, parsed_date)
            )
            existing = cursor.fetchone()

            if existing:
                # Update existing record
                cursor.execute(
                    "UPDATE attendance SET status = %s WHERE id = %s",
                    (status, existing[0])
                )
                logger.info(f"Updated attendance ID {existing[0]} for student {student_id} to {status} on {date_str}.")
            else:
                # Insert new record
                cursor.execute(
                    "INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)",
                    (student_id, parsed_date, status)
                )
                logger.info(f"Marked attendance for student {student_id} as {status} on {date_str}.")

            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error in AttendanceService.mark_attendance: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_attendance_records(date_str=None, student_id=None):
        """
        Retrieves attendance records. Can filter by date or student_id.
        Returns detailed list with student names.
        """
        conn = None
        cursor = None
        records = []
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT a.id, a.student_id, s.name as student_name, s.class as student_class, a.date, a.status 
                FROM attendance a
                JOIN students s ON a.student_id = s.id
            """
            params = []
            conditions = []
            
            if date_str:
                conditions.append("a.date = %s")
                params.append(date_str)
            if student_id:
                conditions.append("a.student_id = %s")
                params.append(student_id)
                
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
                
            query += " ORDER BY a.date DESC, s.name ASC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # Format dates to string
            for row in rows:
                if isinstance(row['date'], datetime) or hasattr(row['date'], 'strftime'):
                    row['date'] = row['date'].strftime("%Y-%m-%d")
                records.append(row)
                
            return records
        except Exception as e:
            logger.error(f"Error in AttendanceService.get_attendance_records: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_attendance_summary():
        """
        Returns attendance status counts.
        Returns a dict: {'Present': X, 'Absent': Y, 'Late': Z}
        """
        conn = None
        cursor = None
        summary = {"Present": 0, "Absent": 0, "Late": 0}
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT status, COUNT(*) FROM attendance GROUP BY status")
            rows = cursor.fetchall()
            for row in rows:
                status, count = row
                if status in summary:
                    summary[status] = count
            return summary
        except Exception as e:
            logger.error(f"Error in AttendanceService.get_attendance_summary: {e}")
            return summary
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

