import os
from dotenv import load_dotenv
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

load_dotenv()

# Initialize Firebase
FIREBASE_CRED = os.environ.get("FIREBASE_CRED")
cred = credentials.Certificate(json.loads(FIREBASE_CRED))
firebase_admin.initialize_app(cred)

ATTENDEES = "attendees"

db = firestore.client()

with open("deleteuser.json") as data:
    jsonData = json.load(data)
    for i in jsonData:
        hashVal = i["hashVal"]
        db.collection(ATTENDEES).document(hashVal).delete()
