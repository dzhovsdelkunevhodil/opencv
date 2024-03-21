# В рамках данной лабораторной работы вам необходимо выполнить следующее:
# 1)Сформировать изображение при помощи инструментов OpenCV в котором:
# 1.1) Разные фигуры: (1 равносторонний треугольник, 1 произвольный треугольник, ромб, трапеция,
# квадрат, пятиугольник),
# круг и 1 - 3 фигур на ваше усмотрение.
# 1.2) Фигуры должны быть разных цветов на ваше усмотрение
#
# В рамках задачи по поиску контуров, цветов фигур и площадей вам нужно:
# 1) В начале изображения вывести № вашей группы, ФИО, количество найденных контуров.
# В терминал вывести ту же информацию.
# 2) Обвести все ваши объекты в контур
# 3) Найти центры объектов, отметить их на каждой из фигур,
# от центра найденных объектов добавить подписи для каждого из типа фигур
# и их цвета.
# 4) Вывести площади всех найденных фигур
# 5) Вывести цвета фигур
#
# 6) Вывести в терминал общее количество фигур и ниже представить количество по каждой из фигур, пример:
# Общее количество фигур: 6
# Треугольников – 2 (1 равносторонний зеленый площадью 2010, 1 произвольный красный площадью 1780)
# Четырехугольников – 3 ….
# и т.д.
# Цветовую гамму и размеры шрифтов можете использовать по вашему усмотрению.

#######################################################################################################################

import cv2
import numpy as np
import imutils
import math

d = {}

masks = {
"Orange (fcac3c)": ((15, 192, 250), (19, 196, 254)),
"Light-Orange (fcd48c)": ((17, 111,250), (21, 115, 254)),
"Cherry (841237)": ((168, 218, 130), (172, 222, 134)),
"Cian (5aa0a1)": ((88, 110, 159), (92, 114, 163)),
"Light-Cian (a4d4cc)": ((83, 56, 210), (87, 60, 214)),
"Brown (a47f62)": ((11, 101, 162),(15, 105, 166)),
"Sea (07517f)": ((99, 239, 125),(103, 243, 129)),
"Swamp (49452a)": ((24, 106, 71),(28, 108, 75)),
}
colors = ["Orange (fcac3c)", "Light-Orange (fcd48c)", "Cherry (841237)", "Cian (5aa0a1)", "Light-Cian (a4d4cc)",
          "Brown (a47f62)","Sea (07517f)","Swamp (49452a)"]

###################################################################################################
class ShapeDetector:
    def __init__(self):
        pass
    def detect(self, c, color, area):
        shape = "unidentified" + ' ' + color + ' '+ area
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        if len(approx) == 3:
            l0 = math.sqrt((approx[0,0][0] - approx[1,0][0])**2 + (approx[0,0][1] - approx[1,0][1])**2)
            l1 = math.sqrt((approx[0,0][0] - approx[2,0][0])**2 + (approx[0,0][1] - approx[2,0][1])**2)
            l2 = math.sqrt((approx[1,0][0] - approx[2,0][0])**2 + (approx[1,0][1] - approx[2,0][1])**2)

            if (abs(l0 - l1) < 5 and abs(l0 - l2) < 5) :
                shape = "eq triangle" + ' ' + color + ' '+ area
            else :
                shape = "uneq triangle" + ' ' + color + ' '+ area
        elif len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            if ar >= 0.95 and ar <= 1.05:
                shape = "square" + ' ' + color + ' '+ area

            else:
                l0 = math.sqrt((approx[0, 0][0] - approx[1, 0][0]) ** 2 + (approx[0, 0][1] - approx[1, 0][1]) ** 2)
                l1 = math.sqrt((approx[1, 0][0] - approx[2, 0][0]) ** 2 + (approx[1, 0][1] - approx[2, 0][1]) ** 2)
                l2 = math.sqrt((approx[2, 0][0] - approx[3, 0][0]) ** 2 + (approx[2, 0][1] - approx[3, 0][1]) ** 2)
                l3 = math.sqrt((approx[3, 0][0] - approx[0, 0][0]) ** 2 + (approx[3, 0][1] - approx[0, 0][1]) ** 2)
                diagonal = math.sqrt((approx[1, 0][0] - approx[3, 0][0]) ** 2 + (approx[1, 0][1] - approx[3, 0][1]) ** 2)
                if (abs(l0 - l1) < 5 and abs(l0 - l2) < 5 and abs(l1 - l2) < 5 and abs(l2 - l3) < 5):
                    shape = "romb" + ' ' + color + ' '+ area
                else:
                    angle = np.degrees(np.arccos((l0**2 + l1**2 - diagonal**2) / (2*l0*l1)))
                    if angle <= 95 and angle >= 85:
                        shape = "rectangle" + ' ' + color + ' '+ area
                    else:
                        shape = "trapezoid" + ' ' + color + ' '+ area
        elif len(approx) == 5:
            shape = "pentagon" + ' ' + color + ' '+ area
        else:
            shape = "circle" + ' ' + color + ' '+ area
        if shape in d:
            d[shape] += 1
        else:
            d[shape] = 1
        return shape

#######################################################################################################

img = np.zeros((700, 1500, 3), dtype='uint8')
img[:] = 255, 255, 255

vertices = np.array([[198, 270], [275, 215], [210, 215]], np.int32)
cv2.fillPoly(img, [vertices], (60, 172, 252)) #1

center = (1200, 200)
dif = 150
eqvertices = []
for i in range(3):
    x = int(center[0]+ dif*np.cos(i*2*np.pi/3))
    y = int(center[1]+ dif*np.sin(i*2*np.pi/3))
    eqvertices.append((x,y))
eqvertices = np.array(eqvertices)
cv2.fillPoly(img, [eqvertices], (140, 212,252)) #2

cv2.rectangle(img, (240,70), (970, 200), (55, 18, 132), thickness=cv2.FILLED) #3

cv2.rectangle(img, (img.shape[1]//2-55,img.shape[0]//2-55), (img.shape[1]//2+55,img.shape[0]//2+55), (161, 160, 90), thickness=cv2.FILLED) #4

vertices = np.array([[198, 470],[210, 415],[275, 415], [287, 470]], np.int32)
cv2.fillPoly(img, [vertices], (204, 212, 164)) #5

vertices = np.array([[365, 570],[385, 515],[425, 515], [437, 570], [380, 600]], np.int32)
cv2.fillPoly(img, [vertices], (98, 127, 164)) #6

vertices = np.array([[1200, 470],[1300, 320],[1400, 470], [1300, 620]], np.int32)
cv2.fillPoly(img, [vertices], (127, 81,7 )) #7

cv2.circle(img, (img.shape[1]//2+110,img.shape[0]//2+100), 50, (42, 69, 73), thickness=cv2.FILLED) #8

cv2.circle(img, (img.shape[1]//2+11,img.shape[0]//2+200), 2, (42, 69, 73), thickness=cv2.FILLED) #...

cv2.circle(img, (img.shape[1]//2+61,img.shape[0]//2+170), 2, (42, 69, 73), thickness=cv2.FILLED) #...

########################################################################################################################

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 220, 255, cv2.THRESH_BINARY_INV)[1]
cnts, ir = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
sd = ShapeDetector()

for color in colors:

    mask = cv2.inRange(hsv, masks[color][0], masks[color][1])
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 10]#погрешность

    for c in contours:
        M = cv2.moments(c)
        cX = int((M["m10"] / M["m00"]))
        cY = int((M["m01"] / M["m00"]))

        area = '0'
        if contours:
            area = str([cv2.contourArea(cnt) for cnt in contours])
        #print(color + ": " + area)
        #cv2.putText(img, str(color + ": " + area), (cX + 10, cY + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        shape = sd.detect(c, color, area)
        cv2.drawContours(img, [c], -1, (51, 51, 51), 3)
        cv2.circle(img, (cX, cY), 7, (0, 0, 0), -1)
        cv2.putText(img, shape, (cX - 155, cY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        # cv2.putText(img, str(round(cv2.contourArea(c), 2)), (cX + 10, cY + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 0, 0), 2)
        # cv2.putText(img, color, (cX + 10, cY + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
# for c in cnts:
#     M = cv2.moments(c)
#     cX = int((M["m10"] / M["m00"]))
#     cY = int((M["m01"] / M["m00"]))
#     shape = sd.detect(c)
#     cv2.circle(img, (cX, cY), 7, (0, 0, 0), -1)
#     cv2.putText(img, shape, (cX+10, cY+5), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 0), 2)
#     cv2.putText(img, str(round(cv2.contourArea(c) , 2)), (cX + 10, cY + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
#     #cv2.putText(img, shape, (cX + 10, cY + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
#     cv2.drawContours(img, [c], -1, (11, 11, 111), 2)

##############################################################################################################################

text = "1144, Zhabin Matvey Alexandrovich, founded {} objects!".format(len(cnts))
print(text)
cv2.putText(img, text, (10, 25), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0,0,0), 2)
print(d)
cv2.imshow("Photo", img)
cv2.waitKey(0)