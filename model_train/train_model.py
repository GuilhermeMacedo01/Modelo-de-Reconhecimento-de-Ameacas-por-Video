import os
import cv2
import numpy as np
from ultralytics import YOLO
from pathlib import Path

# Configurações
MODEL_PATH = 'yolov8n.pt'
DATA_YAML_PATH = 'C:\\Users\\guilh\\OneDrive\\Área de Trabalho\\Armed-Person-Recognition\\Modelo-de-Reconhecimento-de-Ameacas-por-Video\\dataset.yaml'
TEST_IMAGES_PATH = 'C:\\Users\\guilh\\OneDrive\\Área de Trabalho\\Armed-Person-Recognition\\Modelo-de-Reconhecimento-de-Ameacas-por-Video\\dataset\\test\\images'
OUTPUT_DIR = 'output'

# Cores para diferentes classes
COLORS = {
    'arma': (0, 0, 255),      # Vermelho
    'sem risco': (0, 255, 0),  # Verde
    'pessoa armada': (255, 0, 0)  # Azul
}

def setup_directories():
    """Cria diretórios necessários"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def train_model():
    """Treina o modelo com parâmetros otimizados"""
    model = YOLO(MODEL_PATH)
    
    model.train(
        data=DATA_YAML_PATH,
        epochs=80,
        imgsz=640,
        batch=16,
        conf=0.5,
        iou=0.5,
        patience=15,
        save=True,
        workers=4,
        project='runs/train',
        name='armed_detection',
        exist_ok=True,
        pretrained=True,
        optimizer='SGD',
        lr0=0.01,
        lrf=0.01,
        momentum=0.937,
        weight_decay=0.0005,
        warmup_epochs=2,
        warmup_momentum=0.8,
        warmup_bias_lr=0.1,
        box=7.5,
        cls=0.5,
        dfl=1.5,
        augment=True,
        mosaic=1.0,
        mixup=0.5,
        verbose=True,
        seed=42,
        device='cpu'
    )
    
    return model

def evaluate_model(model):
    """Avalia o modelo e retorna métricas"""
    results = model.val()
    
    metrics = {
        'precision': results.box.map50,
        'recall': results.box.map75,
        'mAP50': results.box.map50,
        'mAP50-95': results.box.map
    }
    
    # Calcula F1-score
    f1 = 2 * (metrics['precision'] * metrics['recall']) / (metrics['precision'] + metrics['recall'])
    metrics['f1_score'] = f1
    
    # Imprime métricas
    for metric, value in metrics.items():
        print(f"{metric.capitalize()}: {value:.4f}")
    
    return metrics

def highlight_threats(image_path, detections, model):
    """Processa e destaca ameaças na imagem"""
    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Erro ao carregar imagem: {image_path}")
            return
        
        # Processa todas as detecções
        for detection in detections:
            if detection.boxes is not None and len(detection.boxes) > 0:
                for box, conf, cls in zip(detection.boxes.xyxy, detection.boxes.conf, detection.boxes.cls):
                    x1, y1, x2, y2 = map(int, box.cpu().numpy())
                    confidence = float(conf.cpu().numpy())
                    class_id = int(cls.cpu().numpy())
                    class_name = model.names[class_id]
                    
                    # Usa cor específica para cada classe
                    color = COLORS.get(class_name, (0, 0, 255))
                    
                    # Desenha bounding box
                    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                    
                    # Adiciona label com confiança
                    label = f'{class_name}: {confidence:.2f}'
                    (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                    cv2.rectangle(image, (x1, y1 - label_height - 10), (x1 + label_width, y1), color, -1)
                    cv2.putText(image, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        # Salva imagem processada
        output_path = os.path.join(OUTPUT_DIR, os.path.basename(image_path))
        cv2.imwrite(output_path, image)
        
    except Exception as e:
        print(f"Erro ao processar imagem {image_path}: {str(e)}")

def main():
    """Função principal"""
    setup_directories()
    
    # Treina o modelo
    print("Iniciando treinamento...")
    model = train_model()
    
    # Avalia o modelo
    print("\nEvaluate...")
    metrics = evaluate_model(model)
    
    #  Predict
    print("\nPredict...")
    predictions = model.predict(source=TEST_IMAGES_PATH, save=True)
    
    print("\nProcessando imagens...")
    for img_path in os.listdir(TEST_IMAGES_PATH):
        if img_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_full_path = os.path.join(TEST_IMAGES_PATH, img_path)
            highlight_threats(img_full_path, predictions, model)
    
    print("\nProcessamento concluído!")

if __name__ == "__main__":
    main()
