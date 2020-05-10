from models import User

class UserStorage():
    
    def __init__(self):
        self.last_id = 0
        self.users = []

    def add_user(self, user: User):
        self.last_id += 1
        user.id = self.last_id
        self.users.append(user)

    def get_user_by_credentials(self, username, passwordHash):
        for index, item in enumerate(self.users):
            if item.username == username and item.passwordHash == passwordHash:
                return item
        return None

    def get_user_by_id(self, id):
        for index, item in enumerate(self.users):
            if item.id == id:
                return item
        return None




class SessionStorage():
    def __init__(self):
        self.last_id = 0
        self.refresh_tokens = []
       