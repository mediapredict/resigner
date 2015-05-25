import hashlib

def data_hash(req_body, time_stamp):
    hash = hashlib.sha1()
    hash.update(req_body + time_stamp)
    return hash.hexdigest()[:10]