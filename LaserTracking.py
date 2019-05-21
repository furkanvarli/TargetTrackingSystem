#Tanımlar
import cv2, time
import numpy as np
import RPi.GPIO as GPIO

#Servo Pin Ayarları
servoPIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) 
p.start(2.5)

#açıya göre servo konum hesabı
angle=90
duty=angle/20+2
p.ChangeDutyCycle(duty)

# kameradan görüntü alınması
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

m=0
mid_x=0

# renk tespiti
while True:
    _, img = cap.read()

    # renk uzayı filtreleme için bgrdan hsvye dönüştürülür
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #turuncu nesnenin tespiti için gereken sınır değerler    
    orange_lower = np.array([5,50,50],np.uint8)
    orange_upper = np.array([15,255,255],np.uint8)

    # sınır değerlere göre filtreleme işlemleri
    orange = cv2.inRange(hsv, orange_lower, orange_upper)
       
    kernal = np.ones((5 ,5), "uint8")

    blue=cv2.dilate(orange, kernal)

    res=cv2.bitwise_and(img, img, mask = orange)

    (_,contours,hierarchy)=cv2.findContours(orange,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # tespit edilen renkteki nesnenin etrafına kutu çizilmesi    
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>5000):
            x,y,w,h = cv2.boundingRect(contour)     
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),3)
            mid_x=x+w/2 # nesnenin orta nokta koordinatı bulunur

    # servo ile nesne takip algoritması
    
    if(mid_x>320) and abs(mid_x-320)>150:      
        
        angle=angle-5
        
        if angle < 10:
            angle=10
            
        duty = angle / 20.0 + 2
        p.ChangeDutyCycle(duty)
                
    elif(mid_x<320) and abs(mid_x-320)>150:
        
        angle=angle+5
        
        if angle > 180:
            angle = 180
            
        duty = angle / 20.0 + 2
        p.ChangeDutyCycle(duty)
 

    time.sleep(0.05)




        


    
