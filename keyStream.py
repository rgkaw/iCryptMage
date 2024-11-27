from xxhash import xxh128
from hashlib import sha256
import numpy
from time import time
def keyStream(passwd,height,width):
    start=time()
    n=1
    channel=3
    a=passwd
    array=[]
    sha=sha256(a.encode("ASCII")).digest()
    def c(x):
        ctr=0
        x=xxh128(x).digest()
        for i in x:
            i=i^sha[ctr]
            if ctr<16:
                ctr+=1
            else:
                ctr=0
            array.append(i)
        return x
    while len(array)<width*height*channel:
        a=c(a)
    keystream1=numpy.reshape(numpy.array(array[:height*width*3],dtype=numpy.uint8),(height,width,3))

    limit1=int(height/8)
    limit2=int(width/8)
    keystream2=(array[limit1:limit1+(limit1*limit2)])
    with open('00-4-iCryptMage-total-time.txt','a') as file:
        file.write(str(time()-start)+'\n')
    return keystream1,keystream2,limit1,limit2
