import datetime as dt

class Base(object):

    def __init__(self, id, public_id, created_by, last_modified_by, active):
        self.id = id
        self.created_utc = dt.datetime.utcnow()
        self.created_by = created_by
        self.last_modified_utc = dt.datetime.utcnow()
        self.last_modified_by = last_modified_by
        self.active = active

