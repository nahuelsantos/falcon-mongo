from .user import User

class Player(User):

    def __init__(self, first_name, last_name, phone, phone_confirmed_at, date_of_birth, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.phone = phone
        self.phone_confirmed_at = phone_confirmed_at
        self.gender = gender
        
    def __repr__(self):
        return "<Player(username={self.username!r})>".format(self=self)
        