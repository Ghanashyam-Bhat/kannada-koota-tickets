from firebase_admin import firestore
ATTENDEES = "attendees"

def addToFirebase(data):
    db = firestore.client()
    newDoc = db.collection(ATTENDEES).document(data["hashVal"]).set(data)
    return newDoc