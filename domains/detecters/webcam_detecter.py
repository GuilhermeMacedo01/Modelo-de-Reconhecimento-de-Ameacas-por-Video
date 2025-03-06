import cv2
import numpy as np
from ultralytics import YOLO

from domains.email_sender.send_email import send_email_with_image

def preprocess_frame(frame):
    """ Melhora a imagem """
    
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    l = cv2.equalizeHist(l)
    lab = cv2.merge((l, a, b))

    enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    kernel = np.array([[0, -0.5, 0], [-0.5, 3, -0.5], [0, -0.5, 0]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)

    return sharpened

cap = cv2.VideoCapture(0)


model = YOLO("/Users/guilherme.macedo/ArmedPeopleDetecter/Modelo-de-Reconhecimento-de-Ameacas-por-Video/runs/detect/train12/weights/best.pt")

bateu=0
while True:
    success, img = cap.read()
    if success:
        processed_img = preprocess_frame(img)
        
        results = model(img, conf=0.6)

        for result in results:
            detections = result.boxes
            
            for detection in detections:
                class_id = int(detection.cls)
                label = result.names[class_id]
                confidence = detection.conf 
                
                if label == 'pessoa armada' and confidence > 0.6 and bateu==0:
                    bateu=1
                    send_email_with_image(img) 
                    print("Arma detectada. E-mail enviado.")



            img = result.plot()

        cv2.imshow("Tela", img)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Desligando")
