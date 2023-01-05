import cv2
img = cv2.imread('Nhu_y/Nhu_y84.png')
width = img.shape[1]
height = img.shape[0]
X_center = 0.36614583333333334 * width
Y_center = height/9
B_width = 0.005208333333333333 * width
B_height = 0.08888888888888889 * height
X_max = int(X_center + B_width/2)
X_min = int(X_center - B_width/2)
Y_max = int(Y_center + B_height/2)
Y_min = int(Y_center - B_height/2)

img_rec = cv2.rectangle(img, (X_max, Y_max), (X_min, Y_min), (0, 0, 255))
cv2.imwrite('test.png', img_rec)
