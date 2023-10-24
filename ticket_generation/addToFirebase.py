from firebase_admin import firestore

ATTENDEES = "attendees"

def addToFirebase(data):
    db = firestore.client()
    newDoc = db.collection(ATTENDEES).add(data)
    return newDoc