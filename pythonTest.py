import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv
import json
import os 

load_dotenv()

# Initialize Firebase
FIREBASE_CRED = os.environ.get("FIREBASE_CRED")
cred = credentials.Certificate(json.loads(FIREBASE_CRED))
firebase_admin.initialize_app(cred)

from firebase_admin import firestore

db = firestore.client()
newDoc = db.collection("test").add({"heelo":1})
print(newDoc)