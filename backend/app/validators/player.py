import datetime as dt
from .date import DateValidator

class PlayerValidator(object):

    @staticmethod
    def validate_post(body):
        """
        Validate create player params.

        Args:
            body dictionary with request body

        Returns:
            Empty array on success.
            Array of erros on fail.
        """
        errors = PlayerValidator._validate_required_fields(body)

        if "date_of_birth" in body:
            errors += DateValidator.validate_date_field(body["date_of_birth"])

        return errors


    @staticmethod
    def validate_put(body):
        """
        Validate replace player params.

        Args:
            body dictionary with request body

        Returns:
             Empty array on success.
            Array of erros on fail.
        """
        errors = PlayerValidator._validate_required_fields(body)

        if "_id" not in body:
            errors.append("_id is mandatory")

        if "date_of_birth" in body:
            errors += DateValidator.validate_date_field(body["date_of_birth"])

        return is_valid_req, errors


    @staticmethod
    def validate_patch(body):
        """
        Validate update player params.

        Args:
            body dictionary with request body

        Returns:
            Empty array on success.
            Array of erros on fail.
        """
        errors = []
        
        if "date_of_birth" in body:
            errors += DateValidator.validate_date_field(body["date_of_birth"])
        
        return errors

    @staticmethod
    def _validate_required_fields(body):
        errors = []

        if "username" not in body:
            is_valid_req = False
            errors.append("username is mandatory")

        if "email" not in body:
            is_valid_req = False
            errors.append("email is mandatory")

        if "gender" not in body or body["gender"] not in ["M", "F", "O"]:
            is_valid_req = False
            errors.append("gender is mandatory")
        
        return errors

