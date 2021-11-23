import numpy as np
from PIL import Image
img=Image.open('elephant.png')
arr=np.array(img)
print(arr.shape)
print(arr)
r=open("r.txt","a")
g=open("g.txt","a")
b=open("b.txt","a")
for i in range(arr.shape[0]):
 for j in range(arr.shape[1]):
 r.write(str(arr[i][j][0]).rstrip('\n')+", ")
 g.write(str(arr[i][j][1]).rstrip('\n')+", ")
 b.write(str(arr[i][j][2]).rstrip('\n')+", ")
 r.write("\n")
 g.write("\n")
 b.write("\n")
r.close()
g.close()
b.close() 