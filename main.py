import cv2

altura_barrera = 185
width, height = 320, 240
cap = cv2.VideoCapture('video.wmv')
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(gray)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    x1, y1 = 0, altura_barrera
    x2, y2 = width, altura_barrera

    M = cv2.moments(fgmask)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(frame, (cX, cY), 5, (255, 0, 255), -1)
        estado = "DENTRO" if cY < altura_barrera else "FUERA"

    cv2.putText(frame, "Pulsa W/S para subir/bajar la barrera", (0,10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, estado,(5,35), cv2.FONT_HERSHEY_SIMPLEX , 0.6, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), thickness=2)
    cv2.imshow('Real video',frame);
    cv2.imshow('frame', fgmask)
    
    k = cv2.waitKey(33)
    if k == 27:    # Esc key to stop
        break
    elif k == 119 and altura_barrera > 1:  # W, barrera ARRIBA
        altura_barrera -= 1
    elif k == 115 and altura_barrera < (height - 1):  # S, barrera ABAJO
        altura_barrera += 1
 
cap.release()
cv2.destroyAllWindows()