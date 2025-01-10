import sys
import cv2
import pytesseract
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

# Configuración de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

PROVINCIAS = {
    "A": "Azuay", "B": "Bolívar", "C": "Carchi", "H": "Chimborazo", "X": "Cotopaxi",
    "E": "Esmeraldas", "J": "Galápagos", "G": "Guayas", "I": "Imbabura", "L": "Loja",
    "O": "Los Ríos", "M": "Manabí", "R": "Morona Santiago", "N": "Napo", "S": "Pastaza",
    "P": "Pichincha", "Q": "Orellana", "K": "Sucumbíos", "T": "Tungurahua", "U": "Zamora Chinchipe",
    "W": "Santa Elena", "Y": "Santo Domingo", "Z": "Zamora"
}

MESES = {
    "1": "Febrero", "2": "Marzo", "3": "Abril", "4": "Mayo", "5": "Junio",
    "6": "Julio", "7": "Agosto", "8": "Septiembre", "9": "Octubre", "0": "Noviembre"
}

class ImageViewer(QDialog):
    def __init__(self, image, title="Imagen"):
        super().__init__()
        self.setWindowTitle(title)
        label = QLabel()

        # Redimensionar la imagen a 600x500
        resized_image = cv2.resize(image, (600, 500), interpolation=cv2.INTER_AREA)
        label.setPixmap(self.convert_image(resized_image))

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

    @staticmethod
    def convert_image(image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        qimage = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        return QPixmap.fromImage(qimage)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Proyecto 2: Sistema de Detección de Placas')
        self.setGeometry(100, 100, 500, 200)
        self.initUI()

    def initUI(self):
        # Título
        title_label = QLabel("Proyecto 2: Sistema de Detección de Placas", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px 0;")

        # Botones de reconocimiento en una fila horizontal
        btn_imagen = QPushButton("Reconocer placa en Imagen", self)
        btn_imagen.clicked.connect(self.reconocer_placa_imagen)

        btn_video = QPushButton("Reconocer placa en Video", self)
        btn_video.clicked.connect(self.reconocer_placa_video)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(btn_imagen)
        horizontal_layout.addWidget(btn_video)

        # Botón de Regresar
        btn_salir = QPushButton("Regresar", self)
        btn_salir.clicked.connect(self.close)
        btn_salir.setStyleSheet("font-size: 14px; padding: 5px;")
        btn_salir.setFixedHeight(30)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addLayout(horizontal_layout)
        layout.addWidget(btn_salir)

        # Contenedor principal
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def reconocer_placa_imagen(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Archivos de Imagen (*.png *.jpg *.jpeg)")
        if not file_path:
            print("No se seleccionó ninguna imagen.")
            return

        image = cv2.imread(file_path)
        if image is None:
            print(f"Error: No se pudo abrir la imagen desde {file_path}.")
            return

        # Pasar la imagen cargada para procesar
        self.procesar_placa(image)

    def procesar_placa(self, image):
        if image is None:
            print("Error: No se pudo cargar la imagen.")
            return

        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Aplicar detección de bordes para visualizar mejor las placas
        edges = cv2.Canny(gray, 100, 200)

        # Extraer texto con Tesseract OCR
        texto = pytesseract.image_to_string(gray, config='--oem 3 --psm 8').strip().upper()

        # Extraer información de provincia y mes
        provincia = PROVINCIAS.get(texto[:1], "Desconocida")
        mes = MESES.get(texto[-1:], "Desconocido")

        print(f"Texto detectado: {texto}")
        print(f"Provincia: {provincia}, Mes: {mes}")

        # Dibujar información sobre la imagen
        cv2.putText(image, f"Texto: {texto}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(image, f"Provincia: {provincia}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(image, f"Mes: {mes}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Mostrar la imagen procesada en una ventana de visor
        ImageViewer(image).exec_()

    def reconocer_placa_video(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error al abrir la cámara.")
            return

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Convertir a escala de grises
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Aplicar detección de bordes
                edges = cv2.Canny(gray, 100, 200)

                # Encontrar contornos
                contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                for contour in contours:
                    # Obtener un rectángulo delimitador para cada contorno
                    x, y, w, h = cv2.boundingRect(contour)

                    # Filtrar rectángulos por tamaño (placas suelen tener proporciones específicas)
                    if 100 < w < 300 and 30 < h < 100 and 2 < w / h < 6:
                        # Dibujar rectángulo en la imagen original
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                        # Recortar la región de interés (ROI) y extraer texto
                        roi = gray[y:y + h, x:x + w]
                        texto = pytesseract.image_to_string(roi, config='--oem 3 --psm 8').strip().upper()

                        # Extraer información de provincia y mes
                        provincia = PROVINCIAS.get(texto[:1], "Desconocida")
                        mes = MESES.get(texto[-1:], "Desconocido")

                        # Mostrar texto detectado en la imagen
                        cv2.putText(frame, f"Texto: {texto}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                        cv2.putText(frame, f"Provincia: {provincia}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        cv2.putText(frame, f"Mes: {mes}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # Mostrar video con rectángulos y texto
                cv2.imshow("Reconocimiento de Placa en Video", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = App()
    main_window.show()
    sys.exit(app.exec_())
