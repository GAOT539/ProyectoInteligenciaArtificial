import cv2
import numpy as np
import os
from tensorflow.keras.models import load_model

# Cargar modelo entrenado
#model = load_model("mask_detector_model.h5")
model_path = os.path.abspath(os.path.join("..", "DetectarMascarillas", "mask_detector_model.h5"))
model = load_model(model_path)
labels = ["Con mascarilla", "Sin mascarilla"]  # Cambiar el orden para corregir

# Configuración de la cámara
cap = cv2.VideoCapture(0)

IMG_SIZE = 224

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocesar frame
    resized = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
    normalized = resized / 255.0
    reshaped = np.reshape(normalized, (1, IMG_SIZE, IMG_SIZE, 3))

    # Predicción
    prediction = model.predict(reshaped)
    confidence = np.max(prediction)
    label = labels[np.argmax(prediction)]  # Etiqueta corregida

    # Color del texto según la clase
    color = (0, 255, 0) if label == "Con mascarilla" else (0, 0, 255)

    # Mostrar resultados
    cv2.putText(frame, f"{label} ({confidence * 100:.2f}%)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.rectangle(frame, (5, 5), (frame.shape[1] - 5, frame.shape[0] - 5), color, 2)
    cv2.imshow("Camara Mascarilla", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()