# -*- coding: utf-8 -*-

import falcon
from datetime import datetime
from common.service_info import ServiceInfo, ServiceInfoSchema

class PingResource(object):
    """
    Returns 200 OK if we got this far, framework will fail or not respond
    otherwise
    """
    def on_get(self, _: falcon.Request, resp: falcon.Response):
        service_info = ServiceInfo()
        schema = ServiceInfoSchema()
        resp.status = falcon.HTTP_200
        resp.body = schema.dumps(service_info)
        