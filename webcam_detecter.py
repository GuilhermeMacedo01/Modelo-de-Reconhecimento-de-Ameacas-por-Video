import cv2
from ultralytics import YOLO

cap = cv2.VideoCapture(0)

model = YOLO("C:/Users/guilh/OneDrive/Área de Trabalho/Armed-Person-Recognition/Modelo-de-Reconhecimento-de-Ameacas-por-Video/runs/detect/train12/weights/best.pt")

while True:
    success, img = cap.read()

    if success:
        results = model(img)

        for result in results:
            img = result.plot()

        cv2.imshow("Tela", img)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("desligando")
