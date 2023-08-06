import ujson as json
import requests

from .lib.util import objects, exceptions


class Client:
    def __init__(self):
        self.api = "https://dbsl.ga/api"

    def get_server_info(self, guildId: int):
        response = requests.get(f"{self.api}/s/{guildId}")
        if response.status_code != 200: raise exceptions.CheckException(json.loads(response.text))
        else: return objects.Server(json.loads(response.text)["guild"])