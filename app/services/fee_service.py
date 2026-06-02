from app.utils.db import get_connection
from app.utils.logger import get_logger
from datetime import datetime

logger = get_logger()

class FeeService:
    @staticmethod
    def add_fee_record(student_id, amount, date_str):
        """
        Adds a fee payment record for a student.
        """
        if not student_id:
            raise ValueError("Student ID is required.")
        if not date_str:
            raise ValueError("Date is required.")
            
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError()
        except ValueError:
            raise ValueError("Fee amount must be a positive number.")

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

            cursor.execute(
                "INSERT INTO fees (student_id, amount, date) VALUES (%s, %s, %s)",
                (student_id, amount, parsed_date)
            )
            conn.commit()
            logger.info(f"Recorded fee of {amount} for student {student_id} on {date_str}.")
            return True
        except Exception as e:
            logger.error(f"Error in FeeService.add_fee_record: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_fee_records(student_id=None):
        """
        Retrieves fee records. Can optionally filter by student_id.
        Returns a list of dictionaries with student names.
        """
        conn = None
        cursor = None
        records = []
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT f.id, f.student_id, s.name as student_name, s.class as student_class, f.amount, f.date 
                FROM fees f
                JOIN students s ON f.student_id = s.id
            """
            params = []
            
            if student_id:
                query += " WHERE f.student_id = %s"
                params.append(student_id)
                
            query += " ORDER BY f.date DESC, s.name ASC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            for row in rows:
                if isinstance(row['date'], datetime) or hasattr(row['date'], 'strftime'):
                    row['date'] = row['date'].strftime("%Y-%m-%d")
                # convert decimal to float
                row['amount'] = float(row['amount'])
                records.append(row)
                
            return records
        except Exception as e:
            logger.error(f"Error in FeeService.get_fee_records: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_total_fees():
        """
        Returns the total sum of fees collected.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(amount) FROM fees")
            total = cursor.fetchone()[0]
            return float(total) if total is not None else 0.0
        except Exception as e:
            logger.error(f"Error in FeeService.get_total_fees: {e}")
            return 0.0
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
