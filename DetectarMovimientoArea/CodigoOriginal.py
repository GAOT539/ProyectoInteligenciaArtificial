import cv2
import numpy as np

# Inicia la captura de video
cap = cv2.VideoCapture("Clip3.mp4")

# Inicializa el sustractor de fondo
fgbg = cv2.createBackgroundSubtractorMOG2()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

while True:
    ret, frame = cap.read()
    if ret == False:
        break

    # Convierte el frame a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Dibujamos un rectángulo en frame, para señalar el estado
    cv2.rectangle(frame, (0, 0), (frame.shape[1], 30), (0, 0, 0), -1)
    color = (0, 255, 0)
    texto_estado = "Estado: No se ha detectado movimiento"

    # Especificamos los puntos extremos del área a analizar
    area_pts = np.array([[425, 200], [850, 200], [1150, 570], [135, 570]])
    # Con ayuda de una imagen auxiliar, determinamos el área
    imAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
    imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
    image_area = cv2.bitwise_and(gray, gray, mask=imAux)

    # Obtendremos la imagen binaria donde la región en blanco representa el movimiento
    fgmask = fgbg.apply(image_area)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    fgmask = cv2.dilate(fgmask, None, iterations=2)

    # Encontramos los contornos presentes en fgmask
    cnts = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    for cnt in cnts:
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            texto_estado = "Estado: ALERTA Movimiento Detectado!"
            color = (0, 0, 255)

    # Convertir frame a HSV para la detección del color
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definir rango de color para la pelota de tenis (amarillo/verde)
    lower_color = np.array([25, 50, 50])
    upper_color = np.array([35, 255, 255])

    # Crear una máscara para detectar la pelota
    mask = cv2.inRange(hsv, lower_color, upper_color)
    mask = cv2.bitwise_and(mask, mask, mask=imAux)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.dilate(mask, None, iterations=2)

    # Encontrar contornos de la pelota
    ball_cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    for cnt in ball_cnts:
        if cv2.contourArea(cnt) > 100:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.circle(frame, (x + w // 2, y + h // 2), w // 2, (0, 255, 255), 2)
            texto_estado = "Estado: ALERTA Pelota Detectada!"
            color = (0, 0, 255)

    # Visualizar el estado de la detección de movimiento
    cv2.drawContours(frame, [area_pts], -1, color, 2)
    cv2.putText(frame, texto_estado, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow('fgmask', fgmask)
    cv2.imshow("mask", mask)
    cv2.imshow("frame", frame)

    k = cv2.waitKey(70) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()