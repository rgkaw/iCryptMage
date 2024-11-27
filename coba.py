import xxhash
import cv2
from getpass import getpass
import numpy as np
from time import  time
from keyStream import keyStream
name=str(input("filename : "))
passwd=getpass("Password : ")
start=time()
img=cv2.imread(name)
img=np.ubyte(img)
height,width,channel=img.shape
print("generating keystream")
key1,key2,limit1,limit2=keyStream(passwd,height,width)
end=time()
initiationTime = end-start
ori=np.copy(img)
start=time()
cipher(key1,b)
end=time()
cipherTime=end-start
cip=np.copy(b)
start=time()
b=block_swap(key2,b)
end=time()
scrambleTime=end-start
swap=np.copy(b)
start=time()
b=block_deswap(key2,b)
end=time()
descrambleTime=end-start
deswap=np.copy(b)
start=time()
cipher(key1,b)
end=time()
dechiperTime=end-start
dec=np.copy(b)
end=time()
print("Initiation time = ",initiationTime)
print("Cipher time = ",cipherTime)
print("Scramble time = ",scrambleTime)
print("Descramble time = ",descrambleTime)
print("Decipher time = ",dechiperTime)
print("encrypt time = ", initiationTime +cipherTime+scrambleTime)
print("decrypt time = ",initiationTime+descrambleTime+dechiperTime)

cv2.imshow('0 original image',ori)
cv2.imshow('1 Cipher',cip)
cv2.imwrite('1 en-cipher.png',cip)
cv2.imwrite('2 block scrambling.png',swap)
cv2.imshow('2 block scramble',swap)
cv2.imwrite('3 block descrambling.png',deswap)
cv2.imshow('3 block descramble',deswap)
cv2.imshow('4 decrypted',dec)
cv2.imwrite('4 decrypted.png',dec)
cv2.waitKey(0)
