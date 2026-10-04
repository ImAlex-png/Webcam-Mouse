# 🎨 Air Canvas: Pizarra Virtual con Gestos de la Mano

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue?style=for-the-badge&logo=python" alt="Python Version" />
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-red?style=for-the-badge&logo=opencv" alt="OpenCV" />
  <img src="https://img.shields.io/badge/MediaPipe-Tasks%20Vision-orange?style=for-the-badge&logo=google" alt="MediaPipe" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License" />
</p>

Una aplicación de visión artificial en tiempo real que convierte tu cámara web en un lienzo interactivo. Permite **dibujar en el aire**, **cambiar de color con una paleta táctil aérea** y **borrar trazos**, todo controlado exclusivamente con los **gestos y dedos de tu mano**.

Construido y optimizado para la moderna API **MediaPipe Tasks** y compatible con las versiones más recientes de **Python (incluido Python 3.14)**.

---

## ✨ Características

- 🖌️ **Pintura en tiempo real**: Traza líneas fluidas en el aire usando la punta de tu dedo índice.
- 🎨 **Paleta de Colores en el Aire**: Barra superior interactiva con 4 colores (`Azul`, `Verde`, `Rojo`, `Amarillo`) y botón para vaciar el lienzo (`Limpiar`).
- 🧹 **Modo Borrador Gestual**: Levanta 3 dedos para activar una goma de borrar dinámica en tiempo real.
- ⚡ **Descarga Automática de IA**: No necesitas buscar ni descargar modelos manualmente; el script descarga el modelo preentrenado `hand_landmarker.task` en su primera ejecución.
- 🚀 **Fusión Ultrarrápida**: Motor de renderizado optimizado con NumPy en menos de 100 líneas de código limpio.

---

## 🖐️ Guía de Gestos y Controles

| Gesto | Nombre | Acción |
| :---: | :--- | :--- |
| ☝️ | **1 Dedo (Índice)** | **Modo Dibujar**: Pinta trazos continuos en pantalla con el color activo. |
| ✌️ | **2 Dedos (Índice + Corazón)** | **Modo Selección / Mover**: Desplaza el puntero sin pintar. Si tocas la barra superior, seleccionas un nuevo color o limpias el lienzo. |
| 🖖 | **3 Dedos (Índice + Corazón + Anular)** | **Modo Borrador**: Activa un círculo borrador que elimina los trazos por donde pases los dedos. |
| ⌨️ | **Tecla `q`** | Cierra la ventana y detiene la aplicación. |

---

## 🚀 Instalación y Puesta en Marcha

Sigue estos sencillos pasos para replicar y ejecutar el proyecto en tu ordenador:

### 1. Clonar el Repositorio
```bash
git clone https://github.com/TU-USUARIO/Webcam-Mouse.git
cd Webcam-Mouse
```

### 2. (Recomendado) Crear un Entorno Virtual

- **En Windows:**
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
- **En Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar Dependencias
Instala los paquetes necesarios con un solo comando:
```bash
pip install -r requirements.txt
```
*(Incluye `opencv-python`, `mediapipe>=1.0.1` y `numpy`).*

### 4. Ejecutar el Proyecto
```bash
python mainCode.py
```
> **Nota:** La primera vez que lo ejecutes, el programa descargará automáticamente el archivo de modelo de IA (`hand_landmarker.task`, ~7.8 MB). En las siguientes ejecuciones iniciará al instante.

---

## 🧠 ¿Cómo Funciona por Dentro?

El proyecto utiliza un pipeline directo de visión artificial y geometría computacional:

```
 Cámara Web (cv2.VideoCapture)
           ↓
 Invertir en espejo (cv2.flip)
           ↓
 Detección de mano (MediaPipe Tasks - HandLandmarker)
           ↓
 Clasificación de Gestos (Comparación de coordenadas Y)
           ↓
  ┌──────────────────┬──────────────────┬──────────────────┐
  │ 1 Dedo: Dibujo   │ 2 Dedos: Botones │ 3 Dedos: Borrado │
  │ cv2.line         │ Barra superior   │ cv2.circle negro │
  └──────────────────┴──────────────────┴──────────────────┘
           ↓
 Fusión rápida del lienzo y la cámara (NumPy boolean indexing)
           ↓
 Renderizado en ventana (cv2.imshow)
```

### Lógica de Detección de Dedos
En los sistemas de coordenadas de imagen, el origen `(0, 0)` se ubica en la esquina superior izquierda, por lo que **los valores de Y disminuyen hacia arriba**.
Un dedo se considera levantado si la punta (*Tip*) tiene una coordenada Y menor que su nudillo anterior (*PIP*):

- **Índice arriba:** `pts[8].y < pts[6].y`
- **Corazón arriba:** `pts[12].y < pts[10].y`
- **Anular arriba:** `pts[16].y < pts[14].y`

### Fusión sin Pérdida de Rendimiento
Para evitar conversiones lentas de máscaras bitwise en cada fotograma, el lienzo se superpone usando indexación directa de matrices de NumPy:
```python
has_paint = canvas.any(axis=2)
frame[has_paint] = canvas[has_paint]
```

---

## 📁 Estructura del Repositorio

```text
Webcam-Mouse/
│
├── mainCode.py            # Código fuente principal (menos de 115 líneas)
├── requirements.txt       # Dependencias necesarias del proyecto
├── hand_landmarker.task   # Modelo de detección de manos (autodescargable)
├── .gitignore             # Archivos excluidos de control de versiones
└── README.md              # Documentación e instrucciones del proyecto
```

---

## 🛠️ Tecnologías Utilizadas

- **[Python](https://www.python.org/)** (3.10 o superior, probado en 3.14).
- **[OpenCV](https://opencv.org/)**: Captura de cámara, transformaciones espaciales y renderizado gráfico.
- **[Google MediaPipe Tasks Vision](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)**: Detección y rastreo en tiempo real de los 21 puntos clave de la mano.
- **[NumPy](https://numpy.org/)**: Manipulación matricial de alta velocidad para la fusión de capas.

---

## 🤝 Contribuciones

¡Las contribuciones, ideas y sugerencias son bienvenidas! Si deseas mejorar este proyecto:
1. Haz un Fork del repositorio.
2. Crea una rama para tu función (`git checkout -b feature/NuevaFuncion`).
3. Haz un commit de tus cambios (`git commit -m 'Añadir nueva función'`).
4. Haz push a la rama (`git push origin feature/NuevaFuncion`).
5. Abre un Pull Request.

---

## 📄 Licencia

Este proyecto está bajo la Licencia **MIT**. Consulta el archivo `LICENSE` para más información.
