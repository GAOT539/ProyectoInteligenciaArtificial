import tkinter as tk
import os
import subprocess
import threading
import traceback

from PIL import Image, ImageTk

# Variables globales
ventana_actual = None
proceso_script = None

# Función para centrar ventanas
def centrar_ventana(ventana, width, height):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (width // 2)
    y = (pantalla_alto // 2) - (height // 2)
    ventana.geometry(f"{width}x{height}+{x}+{y}")

# Función para abrir la ventana principal############################################################
def abrir_ventana_principal():
    global ventana_actual
    if ventana_actual:
        ventana_actual.destroy()
    
    ventana_inicio = tk.Tk()
    ventana_inicio.title("Inicio - Proyectos de IA")
    ventana_inicio.configure(bg="#e6e6e6")
    ventana_inicio.resizable(False, False)
    centrar_ventana(ventana_inicio, 460, 360)
    ventana_actual = ventana_inicio

    # Título principal
    titulo = tk.Label(ventana_inicio, text="Proyectos de Inteligencia Artificial", 
                      font=("Arial", 20, "bold"), bg="#e6e6e6", fg="#333333")
    titulo.grid(row=0, column=0, columnspan=2, pady=20)

    # Crear botones grandes en dos columnas
    ancho_boton = 20
    alto_boton = 3

    tk.Button(ventana_inicio, text="Proyecto 1:\nLectura de Lenguaje de Señas", font=("Arial", 12),
              width=ancho_boton, height=alto_boton, bg="#d9d9d9", wraplength=200, 
              command=abrir_proyecto1).grid(row=1, column=0, padx=20, pady=10)

    tk.Button(ventana_inicio, text="Proyecto 2:\nSistema de Detección de Placas", font=("Arial", 12),
              width=ancho_boton, height=alto_boton, bg="#d9d9d9", wraplength=200, 
              command=abrir_proyecto2).grid(row=1, column=1, padx=20, pady=10)

    tk.Button(ventana_inicio, text="Proyecto 3:\nDetectar Movimiento Área", font=("Arial", 12),
              width=ancho_boton, height=alto_boton, bg="#d9d9d9", wraplength=200, 
              command=abrir_proyecto3).grid(row=2, column=0, padx=20, pady=10)

    tk.Button(ventana_inicio, text="Proyecto 4:\nDetectar Mascarilla", font=("Arial", 12),
              width=ancho_boton, height=alto_boton, bg="#d9d9d9", wraplength=200, 
              command=abrir_proyecto4).grid(row=2, column=1, padx=20, pady=10)

    tk.Button(ventana_inicio, text="Proyecto 5:\nDistancia entre Objetos", font=("Arial", 12),
              width=ancho_boton, height=alto_boton, bg="#d9d9d9", wraplength=200, 
              command=abrir_proyecto5).grid(row=3, column=0, columnspan=2, pady=10)

    ventana_inicio.mainloop()

# Función para abrir el menú del Proyecto 1############################################################
def abrir_proyecto1():
    global ventana_actual
    if ventana_actual:
        ventana_actual.destroy()

    ventana_proyecto1 = tk.Tk()
    ventana_proyecto1.title("Proyecto 1 - Subproyectos")
    ventana_proyecto1.configure(bg="#f0f0f0")
    ventana_proyecto1.resizable(False, False)
    centrar_ventana(ventana_proyecto1, 500, 250)  # Ajusta el tamaño según sea necesario
    ventana_actual = ventana_proyecto1

    # Configurar una cuadrícula en el panel
    ventana_proyecto1.grid_rowconfigure(0, weight=1)  # Espacio arriba
    ventana_proyecto1.grid_rowconfigure(1, weight=1)  # Espacio para el título
    ventana_proyecto1.grid_rowconfigure(2, weight=1)  # Espacio para los botones
    ventana_proyecto1.grid_rowconfigure(3, weight=1)  # Espacio para el botón "Regresar"
    ventana_proyecto1.grid_rowconfigure(4, weight=1)  # Espacio abajo
    ventana_proyecto1.grid_columnconfigure(0, weight=1)  # Centrar horizontalmente
    ventana_proyecto1.grid_columnconfigure(1, weight=1)  # Centrar horizontalmente

    # Título centrado
    tk.Label(ventana_proyecto1, text="Proyecto 1: Lectura de Lenguaje de Señas", font=("Arial", 16, "bold"),
             bg="#f0f0f0", fg="#333333").grid(row=1, column=0, columnspan=2, pady=10)

    # Botones para subproyectos, centrados horizontalmente
    ancho_boton = 20
    alto_boton = 2

    tk.Button(ventana_proyecto1, text="Lectura de Letras", font=("Arial", 12), bg="#d9d9d9",
              width=ancho_boton, height=alto_boton, command=abrir_lectura_letras).grid(row=2, column=0, padx=10, pady=10, sticky="e")

    tk.Button(ventana_proyecto1, text="Lectura de Números", font=("Arial", 12), bg="#d9d9d9",
              width=ancho_boton, height=alto_boton, command=abrir_lectura_numeros).grid(row=2, column=1, padx=10, pady=10, sticky="w")

    # Botón de regresar, centrado y con ancho combinado
    tk.Button(ventana_proyecto1, text="Regresar", font=("Arial", 12), bg="#cccccc",
              width=ancho_boton * 2 + 4, height=alto_boton, command=abrir_ventana_principal).grid(row=3, column=0, columnspan=2, pady=20)

    ventana_proyecto1.mainloop()

# Función para abrir "Lectura de Letras"
def abrir_lectura_letras():
    global ventana_actual
    if ventana_actual:
        ventana_actual.destroy()

    # Crear el panel de Lectura de Letras
    ventana_letras = tk.Tk()
    ventana_letras.title("Lectura de Letras")
    ventana_letras.configure(bg="#f0f0f0")
    ventana_letras.resizable(False, False)
    centrar_ventana(ventana_letras, 500, 400)
    ventana_actual = ventana_letras

    # Configurar la cuadrícula
    ventana_letras.grid_rowconfigure(0, weight=1)  # Título
    ventana_letras.grid_rowconfigure(1, weight=1)  # Descripción
    ventana_letras.grid_rowconfigure(2, weight=2)  # Imagen
    ventana_letras.grid_rowconfigure(3, weight=1)  # Botones
    ventana_letras.grid_rowconfigure(4, weight=1)  # Espacio abajo
    ventana_letras.grid_columnconfigure(0, weight=1)

    # Título
    tk.Label(ventana_letras, text="Lectura de Letras", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333333").grid(row=0, column=0, pady=10)

    # Descripción
    tk.Label(ventana_letras, text="Este subproyecto permite reconocer letras en lenguaje de señas, facilitando la comunicación inclusiva.",
             font=("Arial", 12), wraplength=500, justify="center", bg="#f0f0f0", fg="#555555").grid(row=1, column=0, pady=10)

    # Imagen
    img_path = os.path.abspath(os.path.join("assets", "images", "lectura_letras.png"))
    img = Image.open(img_path)
    img = img.resize((300, 200), Image.ANTIALIAS)  # Redimensionar la imagen
    img_tk = ImageTk.PhotoImage(img)
    img_label = tk.Label(ventana_letras, image=img_tk, bg="#f0f0f0")
    img_label.image = img_tk  # Mantener una referencia a la imagen
    img_label.grid(row=2, column=0, pady=10)

    # Botones horizontales
    frame_botones = tk.Frame(ventana_letras, bg="#f0f0f0")
    frame_botones.grid(row=3, column=0, pady=20)

    tk.Button(frame_botones, text="Iniciar Ejecución", font=("Arial", 12), bg="#d9d9d9",
              command=lambda: threading.Thread(target=ejecutar_segment_letras).start()).pack(side="left", padx=20)
    tk.Button(frame_botones, text="Regresar", font=("Arial", 12), bg="#cccccc",
              command=lambda: regresar_a_proyecto1(ventana_letras)).pack(side="left", padx=20)

    ventana_letras.mainloop()

# Función para abrir "Lectura de Números"
def abrir_lectura_numeros():
    global ventana_actual
    if ventana_actual:
        ventana_actual.destroy()

    # Crear el panel de Lectura de Números
    ventana_numeros = tk.Tk()
    ventana_numeros.title("Lectura de Números")
    ventana_numeros.configure(bg="#f0f0f0")
    ventana_numeros.resizable(False, False)
    centrar_ventana(ventana_numeros, 500, 400)
    ventana_actual = ventana_numeros

    # Configurar la cuadrícula
    ventana_numeros.grid_rowconfigure(0, weight=1)  # Título
    ventana_numeros.grid_rowconfigure(1, weight=1)  # Descripción
    ventana_numeros.grid_rowconfigure(2, weight=2)  # Imagen
    ventana_numeros.grid_rowconfigure(3, weight=1)  # Botones
    ventana_numeros.grid_rowconfigure(4, weight=1)  # Espacio abajo
    ventana_numeros.grid_columnconfigure(0, weight=1)

    # Título
    tk.Label(ventana_numeros, text="Lectura de Números", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333333").grid(row=0, column=0, pady=10)

    # Descripción
    tk.Label(ventana_numeros, text="Este subproyecto facilita el reconocimiento de números en lenguaje de señas, útil para aplicaciones educativas y prácticas.",
             font=("Arial", 12), wraplength=500, justify="center", bg="#f0f0f0", fg="#555555").grid(row=1, column=0, pady=10)

    # Imagen
    img_path = os.path.abspath(os.path.join("assets", "images", "lectura_numeros.png"))
    img = Image.open(img_path)
    img = img.resize((300, 200), Image.ANTIALIAS)  # Redimensionar la imagen
    img_tk = ImageTk.PhotoImage(img)
    img_label = tk.Label(ventana_numeros, image=img_tk, bg="#f0f0f0")
    img_label.image = img_tk  # Mantener una referencia a la imagen
    img_label.grid(row=2, column=0, pady=10)

    # Botones horizontales
    frame_botones = tk.Frame(ventana_numeros, bg="#f0f0f0")
    frame_botones.grid(row=3, column=0, pady=20)

    tk.Button(frame_botones, text="Iniciar Ejecución", font=("Arial", 12), bg="#d9d9d9",
              command=lambda: threading.Thread(target=ejecutar_segment_numeros).start()).pack(side="left", padx=20)
    tk.Button(frame_botones, text="Regresar", font=("Arial", 12), bg="#cccccc",
              command=lambda: regresar_a_proyecto1(ventana_numeros)).pack(side="left", padx=20)

    ventana_numeros.mainloop()

# Función para ejecutar "Lectura de Letras"
def ejecutar_segment_letras():
    global proceso_script
    entorno_virtual = os.path.abspath(os.path.join("..", "EntornoVirt", "Scripts", "python.exe"))
    script_path = os.path.abspath(os.path.join("..", "LenguajeSeñas", "Code", "segment_vgg19_dia22_miguel.py"))

    try:
        proceso_script = subprocess.Popen([entorno_virtual, script_path])
        proceso_script.wait()
    except Exception as e:
        print(f"Error al ejecutar el script de Lectura de Letras: {e}")

# Función para ejecutar "Lectura de Números"
def ejecutar_segment_numeros():
    global proceso_script
    entorno_virtual = os.path.abspath(os.path.join("..", "EntornoVirt", "Scripts", "python.exe"))
    script_path = os.path.abspath(os.path.join("..", "LenguajeSeñas", "Code", "segment_modelmiguelnumber.py"))

    try:
        proceso_script = subprocess.Popen([entorno_virtual, script_path])
        proceso_script.wait()
    except Exception as e:
        print(f"Error al ejecutar el script de Lectura de Números: {e}")

# Función para regresar al menú del Proyecto 1
def regresar_a_proyecto1(ventana):
    global proceso_script
    if proceso_script and proceso_script.poll() is None:
        proceso_script.terminate()
        proceso_script.wait()

    abrir_proyecto1()
    ventana.destroy()
    abrir_proyecto1()
 
# Función para abrir el menú del Proyecto 2############################################################
def abrir_proyecto2():
    """Ocultar el panel principal mientras se ejecuta el Proyecto 2 y mostrarlo al finalizar."""
    global ventana_actual

    # Ocultar la ventana principal
    ventana_actual.withdraw()

    def ejecutar_y_mostrar():
        try:
            ejecutar_sistema_deteccion_placas()
        finally:
            # Mostrar la ventana principal al finalizar
            ventana_actual.deiconify()

    # Ejecutar el script en un hilo separado
    threading.Thread(target=ejecutar_y_mostrar).start()

def ejecutar_sistema_deteccion_placas():
    """Función para ejecutar el sistema de detección de placas."""
    global proceso_script
    entorno_virtual = os.path.abspath(os.path.join("..", "EntornoVirt", "Scripts", "python.exe"))
    script_path = os.path.abspath(os.path.join("..", "SistemaDeteccionPlacas", "SistemaDP.py"))

    print(f"Ruta del entorno virtual: {entorno_virtual}")
    print(f"Ruta del script: {script_path}")

    try:
        # Validar que el entorno virtual y el script existan
        if not os.path.exists(entorno_virtual):
            raise FileNotFoundError(f"El entorno virtual no existe: {entorno_virtual}")
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"El archivo del script no existe: {script_path}")

        # Ejecutar el script
        proceso_script = subprocess.Popen(
            [entorno_virtual, script_path],
            stdout=subprocess.PIPE,  # Capturar salida estándar
            stderr=subprocess.PIPE   # Capturar errores estándar
        )

        # Leer las salidas y esperar a que el proceso termine
        stdout, stderr = proceso_script.communicate()

        # Imprimir las salidas
        if stdout:
            print("Salida del script:\n", stdout.decode())
        if stderr:
            print("Errores del script:\n", stderr.decode())

    except FileNotFoundError as fnf_error:
        print(f"Archivo no encontrado: {fnf_error}")
    except PermissionError as perm_error:
        print(f"Error de permisos: {perm_error}")
    except Exception as e:
        print(f"Error inesperado:\n{traceback.format_exc()}")
 
# Función para abrir el menú del Proyecto 3############################################################
def abrir_proyecto3():
    """Abrir el submenú del Proyecto 3."""
    global ventana_actual
    if ventana_actual:
        ventana_actual.destroy()

    ventana_proyecto3 = tk.Tk()
    ventana_proyecto3.title("Proyecto 3 - Detectar Movimiento Área")
    ventana_proyecto3.configure(bg="#f0f0f0")
    ventana_proyecto3.resizable(False, False)
    centrar_ventana(ventana_proyecto3, 450, 300)  # Ajusta el tamaño según sea necesario
    ventana_actual = ventana_proyecto3

    # Configurar una cuadrícula en el panel
    ventana_proyecto3.grid_rowconfigure(0, weight=1)  # Espacio para el título
    ventana_proyecto3.grid_rowconfigure(1, weight=1)  # Espacio para los botones
    ventana_proyecto3.grid_rowconfigure(2, weight=1)  # Espacio para el botón "Regresar"
    ventana_proyecto3.grid_columnconfigure(0, weight=1)

    # Título centrado
    tk.Label(ventana_proyecto3, text="Proyecto 3: Detectar Movimiento Área", font=("Arial", 16, "bold"),
             bg="#f0f0f0", fg="#333333").grid(row=0, column=0, pady=10)

    # Botones
    ancho_boton = 25
    alto_boton = 2

    tk.Button(ventana_proyecto3, text="Detectar Movimiento Cámara", font=("Arial", 12), bg="#d9d9d9",
              width=ancho_boton, height=alto_boton, command=abrir_detectar_movimiento_camara).grid(row=1, column=0, pady=10)
    
    tk.Button(ventana_proyecto3, text="Detectar Movimiento Video", font=("Arial", 12), bg="#d9d9d9",
              width=ancho_boton, height=alto_boton, command=abrir_detectar_movimiento_video).grid(row=2, column=0, pady=10)

    # Botón de regresar
    tk.Button(ventana_proyecto3, text="Regresar", font=("Arial", 12), bg="#cccccc",
              width=ancho_boton, height=alto_boton, command=abrir_ventana_principal).grid(row=3, column=0, pady=20)

    ventana_proyecto3.mainloop()

# Función para abrir Detectar Movimiento Cámara
def abrir_detectar_movimiento_camara():
    """Ejecutar el script de detección de movimiento usando la cámara y manejar la interfaz."""
    global ventana_actual

    # Bloquear y ocultar la ventana actual
    ventana_actual.withdraw()

    def ejecutar_y_mostrar():
        try:
            ejecutar_detectar_movimiento_camara()
        finally:
            # Mostrar y desbloquear la ventana al finalizar
            ventana_actual.deiconify()

    # Ejecutar el script en un hilo separado
    threading.Thread(target=ejecutar_y_mostrar).start()

def ejecutar_detectar_movimiento_camara():
    """Función para ejecutar el script de detección de movimiento con la cámara."""
    global proceso_script
    entorno_virtual = os.path.abspath(os.path.join("..", "EntornoVirt", "Scripts", "python.exe"))
    script_path = os.path.abspath(os.path.join("..", "DetectarMovimientoArea", "DetectarMovimientoCamara.py"))

    print(f"Ruta del entorno virtual: {entorno_virtual}")
    print(f"Ruta del script: {script_path}")

    try:
        # Validar que el entorno virtual y el script existan
        if not os.path.exists(entorno_virtual):
            raise FileNotFoundError(f"El entorno virtual no existe: {entorno_virtual}")
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"El archivo del script no existe: {script_path}")

        # Ejecutar el script
        proceso_script = subprocess.Popen(
            [entorno_virtual, script_path],
            stdout=subprocess.PIPE,  # Capturar salida estándar
            stderr=subprocess.PIPE   # Capturar errores estándar
        )

        # Leer las salidas y esperar a que el proceso termine
        stdout, stderr = proceso_script.communicate()

        # Imprimir las salidas
        if stdout:
            print("Salida del script:\n", stdout.decode())
        if stderr:
            print("Errores del script:\n", stderr.decode())

    except FileNotFoundError as fnf_error:
        print(f"Archivo no encontrado: {fnf_error}")
    except PermissionError as perm_error:
        print(f"Error de permisos: {perm_error}")
    except Exception as e:
        print(f"Error inesperado:\n{traceback.format_exc()}")

# Función para abrir Detectar Movimiento Video
def abrir_detectar_movimiento_video():
    """Ejecutar el script de detección de movimiento desde un video y manejar la interfaz."""
    global ventana_actual

    # Bloquear y ocultar la ventana actual
    ventana_actual.withdraw()

    def ejecutar_y_mostrar():
        try:
            ejecutar_detectar_movimiento_video()
        finally:
            # Mostrar y desbloquear la ventana al finalizar
            ventana_actual.deiconify()

    # Ejecutar el script en un hilo separado
    threading.Thread(target=ejecutar_y_mostrar).start()

def ejecutar_detectar_movimiento_video():
    """Función para ejecutar el script de detección de movimiento desde un video."""
    global proceso_script
    entorno_virtual = os.path.abspath(os.path.join("..", "EntornoVirt", "Scripts", "python.exe"))
    script_path = os.path.abspath(os.path.join("..", "DetectarMovimientoArea", "DetectarMovimientoVideo.py"))

    print(f"Ruta del entorno virtual: {entorno_virtual}")
    print(f"Ruta del script: {script_path}")

    try:
        # Validar que el entorno virtual y el script existan
        if not os.path.exists(entorno_virtual):
            raise FileNotFoundError(f"El entorno virtual no existe: {entorno_virtual}")
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"El archivo del script no existe: {script_path}")

        # Ejecutar el script
        proceso_script = subprocess.Popen(
            [entorno_virtual, script_path],
            stdout=subprocess.PIPE,  # Capturar salida estándar
            stderr=subprocess.PIPE   # Capturar errores estándar
        )

        # Leer las salidas y esperar a que el proceso termine
        stdout, stderr = proceso_script.communicate()

        # Imprimir las salidas
        if stdout:
            print("Salida del script:\n", stdout.decode())
        if stderr:
            print("Errores del script:\n", stderr.decode())

    except FileNotFoundError as fnf_error:
        print(f"Archivo no encontrado: {fnf_error}")
    except PermissionError as perm_error:
        print(f"Error de permisos: {perm_error}")
    except Exception as e:
        print(f"Error inesperado:\n{traceback.format_exc()}")

# Función para abrir el menú del Proyecto 4############################################################
def abrir_proyecto4():
    """Ejecutar el script de detección de mascarilla y manejar la interfaz."""
    global ventana_actual

    # Bloquear y ocultar la ventana principal
    ventana_actual.withdraw()

    def ejecutar_y_mostrar():
        try:
            ejecutar_detectar_mascarilla()
        finally:
            # Mostrar y desbloquear la ventana principal al finalizar
            ventana_actual.deiconify()

    # Ejecutar el script en un hilo separado
    threading.Thread(target=ejecutar_y_mostrar).start()

def ejecutar_detectar_mascarilla():
    """Función para ejecutar el script de detección de mascarilla."""
    global proceso_script
    entorno_virtual = os.path.abspath(os.path.join("..", "EntornoVirt", "Scripts", "python.exe"))
    script_path = os.path.abspath(os.path.join("..", "DetectarMascarillas", "Mascarilla.py"))

    print(f"Ruta del entorno virtual: {entorno_virtual}")
    print(f"Ruta del script: {script_path}")

    try:
        # Validar que el entorno virtual y el script existan
        if not os.path.exists(entorno_virtual):
            raise FileNotFoundError(f"El entorno virtual no existe: {entorno_virtual}")
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"El archivo del script no existe: {script_path}")

        # Ejecutar el script
        proceso_script = subprocess.Popen(
            [entorno_virtual, script_path],
            stdout=subprocess.PIPE,  # Capturar salida estándar
            stderr=subprocess.PIPE   # Capturar errores estándar
        )

        # Leer las salidas y esperar a que el proceso termine
        stdout, stderr = proceso_script.communicate()

        # Imprimir las salidas
        if stdout:
            print("Salida del script:\n", stdout.decode())
        if stderr:
            print("Errores del script:\n", stderr.decode())

    except FileNotFoundError as fnf_error:
        print(f"Archivo no encontrado: {fnf_error}")
    except PermissionError as perm_error:
        print(f"Error de permisos: {perm_error}")
    except Exception as e:
        print(f"Error inesperado:\n{traceback.format_exc()}")

# Función para abrir el menú del Proyecto 5############################################################
def abrir_proyecto5():
    """Ejecutar el script de distancia entre objetos y manejar la interfaz."""
    global ventana_actual

    # Bloquear y ocultar la ventana principal
    ventana_actual.withdraw()

    def ejecutar_y_mostrar():
        try:
            ejecutar_distancia_objetos()
        finally:
            # Mostrar y desbloquear la ventana principal al finalizar
            ventana_actual.deiconify()

    # Ejecutar el script en un hilo separado
    threading.Thread(target=ejecutar_y_mostrar).start()

def ejecutar_distancia_objetos():
    """Función para ejecutar el script de distancia entre objetos."""
    global proceso_script
    entorno_virtual = os.path.abspath(os.path.join("..", "EntornoVirt", "Scripts", "python.exe"))
    script_path = os.path.abspath(os.path.join("..", "DistanciaEntreObjetosVerdes", "DistanciaDosObjetos.py"))

    print(f"Ruta del entorno virtual: {entorno_virtual}")
    print(f"Ruta del script: {script_path}")

    try:
        # Validar que el entorno virtual y el script existan
        if not os.path.exists(entorno_virtual):
            raise FileNotFoundError(f"El entorno virtual no existe: {entorno_virtual}")
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"El archivo del script no existe: {script_path}")

        # Ejecutar el script
        proceso_script = subprocess.Popen(
            [entorno_virtual, script_path],
            stdout=subprocess.PIPE,  # Capturar salida estándar
            stderr=subprocess.PIPE   # Capturar errores estándar
        )

        # Leer las salidas y esperar a que el proceso termine
        stdout, stderr = proceso_script.communicate()

        # Imprimir las salidas
        if stdout:
            print("Salida del script:\n", stdout.decode())
        if stderr:
            print("Errores del script:\n", stderr.decode())

    except FileNotFoundError as fnf_error:
        print(f"Archivo no encontrado: {fnf_error}")
    except PermissionError as perm_error:
        print(f"Error de permisos: {perm_error}")
    except Exception as e:
        print(f"Error inesperado:\n{traceback.format_exc()}")

# Iniciar la aplicación
abrir_ventana_principal()
