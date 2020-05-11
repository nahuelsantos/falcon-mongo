from marshmallow import Schema, fields

class BaseSchema(Schema):
    _id = fields.UUID(required=True)
    created_utc = fields.DateTime(required=True)
    created_by = fields.Str(required=True)
    last_modified_utc = fields.DateTime(required=True)
    last_modified_by = fields.Str(required=True)
    active = fields.Boolean()
    
    class Meta:
        dateformat = '%Y-%m-%dT%H:%M:%S'
        ordered = True
