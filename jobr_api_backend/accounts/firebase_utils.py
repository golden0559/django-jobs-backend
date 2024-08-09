import firebase_admin
from firebase_admin import credentials, auth

def initialize_firebase():
    cred = credentials.Certificate('firebase-secrets.json')
    firebase_admin.initialize_app(cred)

initialize_firebase()