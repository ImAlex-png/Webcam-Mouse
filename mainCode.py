import os
import urllib.request
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# 1. Descarga automática del modelo si no existe
MODEL_PATH = "hand_landmarker.task"
if not os.path.exists(MODEL_PATH):
    print("Descargando modelo...")
    url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"
    urllib.request.urlretrieve(url, MODEL_PATH)

# 2. Configurar detector de MediaPipe
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)

# 3. Cámara y variables principales
cap = cv2.VideoCapture(0)
canvas = None
prev_x, prev_y = None, None

BUTTONS = [
    ("AZUL", (255, 0, 0)),
    ("VERDE", (0, 255, 0)),
    ("ROJO", (0, 0, 255)),
    ("AMARILLO", (0, 255, 255)),
    ("LIMPIAR", (50, 50, 50))
]
current_color = BUTTONS[1][1]  # Verde por defecto
header_h = 65

print("\n--- GESTOS ---")
print("• 1 Dedo: Dibujar")
print("• 2 Dedos: Seleccionar color arriba / Moverse")
print("• 3 Dedos: Borrador")
print("• Tecla 'q': Salir\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    if canvas is None:
        canvas = np.zeros_like(frame)

    # Inferencia de mano
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = detector.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))

    if res.hand_landmarks:
        pts = res.hand_landmarks[0]

        # Comprobación de dedos arriba (punta más alta que nudillo)
        idx_up = pts[8].y < pts[6].y
        mid_up = pts[12].y < pts[10].y
        rng_up = pts[16].y < pts[14].y

        ix, iy = int(pts[8].x * w), int(pts[8].y * h)
        mx, my = int(pts[12].x * w), int(pts[12].y * h)

        # 3 DEDOS: BORRADOR
        if idx_up and mid_up and rng_up:
            prev_x, prev_y = None, None
            rx, ry = int(pts[16].x * w), int(pts[16].y * h)
            ex, ey = (ix + mx + rx) // 3, (iy + my + ry) // 3
            cv2.circle(canvas, (ex, ey), 40, (0, 0, 0), -1)
            cv2.circle(frame, (ex, ey), 40, (255, 255, 255), 2)
            cv2.putText(frame, "BORRADOR", (ex - 45, ey - 48), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # 2 DEDOS: SELECCIONAR COLOR / MOVER
        elif idx_up and mid_up and not rng_up:
            prev_x, prev_y = None, None
            sx, sy = (ix + mx) // 2, (iy + my) // 2
            cv2.circle(frame, (sx, sy), 10, (255, 255, 255), 2)

            if sy < header_h:
                btn_w = w // len(BUTTONS)
                idx = min(sx // btn_w, len(BUTTONS) - 1)
                name, col = BUTTONS[idx]
                if name == "LIMPIAR":
                    canvas = np.zeros_like(frame)
                else:
                    current_color = col

        # 1 DEDO: DIBUJAR
        elif idx_up and not mid_up and not rng_up:
            if iy > header_h:
                cv2.circle(frame, (ix, iy), 6, current_color, -1)
                if prev_x is None:
                    prev_x, prev_y = ix, iy
                cv2.line(canvas, (prev_x, prev_y), (ix, iy), current_color, 6)
                prev_x, prev_y = ix, iy
            else:
                prev_x, prev_y = None, None
        else:
            prev_x, prev_y = None, None
    else:
        prev_x, prev_y = None, None

    # Superponer el dibujo sobre el fotograma
    has_paint = canvas.any(axis=2)
    frame[has_paint] = canvas[has_paint]

    # Barra superior con los botones
    btn_w = w // len(BUTTONS)
    for i, (name, col) in enumerate(BUTTONS):
        x1, x2 = i * btn_w, (i + 1) * btn_w
        cv2.rectangle(frame, (x1 + 2, 2), (x2 - 2, header_h), col, -1)
        border = (255, 255, 255) if col == current_color and name != "LIMPIAR" else (60, 60, 60)
        thick = 3 if border == (255, 255, 255) else 1
        cv2.rectangle(frame, (x1 + 2, 2), (x2 - 2, header_h), border, thick)
        cv2.putText(frame, name, (x1 + 10, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

    cv2.imshow("Air Canvas", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()