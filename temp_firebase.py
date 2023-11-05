import os
from dotenv import load_dotenv
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

load_dotenv()

# Initialize Firebase
FIREBASE_CRED = os.environ.get("FIREBASE_CRED")
cred = credentials.Certificate(json.loads(FIREBASE_CRED))
firebase_admin.initialize_app(cred)

ATTENDEES = "attendees"

db = firestore.client()

allDocs = list(db.collection(ATTENDEES).stream())
print(len(allDocs))
allAttendees = list()
for doc in allDocs:
    docData = doc.to_dict()
    allAttendees.append(docData)

with open("attendeeData.json", "w") as jsonData:
    jsonData.write(json.dumps(allAttendees))
