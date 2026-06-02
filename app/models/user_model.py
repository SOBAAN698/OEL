class User:
    def __init__(self, user_id=None, username="", password=""):
        self.id = user_id
        self.username = username
        self.password = password

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}')"
