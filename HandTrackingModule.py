# importamos las librerias que usaremos
import cv2
import mediapipe as mp

# En el código siguiente, se usa una clase que sera para el seguimiento de la mano.
# Luego se definen los parámetros básicos que necesitamos para que la función hands funcione.
# MediaPipe proporciona estos parámetros en la función hands.

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.75, trackCon=0.75):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
# En el código siguiente, definimos un metedo para rastrear específicamente las manos en nuestra imagen de entrada.
# El código como en el primer prototipo es el que convierte la imagen a RGB y procesa la imagen RGB para ubicar las manos.
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
#En el código siguiente, definimos findPosition el que usaremos para encontrar las coordenadas x e y de cada uno de los 21 puntos de la mano.
# También creamos una lista que usaremos para almacenar los valores de estas coordenadas.
    def findPosition(self, img, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lmList

# El código siguiente los usaremos usaremos para mostrar lo que puede hacer el módulo.
# En este caso, puede identificar y rastrear manos y utiliza img y lmlist.
def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])

        cv2.imshow("Image", img)
        cv2.waitKey(1)

# El siguiente código implica que, si estamos usando el módulo, ejecute el codigo main.
if __name__ == "__main__":
    main()