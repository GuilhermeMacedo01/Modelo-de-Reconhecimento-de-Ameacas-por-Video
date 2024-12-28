from ultralytics import YOLO
import cv2
from windowcapture import WindowCapture
from collections import defaultdict
import numpy as np

offset_x = 400
offset_y = 300
wincap = WindowCapture(size=(800, 600), origin=(offset_x, offset_y))

model = YOLO("trained_model.pt")
track_history = defaultdict(lambda: [])
seguir = True
deixar_rastro = True

while True:
    img = wincap.get_screenshot()

    if seguir:
        results = model.track(img, persist=True)
    else:
        results = model(img)

    for result in results:
        img = result.plot()

        if seguir and deixar_rastro:
            try:
                boxes = result.boxes.xywh.cpu()
                track_ids = result.boxes.id.int().cpu().tolist()

                for box, track_id in zip(boxes, track_ids):
                    x, y, w, h = box
                    track = track_history[track_id]
                    track.append((float(x), float(y)))
                    if len(track) > 30:
                        track.pop(0)

                    points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                    cv2.polylines(img, [points], isClosed=False, color=(230, 0, 0), thickness=5)
            except:
                pass

    cv2.imshow("Tela", img)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cv2.destroyAllWindows()
print("desligando")