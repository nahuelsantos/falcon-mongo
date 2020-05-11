import datetime as dt

from .base import Base
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    def __init__(self, username, email, email_confirmed_at, password):
        self.username = username
        self.email = email
        self.email_confirmed_at = email_confirmed_at
        self.password = password
        self.last_login_utc = dt.datetime.utcnow()

    def __repr__(self):
        return "<User(username={self.username!r})>".format(self=self)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
