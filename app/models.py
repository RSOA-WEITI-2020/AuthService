
class User():
    id = 0
    username = ""
    passwordHash = ""
    email = ""

    def __init__(self, username, passwordHash, email):
        self.username = username
        self.passwordHash = passwordHash
        self.email = email