from pathlib import Path
import cv2
from ultralytics import YOLO

cap = cv2.VideoCapture(0)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "runs" / "detect" / "train12" / "weights" / "best.pt"

model = YOLO("/Users/guilherme.macedo/ArmedPeopleDetecter/Modelo-de-Reconhecimento-de-Ameacas-por-Video/runs/detect/train12/weights/best.pt")

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
