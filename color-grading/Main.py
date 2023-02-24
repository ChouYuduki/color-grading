import cv2 as cv
import numpy as np


def nothing(x):
    pass


def GammaConvert(img, ga_val):
    table = []
    for i in range(256):
        table.append(((i/255.0)**(1.0/ga_val))*255)
    table = np.array(table).astype('uint8')
    return cv.LUT(img, table)


def Change_saturation(img,num):
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    dst = np.array([int((num/100.0)*i) for i in range(256)]).astype("uint8")
    img_ori = np.array([i for i in range(256)]).astype("uint8")
    saturate = np.dstack((img_ori,dst,img_ori))
    img_saturated = cv.LUT(img_hsv,saturate)
    out = cv.cvtColor(img_saturated, cv.COLOR_HSV2BGR)
    return out


def Change_corTem(img,num):
    (b,g,r) = cv.split(img)
    r_out, g_out, b_out = r, g, b
    cv.convertScaleAbs(r,r_out,1,(num-100)/10)
    cv.convertScaleAbs(g,g_out,1,(num-100)/10)
    cv.convertScaleAbs(b,b_out,1,-(num-100)/10)
    out = cv.merge([b_out,g_out,r_out])
    out = np.clip(out, 0, 255)
    out = np.uint8(out)
    return out


def Contrast(img,num):
    out = img * (num/127 + 1) - num
    out = np.clip(out,0,255)
    out = np.uint8(out)
    return out


img = cv.imread('girl.jpg')
cv.namedWindow('img')
cv.createTrackbar('lightness','img',100,200,nothing)
cv.createTrackbar('saturation','img',100,200,nothing)
cv.createTrackbar('contrast','img',0,300,nothing)
cv.createTrackbar('temp','img',100,200,nothing)

while(True):
    light_bar = cv.getTrackbarPos('lightness','img')
    caturate_bar = cv.getTrackbarPos('saturation','img')
    contrast_bar = cv.getTrackbarPos('contrast','img')
    Tem_bar = cv.getTrackbarPos('temp','img')
    img_after = GammaConvert(img,light_bar/100.0)
    img_after2 = Change_saturation(img_after,caturate_bar)
    img_after3 = Contrast(img_after2,contrast_bar)
    img_after4 = Change_corTem(img_after3,Tem_bar)
    cv.imshow('img',img_after4)
    k = cv.waitKey(1)&0xFF
    if k == 27:
        break

# cv.waitKey()
cv.destroyWindow()
