import pyfirmata
import time
import numpy as np 
import cv2 
import time


def detectar_hojas():
    _, imageFrame = webcam.read()

    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 


    red_lower = np.array([136, 87, 111], np.uint8) 
    red_upper = np.array([180, 255, 255], np.uint8) 
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 
  
    
    
    green_lower = np.array([25, 52, 72], np.uint8) 
    green_upper = np.array([102, 255, 255], np.uint8) 
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper) 
  
    
    
    blue_lower = np.array([94, 80, 2], np.uint8) 
    blue_upper = np.array([120, 255, 255], np.uint8) 
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper) 
      
    
    
    
    
    kernal = np.ones((5, 5), "uint8")


    red_mask = cv2.dilate(red_mask, kernal) 
    res_red = cv2.bitwise_and(imageFrame, imageFrame,  
                              mask = red_mask) 
      
    
    green_mask = cv2.dilate(green_mask, kernal) 
    res_green = cv2.bitwise_and(imageFrame, imageFrame, 
                                mask = green_mask) 
      
    
    blue_mask = cv2.dilate(blue_mask, kernal) 
    res_blue = cv2.bitwise_and(imageFrame, imageFrame, 
                               mask = blue_mask)

    # contours, hierarchy = cv2.findContours(red_mask, 
    #                                        cv2.RETR_TREE, 
    #                                        cv2.CHAIN_APPROX_SIMPLE) 
    
    # for pic, contour in enumerate(contours): 
    #     area = cv2.contourArea(contour) 
    #     if(area > 300): 
    #         x, y, w, h = cv2.boundingRect(contour) 
    #         imageFrame = cv2.rectangle(imageFrame,(x, y),  
    #                                    (x + w, y + h),  
    #                                    (0, 0, 255), 2) 
              
    #         cv2.putText(imageFrame, "Red Colour",(x, y), 
    #                     cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
    #                     (0, 0, 255))     
  
    
    contours, hierarchy = cv2.findContours(green_mask, 
                                           cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_SIMPLE) 

    posiciones = []
    valores = [0,0,0,0]

    for pic, contour in enumerate(contours): 
        area = cv2.contourArea(contour) 
        if(area > 2000): 
            x, y, w, h = cv2.boundingRect(contour)
            valores[0], valores[1],valores[2],valores[3] = x,y,w,h
            posiciones = posiciones + valores
            imageFrame = cv2.rectangle(imageFrame,(x, y),  
                                       (x + w, y + h), 
                                       (0, 255, 0), 2) 
            x1 = x + (w/2)
            y1 = y + (h/2)
            imageFrame = cv2.circle(imageFrame, (int(x1), int(y1)), 5, (255,0,0), 2)
              
            cv2.putText(imageFrame, "hoja",(x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX,  
                        1.0,(0, 255, 0)) 
  
    posiciones = np.array(posiciones)
    try:
        posiciones = np.array(np.split(posiciones,(posiciones.shape[0]/4)))
    except:
        posiciones = np.array([[0,0,0,0]])
    # contours, hierarchy = cv2.findContours(blue_mask, 
    #                                        cv2.RETR_TREE, 
    #                                        cv2.CHAIN_APPROX_SIMPLE) 
    # for pic, contour in enumerate(contours): 
    #     area = cv2.contourArea(contour) 
    #     if(area > 300): 
    #         x, y, w, h = cv2.boundingRect(contour) 
    #         imageFrame = cv2.rectangle(imageFrame,(x, y), 
    #                                    (x + w, y + h), 
    #                                    (255, 0, 0), 2) 
              
    #         cv2.putText(imageFrame, "Blue Colour",(x, y), 
    #                     cv2.FONT_HERSHEY_SIMPLEX, 
    #                     1.0,(255, 0, 0)) 
              
    
    cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame) 
    if cv2.waitKey(10) & 0xFF == ord('q'): 
        cap.release() 
        cv2.destroyAllWindows() 
    return posiciones

def conveyor(valor):
    conveyor.write(valor)

def velocidadMotores(vd,vi):
    motord.write(vd)
    motori.write(vi)

def ordenar(posiciones):

    ordenada = sorted(posiciones, key=lambda ok: ok[1],reverse=True)

    return np.array(ordenada)

def map(x, in_min, in_max, out_min, out_max):
		mapped =  float((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)
		return mapped 

def velocidad(posiciones):
    target = posiciones[0,:]

    x1 = target[0] + (target[2]/2)

    x1 = map(x1,0,640,-320,320)

    y1 = target[1] + (target[3]/2)

    y1 = map(y1,0,480,-240,240)

    x1 = map(x1,-320,320,0,100)
    
    vg = x1
    vl = 20

    vd = vl - vg
    vi = vl + vg

    print("vd = ",vd)
    print("vi = ",vi)
    #velocidadMotores()

if __name__ == '__main__':
    board = pyfirmata.Arduino('/dev/ttyACM0')
    print("Communication Successfully started")

    motord = board.digital[9]
    motori = board.digital[10]
    conveyor = board.digital[11]

    motord.mode = pyfirmata.PWM
    motori.mode = pyfirmata.PWM

    webcam = cv2.VideoCapture(0)

    while True:
        
        posiciones = detectar_hojas()

        posiciones = ordenar(posiciones)

        velocidad(posiciones)

        print("listo")
