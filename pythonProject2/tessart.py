import cv2
import pytesseract
from pytesseract import Output


def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)



img = cv2.imread('D:\\Downloads\\ocr2rotaa.jpg')

img = get_grayscale(img)
cv2.imshow('img', img)
cv2.waitKey(0)
img = thresholding(img);

cv2.imshow('img', img)
cv2.waitKey(0)

# Adding custom options
print(pytesseract.__version__)
custom_config = r'--psm  9 --oem 3 -c tessedit_char_whitelist=ABCD'
print(pytesseract.image_to_string(img, config=custom_config))
d = pytesseract.image_to_data(img,config=custom_config, output_type=Output.DICT)
print(d['text'])
n_boxes = len(d['text'])
for i in range(n_boxes):
    #if int(d['conf'][i]) > 10:
    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('img', img)
cv2.waitKey(0)