import falcon

from repositories.player import PlayersRepository
from typing import List, Dict

class PlayersController(object):
    """
    Controllers orchestrate calls to other controllers and repositories
    to complete API requests.
    """
    def __init__(self):
        self._repo = PlayersRepository()

    def create_item(self, req: falcon.Request):
        return self._repo.create_item(req)

    def delete_item(self, req: falcon.Request, contact_id: str) -> None:
        self._repo.delete_item(req, contact_id)

    def find_one(self) -> Dict:
        return self._repo.find_one()

    def get_list(self, req: falcon.Request) -> List[Dict]:
        return self._repo.get_list(req)

    def get_item(self, req: falcon.Request, contact_id: str) -> Dict:
        return self._repo.get_item(req, contact_id)

    def update_item(self, req: falcon.Request, contact_id: str) -> Dict:
        return self._repo.update_item(req, contact_id)

    def replace_item(self, req: falcon.Request, contact_id: str) -> Dict:
        return self._repo.replace_item(req, contact_id)