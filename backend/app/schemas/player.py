from .base import BaseSchema
from marshmallow import fields

class PlayerSchema(BaseSchema):
    username = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    phone = fields.Str()
    date_of_birth = fields.DateTime()
    gender = fields.Str()

