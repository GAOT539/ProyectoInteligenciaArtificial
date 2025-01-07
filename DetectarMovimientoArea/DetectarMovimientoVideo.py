import cv2
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def seleccionar_video():
    """Abre un cuadro de diálogo para seleccionar un archivo de video."""
    Tk().withdraw()  # Ocultar la ventana principal de Tkinter
    archivo_video = askopenfilename(
        title="Selecciona un archivo de video",
        filetypes=[("Archivos de video", "*.mp4 *.avi *.mov *.mkv")]
    )
    return archivo_video

def detectar_movimiento(video_path, ancho=600, alto=500):
    """Detecta movimiento en el video seleccionado."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: No se pudo abrir el archivo {video_path}")
        return

    # Inicializa el sustractor de fondo
    fgbg = cv2.createBackgroundSubtractorMOG2()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Redimensionar el frame al tamaño deseado (600x500)
        frame = cv2.resize(frame, (ancho, alto))

        # Convierte el frame a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Dibujamos un rectángulo en frame, para señalar el estado
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 30), (0, 0, 0), -1)
        color = (0, 255, 0)
        texto_estado = "Estado: No se ha detectado movimiento"

        # Especificamos los puntos extremos del área a analizar
        area_pts = np.array([[100, 50], [500, 50], [500, 400], [100, 400]])
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

        # Visualizar el estado de la detección de movimiento
        cv2.drawContours(frame, [area_pts], -1, color, 2)
        cv2.putText(frame, texto_estado, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        cv2.imshow("fgmask", fgmask)
        cv2.imshow("frame", frame)

        # Esperar por la tecla 'q' para salir
        k = cv2.waitKey(30) & 0xFF
        if k == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Seleccionar un archivo de video
    video_path = seleccionar_video()
    if video_path:
        detectar_movimiento(video_path, ancho=600, alto=500)
    else:
        print("No se seleccionó ningún archivo.")
