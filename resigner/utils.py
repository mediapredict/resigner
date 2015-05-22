import hashlib

def data_hash(req_body):
    hash = hashlib.sha1()
    hash.update(req_body)
    return hash.hexdigest()[:10]