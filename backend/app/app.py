import falcon

from common.logging import Logger
from common.middleware import Telemetry
from falcon_auth import FalconAuthMiddleware, JWTAuthBackend, BasicAuthBackend
from resources.health import PingResource
from resources.player import PlayerResource, PlayersResource


def initialize() -> falcon.API:

    api = application = falcon.API(media_type='application/vnd.api+json',
                                   middleware=[Telemetry()])
    
    api.add_route('/ping', PingResource())
    api.add_route('/players', PlayersResource())
    api.add_route('/players/{player_id}', PlayerResource())

    return api

def run() -> falcon.API:
    """
    :return: an initialized falcon.API
    """
    Logger('app').info("timap service starting")
    return initialize()

