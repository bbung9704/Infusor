# Firebase Storage
import firebase_admin
from firebase_admin import credentials, storage

class FireBaseStorage:
    def __init__(self):
        self.__cred = credentials.Certificate('key/serviceKey.json')
        firebase_admin.initialize_app(self.__cred)
        self.bucket = storage.bucket('infuser-7a7c8.appspot.com')

fireBaseStorage = FireBaseStorage()