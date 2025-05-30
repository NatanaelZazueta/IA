import cv2
import numpy as np
from tensorflow.keras.models import load_model

EMOCIONES = ['Enojado', 'Asco', 'Miedo', 'Feliz', 'Neutral', 'Triste', 'Sorprendido']

IMG_SIZE = (48, 48)

modelo = load_model("modelo_emociones.h5")

detector_rostros = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cam = cv2.VideoCapture(0)

print("Presiona 'q' para salir...")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rostros = detector_rostros.detectMultiScale(gris, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in rostros:
        rostro = gris[y:y+h, x:x+w]
        rostro_redim = cv2.resize(rostro, IMG_SIZE)
        rostro_redim = rostro_redim.astype("float32") / 255.0
        rostro_redim = np.expand_dims(rostro_redim, axis=-1)  
        rostro_redim = np.expand_dims(rostro_redim, axis=0)   

        pred = modelo.predict(rostro_redim, verbose=0)
        emocion = EMOCIONES[np.argmax(pred)]

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, emocion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (255, 255, 255), 2)

    cv2.imshow("Detector de Emociones", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
