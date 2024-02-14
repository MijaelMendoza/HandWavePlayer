#Importamos las librerias que se van a utilizar
import cv2
import mediapipe as mp
import time

# se asignan variables para usar las funciones que estan dentro de OpenCV y MediaPipe

capture = cv2.VideoCapture(0)           # inicia la captura de video
mpHands = mp.solutions.hands        # esta funcion nos permite un paquete prediseñado dentro de MediaPipe
hands = mpHands.Hands()             # nos da informacion de las manos
mpDraw = mp.solutions.drawing_utils # esta funcion nos permite dibujar las conecxiones entre todos los puntos de interes

pTime = 0
cTime = 0

# El siguiente código toma la entrada de imagen de la cámara
# Luego convierte la imagen de BGR a RGB.
# Esto se debe a que MediaPipe solo funciona con imágenes RGB, no con BGR, sería nuestro while principal

while True:
    success, img = capture.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    # usamos la condicion if para verificar si se detecta una mano.

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
         # Luego usamos el primer ciclo for para permitirnos trabajar con una mano a la vez.

            for id, lm in enumerate(handLms.landmark):

            #El segundo bucle for nos ayuda a obtener la información de los 21 puntos de interes de la mano que nos dará
            # las coordenadas x e y de cada punto enumerado en el diagrama de puntos de interes de la mano.
            # Este bucle también nos dará el id de cada punto.

                #print(id, lm)
                h, w, c = img.shape
                cx = int(lm.x * w)
                cy = int(lm.y * h)
                print(id, cx, cy)

                #El siguiente codigo dibuja los puntos de interes de la mano y las conexiones de la misma

                if id == 50:

                    cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            # Esta condicion if encierra en un círculo en el punto de interes número 20 del diagrama de la mano.
            # Esta es la punta del dedo meñique.


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 3)

    cv2.imshow("img", img)
    cv2.waitKey(1)

    # Usamos el código anterior para mostrar el resultado al usuario.
    # La salida es un video en tiempo real del usuario donde tiene iene las manos del usuario detectadas con
    # los 21 puntos de interes de las manos y las conexiones dibujadas en las manos.