import os
import cv2
from ultralytics import YOLO


model = YOLO('yolov8n.pt')
data_yaml_path = '/Users/guilherme.macedo/ArmedPeopleDetecter/dataset.yaml'

# Treinamento do modelo
model.train(
    data=data_yaml_path,  # referência ao arquivo YAML
    epochs=5,             
    imgsz=640,            # tamanho das imagens
    batch=16,             
    conf=0.25             # confiança mínima
)
results = model.val()

# Métricas de desempenho
print(f"Precision (P): {results.box.map50:.4f}")
print(f"Recall (R): {results.box.map75:.4f}")
print(f"mAP50 (mean Average Precision @ 0.5 IoU): {results.box.map50:.4f}")
print(f"mAP50-95 (mean Average Precision @ 0.5-0.95 IoU): {results.box.map:.4f}")

predictions = model.predict(source='/Users/guilherme.macedo/ArmedPeopleDetecter/Armed Person Recognition.v13-satexphue.yolov8/test/images', save=True)  # ajuste conforme necessário

def highlight_threats(image_path, detections):
    image = cv2.imread(image_path)
    
    # Itera para desenhar as boxes
    for detection in detections:
        if detection.boxes is not None and len(detection.boxes) > 0:  
            bbox = detection.boxes.xyxy[0].cpu().numpy()
            conf = detection.boxes.conf[0].cpu().numpy()
            cls = detection.boxes.cls[0].cpu().numpy()

            x1, y1, x2, y2 = map(int, bbox)
            color = (0, 0, 255)
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

            label = f'{model.names[int(cls)]}: {conf:.2f}'
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    output_path = os.path.join('output', os.path.basename(image_path))
    cv2.imwrite(output_path, image)

os.makedirs('output', exist_ok=True)

for img_path in os.listdir('/Users/guilherme.macedo/ArmedPeopleDetecter/Rapid dataset/test/images'):
    img_full_path = os.path.join('/Users/guilherme.macedo/ArmedPeopleDetecter/Rapid dataset/test/images', img_path)
    highlight_threats(img_full_path, predictions)

print("Ameaças destacadas e imagens salvas.")
