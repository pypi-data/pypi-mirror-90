import ujson as json
import requests
from .__init__ import __version__
from .lib.util import objects, exceptions


class Client:
    def __init__(self):
        self.version = __version__

    def plugin_info(self, guildId: int):
        return self.version