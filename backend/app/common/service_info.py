# -*- coding: utf-8 -*-
"""
Service information
"""
import datetime as dt
from marshmallow import Schema, fields

class ServiceInfo(object):
    """Current build info"""
    service_name = 'falcon-api'
    service_environment = 'dev'
    version = '0.0.1-alpha'
    build_date = dt.datetime(2020, 5, 4, 4, 20, 0)

class ServiceInfoSchema(Schema):
    service_name = fields.Str()
    service_environment = fields.Str()
    version = fields.Str()
    build_date = fields.DateTime()

    class Meta:
        dateformat = '%Y-%m-%dT%H:%M:%S'
        ordered = True