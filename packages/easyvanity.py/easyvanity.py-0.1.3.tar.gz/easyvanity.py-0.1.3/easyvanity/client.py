import ujson as json
import requests
from pymongo import MongoClient

from .lib.util import objects, exceptions


class Client(object):
    def __init__(self, mongoUri: str, siteUrl: str, debug: bool):
        self.mongoDb = mongoUri
        self.siteUri = siteUrl
        self.debugMode = debug
        mongoCli = MongoClient(mongoUri)
        self.db = mongoCli["easyvanity"]
        if debug == True:
            print('Attempted connection to the database.')

    def createVanity(self, vanityId: str, ownerId: str, callbackUrl: str):
        if self.mongoDb is None:
            return print('Error: No mongoUri defined...')
        else:
            url = {
                "vanityId": str(vanityId),
                "callback": str(callbackUrl),
                "ownerId": str(ownerId),
                "disabled": False
            }
            existing = self.db.urls.find_one({ "vanityId": vanityId })
            if existing is None:
                self.db.urls.insert_one(url)
                self.db.urls.find_one({ "vanityId": vanityId })
                return f"New Vanity available at the following Id: {vanityId}"
            else:
                return print('VanityId already exists!')

    def getVanityById(self, vanityId: str):
        if self.mongoDb is None:
            return print('Error: no mongoUri defined...')
        else:
            vanity = self.db.urls.find_one({ "vanityId": vanityId })
            if vanity is None:
                if self.debugMode == True:
                    print('Vanity not found!')
                return "Vanity is not found!"
            else:
                if self.debugMode == True:
                    print(f"Raw data found: {vanity}")
                return objects.vanityData(vanity)
    
    def getUserVanities(self, ownerId: str):
        if self.mongoDb is None:
            return print('Error: no mongoUri defined...')
        else:
            userVans = self.db.urls.find({ "ownerId": ownerId })
            if userVans is None:
                return "No records found..."
            return objects.ownerVanities(json.loads(userVans)).ownerVanities

        # headers = {
        #     "Authorization": apiKey
        # }
        # response = requests.get(f"{self.api}/public/bot/{botId}", headers=headers)
        # if response.status_code != 200: raise exceptions.CheckException(json.loads(response.text))
        # else: return objects.botInfo(json.loads(response.text)["response"])