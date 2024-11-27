import numpy as np
import xxhash
from time import time
def keyGen(h,w):
    start=time()
    p='1'
    a=np.arange(h*w,dtype=np.uint8)
    b=np.copy(a)
    c=np.copy(b)

    for i in range(h*w):
        x=xxhash.xxh32_digest(p)
        a[i]=x[0]
        b[i]=x[1]/64
        c[i]=x[2]
        p=str(x)
    with open('00-2-chuuman-key-time.txt','a') as file:
        file.write(str(time()-start)+'\n')
    return a,b,c