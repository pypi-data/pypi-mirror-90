import ujson as json
import requests

from .lib.util import objects, exceptions


class Client(object):
    def __init__(self, mongoUri: str):
        self.mongoDb = mongoUri
    # if self.mongoUri is None:
    #     return print('Error: No mongoUri defined...')

    def get_bot_info(self, botId: int, apiKey: str):
        if self.mongoDb is None:
            return print('Error: No mongoUri defined...')
        # headers = {
        #     "Authorization": apiKey
        # }
        # response = requests.get(f"{self.api}/public/bot/{botId}", headers=headers)
        # if response.status_code != 200: raise exceptions.CheckException(json.loads(response.text))
        # else: return objects.botInfo(json.loads(response.text)["response"])