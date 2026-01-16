import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings
import os

FIREBASE_CRED_PATH = os.path.join(settings.BASE_DIR, 'firebase', 'soutenance-6fd64-firebase-adminsdk-fbsvc-82188dd175.json')

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CRED_PATH)
    firebase_admin.initialize_app(cred)