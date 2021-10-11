import hashlib

path = ''
with open(path, 'rb') as f:
    print(hashlib.md5(f.read()).hexdigest())
