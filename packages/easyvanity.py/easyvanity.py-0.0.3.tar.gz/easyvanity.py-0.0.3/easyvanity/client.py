import ujson as json
import requests
from pymongo import MongoClient

from .lib.util import objects, exceptions


class Client(object):
    def __init__(self, mongoUri: str, siteUrl: str):
        self.mongoDb = mongoUri
        self.siteUri = siteUrl
        mongoCli = MongoClient('MONGOURL')
        self.db = mongoCli["easyvanity"]

    def createVanity(self, vanityLink: str, ownerId: str, callbackUrl: str):
        if self.mongoDb is None:
            return print('Error: No mongoUri defined...')
        else:
            url = {
                "vanityLink": str(vanityLink),
                "callback": str(callbackUrl),
                "ownerId": str(ownerId),
                "disabled": False
            }
            existing = self.db.urls.find_one({ "vanityLink": vanityLink })
            if existing is None:
                self.db.urls.insert_one(url)
                self.db.users.find_one({ "vanityLink": vanityLink })
                return f"Vanity created: {vanityLink}"
            else:
                return print('VanityLink already exists!')
        # headers = {
        #     "Authorization": apiKey
        # }
        # response = requests.get(f"{self.api}/public/bot/{botId}", headers=headers)
        # if response.status_code != 200: raise exceptions.CheckException(json.loads(response.text))
        # else: return objects.botInfo(json.loads(response.text)["response"])