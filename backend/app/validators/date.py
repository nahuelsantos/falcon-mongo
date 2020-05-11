import datetime as dt
from common.logging import Logger

class DateValidator(object):

    @staticmethod
    def validate_date_field(date):
        errors = []

        try:
            dt.datetime.fromisoformat(date)
        except Exception as e:
            errors.append("invalid date of birth")

        return errors
