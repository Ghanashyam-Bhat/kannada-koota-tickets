from hashlib import sha256
import time

def generateUniqueData(id,email,name,phone):
    hash_val = sha256((id+name+email+phone+str(time.time())).encode('utf-8')).hexdigest()
    return hash_val