import cv2



img=cv2.imread("MyPicture.jpg",1)
img=cv2.resize(img,(889,800))
cv2.imwrite("MyPicture.jpg",img)

img=cv2.imread("wali.jpeg",1)
img=cv2.resize(img,(889,800))
cv2.imwrite("wali.jpeg",img)

img=cv2.imread("ali.jpeg",1)
img=cv2.resize(img,(889,800))
cv2.imwrite("ali.jpeg",img)
