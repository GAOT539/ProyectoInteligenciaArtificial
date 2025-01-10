import cv2
import numpy as np

def ordenar_puntos(puntos):
    n_puntos = np.concatenate([puntos[0], puntos[1], puntos[2], puntos[3]]).tolist()
    y_order = sorted(n_puntos, key=lambda n_puntos: n_puntos[1])
    x1_order = sorted(y_order[:2], key=lambda x1_order: x1_order[0])
    x2_order = sorted(y_order[2:4], key=lambda x2_order: x2_order[0])
    return [x1_order[0], x1_order[1], x2_order[0], x2_order[1]]

def calcular_distancia(punto1, punto2):
    distancia_pixeles = np.linalg.norm(np.array(punto1) - np.array(punto2))
    # Factor ajustado a cm (suponiendo que 29.7 corresponde a pulgadas)
    distancia_cm = (distancia_pixeles * 29.7 * 2.54) / 720
    #pulgadas distancia_cm = (distancia_pixeles * 29.7) / 720
    return distancia_cm

capturavideo = cv2.VideoCapture(0)  # Usa 0 para la cámara predeterminada

if not capturavideo.isOpened():
    print("No se pudo abrir la cámara")
    exit()

while True:
    ret, frame = capturavideo.read()
    if not ret:
        print("Error al capturar el frame")
        break

    imagenHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    verdeBajo = np.array([36, 14, 0], np.uint8)
    verdeAlto = np.array([56, 120, 255], np.uint8)
    maskVerde = cv2.inRange(imagenHSV, verdeBajo, verdeAlto)

    cnts = cv2.findContours(maskVerde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:2]

    puntos = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        cx, cy = x + w // 2, y + h // 2  # Centro del rectángulo
        puntos.append((cx, cy))
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)  # Marca el centro del objeto

    if len(puntos) == 2:
        distancia_cm = calcular_distancia(puntos[0], puntos[1])
        cv2.line(frame, puntos[0], puntos[1], (0, 0, 255), 2)
        mid_point = ((puntos[0][0] + puntos[1][0]) // 2, (puntos[0][1] + puntos[1][1]) // 2)
        cv2.putText(frame, "{:.2f} cm".format(distancia_cm), mid_point, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Detectar Distancia entre Objetos Verdes", frame)

    if cv2.waitKey(1) == ord('q'):
        break

capturavideo.release()
cv2.destroyAllWindows()
