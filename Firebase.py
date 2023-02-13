import os
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

if firebase_admin._DEFAULT_APP_NAME in firebase_admin._apps:
    cred = credentials.Certificate('tank-gps-61f21-firebase-adminsdk-b4tyt-66f87b4637.json')
    default_app = firebase_admin.initialize_app(cred)
else:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'tank-gps-61f21-firebase-adminsdk-b4tyt-66f87b4637.json'
    f = open(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    firebaseConfig = json.load(f)
    cred = firebase_admin.credentials.Certificate(firebaseConfig)
    f.close()

# Import database module.

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tank-gps-61f21-default-rtdb.firebaseio.com/'
})

# Get a database reference to our blog.
ref = db.reference('server/saving-data/fireblog')
users_ref = ref.child('users')
users_ref.set({
    'alanisawesome': {
        'date_of_birth': 'June 23, 1912',
        'full_name': 'Alan Turing'
    },
    'gracehop': {
        'date_of_birth': 'December 9, 1906',
        'full_name': 'Grace Hopper'
    }
})