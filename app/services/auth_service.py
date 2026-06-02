from app.utils.db import get_connection
from app.models.user_model import User
from app.utils.logger import get_logger

logger = get_logger()

class AuthService:
    @staticmethod
    def authenticate(username, password):
        """
        Authenticates an admin user based on username and password.
        Returns a User object if successful, None otherwise.
        """
        if not username or not username.strip():
            logger.warning("Authentication failed: Empty username field")
            raise ValueError("Username cannot be empty.")
            
        if not password or not password.strip():
            logger.warning("Authentication failed: Empty password field")
            raise ValueError("Password cannot be empty.")

        username = username.strip()
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            row = cursor.fetchone()

            if row:
                if row['password'] == password:
                    logger.info(f"User '{username}' successfully authenticated.")
                    return User(user_id=row['id'], username=row['username'], password=row['password'])
                else:
                    logger.warning(f"Failed login attempt for '{username}': Invalid password.")
            else:
                logger.warning(f"Failed login attempt: Username '{username}' does not exist.")
            return None

        except Exception as e:
            logger.error(f"Authentication error occurred for '{username}': {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
