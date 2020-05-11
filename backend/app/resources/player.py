import datetime as dt
import falcon

from bson import ObjectId
from common.logging import Logger
from controllers.player import PlayersController
from models.player import Player
from schemas.player import PlayerSchema
from validators.date import DateValidator
from validators.player import PlayerValidator

class _Resource():
    
    def __init__(self):
        self._controller = PlayersController()

    @staticmethod
    def _validate_post(req: falcon.Request, _: falcon.Response, __, ___):
        """
        Validate create player params.

        Args:
            req (falcon.Request): the client request
            resp (falcon.Response): the client response (so far)
            resource:
            params:

        Returns:
            Nothing on success.

            Raises a falcon.HTTPBadRequest on validation error with explanation
            in response body.
        """
        errors = PlayerValidator.validate_post(req.context["body"])
        
        if errors:
            raise falcon.HTTPBadRequest("Bad request", errors)

        if "_id" not in req.context["body"]:
            req.context["body"]["_id"] =  ObjectId()
        
        if "date_of_birth" in req.context["body"]:
            req.context["body"]["date_of_birth"] = dt.datetime.fromisoformat(req.context["body"]["date_of_birth"])

        req.context["body"]["created_utc"] = dt.datetime.utcnow()
        req.context["body"]["created_by"] = req.context["body"]["username"]
        req.context["body"]["last_modified_utc"] = dt.datetime.utcnow()
        req.context["body"]["last_modified_by"] = req.context["body"]["username"]
        req.context["body"]["active"] = True 


    @staticmethod
    def _validate_put(req: falcon.Request, _: falcon.Response, __, ___):
        """
        Validate replace player params.

        Args:
            req (falcon.Request): the client request
            resp (falcon.Response): the client response (so far)
            resource:
            params:

        Returns:
            Nothing on success.

            Raises a falcon.HTTPBadRequest on validation error with explanation
            in response body.
        """
        errors = PlayerValidator.validate_put(req.context["body"])
        
        if errors:
            raise falcon.HTTPBadRequest("Bad request", errors)

        if "date_of_birth" in req.context["body"]:
            req.context["body"]["date_of_birth"] = dt.datetime.fromisoformat(req.context["body"]["date_of_birth"])

        req.context["body"]["last_modified_utc"] = dt.datetime.utcnow()
        req.context["body"]["last_modified_by"] = req.context["body"]["username"]


    @staticmethod
    def _validate_patch(req: falcon.Request, _: falcon.Response, __, ___):
        """
        Validate update player params.

        Args:
            req (falcon.Request): the client request
            resp (falcon.Response): the client response (so far)
            resource:
            params:

        Returns:
            Nothing on success.

            Raises a falcon.HTTPBadRequest on validation error with explanation
            in response body.
        """
        errors = PlayerValidator.validate_patch(req.context["body"])
        
        if errors:
            raise falcon.HTTPBadRequest("Bad request", errors)
        
        if "date_of_birth" in req.context["body"]:
            req.context["body"]["date_of_birth"] = dt.datetime.fromisoformat(req.context["body"]["date_of_birth"])

        req.context["body"]["last_modified_utc"] = dt.datetime.utcnow()
        req.context["body"]["last_modified_by"] = req.context["body"]["username"]


class PlayerResource(_Resource):
    """Handler for element operations"""

    def on_delete(self, req: falcon.Request, _: falcon.Response, player_id: str) -> None:
        self._controller.delete_item(req, player_id)

    def on_get(self, req: falcon.Request, resp: falcon.Response, player_id: str) -> None:
        data = self._controller.get_item(req, player_id)
        resp.body = PlayerSchema().dumps(data)

    @falcon.before(_Resource._validate_patch)
    def on_patch(self, req: falcon.Request, resp: falcon.Response, player_id: str) -> None:
        data = self._controller.update_item(req, player_id)
        resp.body = PlayerSchema().dumps(data)

    @falcon.before(_Resource._validate_put)
    def on_put(self, req: falcon.Request, resp: falcon.Response, player_id: str) -> None:
        data = self._controller.replace_item(req, player_id)
        resp.body = PlayerSchema().dumps(data)

class PlayersResource(_Resource):
    """Handler for collection operations"""

    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        data = self._controller.get_list(req)
        Logger("app").info(str(data))
        resp.body =  PlayerSchema().dumps(data, many=True)

    @falcon.before(_Resource._validate_post)
    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        data = self._controller.create_item(req)
        resp.status = falcon.HTTP_200
        resp.body = PlayerSchema().dumps(data)