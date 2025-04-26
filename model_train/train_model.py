import os
import cv2
from ultralytics import YOLO


model = YOLO('yolov8n.pt')
data_yaml_path = '/Users/guilherme.macedo/ArmedPeopleDetecter/dataset.yaml'

# Treinamento do modelo
model.train(
    data=data_yaml_path,      # referência ao arquivo YAML
    epochs=200,               # mais épocas para garantir convergência completa
    imgsz=640,                # tamanho das imagens (mantido pois é ideal para detecção)
    batch=16,                 # batch size reduzido para melhor estabilidade com 3 classes
    conf=0.3,                 # confiança inicial ajustada para o caso de uso
    iou=0.5,                  # IoU threshold mais conservador para detecção precisa
    patience=30,              # early stopping mais agressivo
    save=True,               
    device='0',               # usar GPU se disponível
    workers=4,                # workers reduzidos para evitar problemas de memória
    project='runs/train',     
    name='armed_detection',   
    exist_ok=True,           
    pretrained=True,          
    optimizer='SGD',          # SGD com momentum para melhor generalização
    lr0=0.01,                 # taxa de aprendizado inicial
    lrf=0.01,                 # taxa de aprendizado final
    momentum=0.937,           # momentum para SGD
    weight_decay=0.0005,      # regularização L2
    warmup_epochs=3,          # warmup para estabilidade inicial
    warmup_momentum=0.8,      # momentum durante warmup
    warmup_bias_lr=0.1,       # taxa de aprendizado do bias durante warmup
    box=7.5,                  # peso da loss de bounding box
    cls=0.5,                  # peso da loss de classificação
    dfl=1.5,                  # peso da loss de distribuição
    verbose=True,             # mostrar progresso detalhado
    seed=42                   # seed para reprodutibilidade
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
