# -*- coding: utf-8 -*-
"""
All operations on the MongoDB players collection
"""

import falcon
import os
import pymongo

from bson import errors as bsonErrors
from bson.objectid import ObjectId
from common.logging import Logger
from pymongo import MongoClient, ReturnDocument
from pymongo import errors as pymongoErrors
from typing import List, Dict, OrderedDict

class PlayersRepository():
    """
    Handles all interactions with the MongoDB players collection

    NOTES:
    MongoDB bson ObjectIds are not json serializable, however, you can cast
    the ObjectId to a str, which is, and use that str to construct an ObjectId
    for searching.
    """

    def __init__(self):
        self._uri = os.getenv('MONGO_URL', '')
        self._database = os.getenv('MONGO_DB', '')
        self._username = os.getenv('MONGO_USERNAME', '')
        self._password = os.getenv('MONGO_PASSWORD', '')

        if not self._uri:
            raise ValueError('DB_URL env var not set; required to connect to mongodb')
        self._client = MongoClient(self._uri,
                                  username=self._username, 
                                  password=self._password,
                                  authSource="admin",
                                  serverSelectionTimeoutMS=5000)
        self._db = self._client.fm
        self._db.players.create_index([('email', pymongo.ASCENDING)], unique=True)
        
        command = [("collMod", "players"),
            ("validator", { "$jsonSchema": { 
                "bsonType": "object", 
                "required": [ "username", "email", "gender" ], 
                "properties": { 
                    "username": { 
                        "bsonType": "string", 
                        "description": "required and must be a string" }, 
                    "email": { 
                        "bsonType": "string", 
                        "pattern": "^.+\@.+$", 
                        "description": "required and must be a valid email address" }, 
                    "gender": { 
                        "enum": [ "M", "F", "O" ], 
                        "description": "can be only M, F or O" },
                    "first_name": { 
                        "bsonType": "string", 
                        "description": "must be a string" }, 
                    "last_name": { 
                        "bsonType": "string", 
                        "description": "must be a string" }, 
                    "phone": { 
                        "bsonType": "string", 
                        "description": "must be a string" }
                }
            }}),
            ("validationLevel", "moderate")]
        command = OrderedDict(command)
        self._db.command(command)
        self._players = self._db.players
        
    def create_item(self, req: falcon.Request):
        try:
            result = self._players.insert_one(
                req.context['body']
            )
            return str(result.inserted_id)
        except (pymongoErrors.WriteError) as e:
            Logger('app').error('Failed to parse date: ' + str(e))
            self._handle_collection_invalid()
        except (pymongoErrors.AutoReconnect,
                pymongoErrors.ConnectionFailure,
                pymongoErrors.NetworkTimeout):
            self._handle_service_unavailable()

    def delete_item(self, _: falcon.Request, object_id: str) -> None:
        try:
            self._players.delete_one(
                {'_id': self._make_objectid(object_id)}
            )
        except (pymongoErrors.AutoReconnect,
                pymongoErrors.ConnectionFailure,
                pymongoErrors.NetworkTimeout):
            self._handle_service_unavailable()

    def find_one(self) -> Dict:
        try:
            return self._players.find_one()
        except (pymongoErrors.AutoReconnect,
                pymongoErrors.ConnectionFailure,
                pymongoErrors.NetworkTimeout):
            self._handle_service_unavailable()

    def get_list(self, _: falcon.Request) -> List[Dict]:
        try:
            # self._info("Fetching all players from datastore")
            result = []
            for player in self._players.find():
                player['_id'] = str(player['_id'])
                result.append(player)
            return result
        except (pymongoErrors.AutoReconnect,
                pymongoErrors.ConnectionFailure,
                pymongoErrors.NetworkTimeout) as e:
            Logger('app').error('Failed to get players: ' + str(e))
            self._handle_service_unavailable()

    def get_item(self, _: falcon.Request, object_id: str) -> Dict:
        try:
            player = self._players.find_one(
                {'_id': self._make_objectid(object_id)}
            )
            if player is None:
                self._handle_not_found(object_id)
            player['_id'] = str(player['_id'])
            return player
        except (pymongoErrors.AutoReconnect,
                pymongoErrors.ConnectionFailure,
                pymongoErrors.NetworkTimeout):
            self._handle_service_unavailable()

    def ping(self) -> None:
        """
        A very light weight database connectivity check used with liveness and
        readiness probes. Throws a service unavailable exception on failure
        :return:
        """
        try:
            self._db.admin.command('ping')
        except:  # pylint: disable=bare-except
            self._handle_service_unavailable()

    def replace_item(self, req: falcon.Request, object_id: str) -> Dict:
        try:
            result = self._players.find_one_and_replace(
                {'_id': self._make_objectid(object_id)},
                req.context['body'],
                return_document=ReturnDocument.AFTER)
            if result is None:
                self._handle_not_found(object_id)
            result['_id'] = str(result['_id'])
            return result
        except (pymongoErrors.AutoReconnect,
                pymongoErrors.ConnectionFailure,
                pymongoErrors.NetworkTimeout):
            self._handle_service_unavailable()

    def update_item(self, req: falcon.Request, object_id: str) -> Dict:
        try:
            result = self._players.find_one_and_update(
                {'_id': self._make_objectid(object_id)},
                {'$set': req.context['body']},
                return_document=ReturnDocument.AFTER)
            if result is None:
                self._handle_not_found(object_id)
            result['_id'] = str(result['_id'])
            return result
        except (pymongoErrors.AutoReconnect,
                pymongoErrors.ConnectionFailure,
                pymongoErrors.NetworkTimeout):
            self._handle_service_unavailable()

    def _make_objectid(self, object_id: str) -> ObjectId:
        try:
            return ObjectId(object_id)
        except bsonErrors.InvalidId as ex:
            raise falcon.HTTPBadRequest(
                title='Invalid player id: {}'.format(object_id),
                description=str(ex))

    def _handle_not_found(self, object_id) -> None:
        raise falcon.HTTPNotFound(
            title='Player not found',
            description="Player {} not found".format(object_id))

    def _handle_collection_invalid(self) -> str:
        raise falcon.HTTPBadRequest(
            title='Player request has incorrect format',
            description="Player request is invalid")

    def _handle_service_unavailable(self) -> None:
        raise falcon.HTTPServiceUnavailable(
            title='Datastore is unreachable',
            description="MongoDB at {} failed to respond to ping. "
                        "This is a transient, future attempts will work "
                        "when the datastore returns to service".format(self._uri),
            href='https://www.ctl.io/api-docs/v2/#firewall',
            retry_after=30
        )
