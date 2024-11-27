from time import sleep,time
import cv2
from cv2 import waitKey
from matplotlib.pyplot import switch_backend
import numpy as np
from perbandingan_key import keyGen
from cv2 import hconcat, vconcat

def block_inverse(keystream,b):
    for i in range(len(keystream)):
        while(keystream[i]>=(limit1*limit2)):
            keystream[i]=keystream[i]-(limit1*limit2)
    blocks=[]
    for i in range(0,limit1):
        for j in range(0,limit2):
            blocks.append(b[i*8:(i+1)*8,j*8:(j+1)*8])
    for i in range(0,limit1*limit2):
        r=keystream[i]
        if r>127:
            blocks[i]=255-blocks[i]
            None
    v_image=[]
    for i in range(0,limit1*limit2,limit2):
        h_image=hconcat(blocks[i:i+limit2])
        v_image.append(h_image)
    final_image=vconcat(v_image)
    return final_image

def block_deinverse(keystream,b):
    for i in range(len(keystream)):
        while(keystream[i]>=(limit1*limit2)):
            keystream[i]=keystream[i]-(limit1*limit2)
    blocks=[]
    for i in range(0,limit1):
        for j in range(0,limit2):
            blocks.append(b[i*8:(i+1)*8,j*8:(j+1)*8])
    for i in range(0,limit1*limit2):
        r=keystream[i]
        if r>127:
            None
            blocks[i]=255-blocks[i]
    v_image=[]
    for i in range(0,limit1*limit2,limit2):
        h_image=hconcat(blocks[i:i+limit2])
        v_image.append(h_image)
    final_image=vconcat(v_image)
    return final_image

def block_rotate(keystream,blocks):
    for i in range(len(keystream)):
        while(keystream[i]>=(limit1*limit2)):
            keystream[i]=keystream[i]-(limit1*limit2)
    for i in range(0,limit1*limit2):
        g=keystream[i]
        blocks[i]=np.rot90(blocks[i],g,(0,1))
    return blocks

def block_derotate(keystream,blocks):
    for i in range(len(keystream)):
        while(keystream[i]>=(limit1*limit2)):
            keystream[i]=keystream[i]-(limit1*limit2)
    for i in range(0,limit1*limit2):
        g=keystream[i]
        blocks[i]=np.rot90(blocks[i],-g,(0,1))
    return blocks
def block_scramble(key,blocks):
    for i in range (len(blocks)):
        blocks[i],blocks[key[i]]=blocks[key[i]],blocks[i]
        None

    v_image=[]
    for i in range(0,limit1*limit2,limit2):
        h_image=hconcat(blocks[i:i+limit2])
        v_image.append(h_image)
    final_image=vconcat(v_image)
    return final_image
def block_descramble(key,blocks):
    for i in range (len(blocks)-1,-1,-1):
        blocks[i],blocks[key[i]]=blocks[key[i]],blocks[i]
        None
    return blocks
def color_shuffling(blocks):
    for i in range(len(blocks)):
        swap=key4[i]
        for j in range(len(blocks[i])):
            for k in range(len(blocks[i][j])):
                # blocks[i][j,k,swap[0]],blocks[i][j,k,swap[1]]=blocks[i][j,k,swap[1]],blocks[i][j,k,swap[0]]
                blocks[i][j,k,swap[1]],blocks[i][j,k,swap[2]]=blocks[i][j,k,swap[2]],blocks[i][j,k,swap[1]]
                None
    return blocks

# def color_deshuffling(blocks):
#     for i in range(len(blocks)):
#         swap=key4[i]
#         if i==2:
#             print(blocks[i][j])
#         for j in range(len(blocks[i])):
#             for k in range(len(blocks[i][j])):
#                 # blocks[i][j,k,swap[0]],blocks[i][j,k,swap[1]]=blocks[i][j,k,swap[1]],blocks[i][j,k,swap[0]]
#                 blocks[i][j,k,swap[1]],blocks[i][j,k,swap[2]]=blocks[i][j,k,swap[2]],blocks[i][j,k,swap[1]]

#                 None

#     return blocks


start=time()
b=cv2.imread("leena.png")
b=cv2.cvtColor(b,cv2.COLOR_BGR2YCrCb)
block_size=8
y,cr,cb=cv2.split(b)
a=[y,cr,cb]
a=cv2.hconcat(a)
x=int(a.shape[1]/block_size)
y=int(a.shape[0]/block_size)
key1,key2,key3=keyGen(x,y)
blocks=[]
limit1=int(a.shape[0]/8)
limit2=int(a.shape[1]/8)


final_image=block_inverse(key1,a)
y=final_image[:,:b.shape[1]]
cb=final_image[:,b.shape[1]:b.shape[1]*2]
cr=final_image[:,b.shape[1]*2:]
final = cv2.merge((y,cb,cr))


limit1=int(final.shape[0]/8)
limit2=int(final.shape[1]/8)
blocks=[]

for i in range(0,limit1):
    for j in range(0,limit2):
        blocks.append(final[i*8:(i+1)*8,j*8:(j+1)*8])
final_2=block_rotate(key2,blocks)


key4=[]
for i in range(len(blocks)):
    sw=np.arange(3)
    np.random.shuffle(sw)
    key4.append(sw)
final_3=color_shuffling(final_2)
final_4=block_scramble(key3,final_3)

end=time()
cv2.imwrite("leena-chuuman.png",final_4)
blocks=[]
for i in range(0,limit1):
    for j in range(0,limit2):
        blocks.append(final_4[i*8:(i+1)*8,j*8:(j+1)*8])
dec4=block_descramble(key3,blocks)

dec3=color_shuffling(dec4)
dec2=block_derotate(key2,dec3)


v_image=[]
for i in range(0,limit1*limit2,limit2):
    h_image=hconcat(dec2[i:i+limit2])
    v_image.append(h_image)
final_image=vconcat(v_image)

y,cr,cb=cv2.split(final_image)

limit2=int(a.shape[1]/8)
bgr=cv2.hconcat((y,cr,cb))
dec1=block_deinverse(key1,bgr)

y=dec1[:,:b.shape[1]]
cb=dec1[:,b.shape[1]:b.shape[1]*2]
cr=dec1[:,b.shape[1]*2:]
ycbcr=cv2.merge((y,cb,cr))

final=cv2.cvtColor(ycbcr,cv2.COLOR_YCrCb2BGR)
with open('00-1-chuuman-total-time.txt','a') as file:
    file.write(str(end-start)+'\n')




# np.random.shuffle(a_linear)
# a_reshaped=np.reshape(a_linear,a.shape)
# cv2.imshow('2',a_reshaped)
# cv2.waitKey(0)
# for i in range(0,limit1):
#     for j in range(0,limit2):
#         blocks.append(b[i*8:(i+1)*8,j*8:(j+1)*8])

# print(len(blocks),len(blocks[0]))
# for i in range(a_linear.shape[0]):
#     # print(i,key1[i])
#     blocks[i],blocks[key1[i]]=blocks[key1[i]],blocks[i]
    


    # a_linear[[i,key1[i]]]=a_linear[[key1[i],i]]
# for i in range(len(a_linear)):
#     if key3[i]>128:
#         a_linear[i]=cv2.bitwise_not(a_linear[i])
    
# for i in range(len(a_linear)):
#     blocks[i],blocks[key1[i]]=blocks[key1[i]],blocks[i]

# for i in range(len(a_linear)):
#     blocks[i]=np.rot90(a_linear[i],key2[i],(0,1))
# v_image=[]
# for i in range(0,12288,192):
#     h_image=hconcat(blocks[i:i+192])
#     v_image.append(h_image)
    # if v_image!=[]:
    #     cv2.imshow('leena-chuuman.png',cv2.vconcat(v_image))
    #     cv2.waitKey(0)
    # cv2.imshow('leena-chuuman.png',(h_image))
    
    
# final_image=vconcat(v_image)




# v_img=[]
# for i in range(0,y):
#     h_img=a_linear[i*x:(i*x)+x]
#     v_img.append(cv2.hconcat(h_img))
# v_img=cv2.vconcat(v_img)

# y=final_image[:,:b.shape[1]]
# cb=final_image[:,b.shape[1]:b.shape[1]*2]
# cr=final_image[:,b.shape[1]*2:]
# final = cv2.merge((y,cb,cr))
# end=time()
# print("time: ",end-start)
# cv2.show('leena-chuuman.png',final)
# cv2.waitKey(0)



