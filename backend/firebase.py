# Firebase Storage
import firebase_admin
from firebase_admin import credentials, storage, firestore

class FireBase:
    def __init__(self):
        self.__cred = credentials.Certificate('key/serviceKey.json')
        firebase_admin.initialize_app(self.__cred)
        self.bucket = storage.bucket('infuser-7a7c8.appspot.com')
        self.db = firestore.client()
    
    def timestamp(self):
        return firestore.firestore.SERVER_TIMESTAMP

    def reverse(self):
        return firestore.firestore.Query.DESCENDING
    
fireBase = FireBase()