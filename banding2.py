import hashlib
import xxhash
from time import time
a='123'.encode('ascii')
size=1080*1920*3
start=time()
for i in range(size):
    a=hashlib.sha256(a).digest()
end=time()
print(end-start)

start=time()
a='123'.encode('ascii')
for i in range(size):
    a=xxhash.xxh128(a).digest()
end=time()
print(end-start)