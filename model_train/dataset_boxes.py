import cv2
import os
from glob import glob

images_dir = 'dataset/valid/images'  
labels_dir = 'dataset/valid/labels'  
output_dir = 'output/valid' 

class_names = ['arma', 'sem risco', 'pessoa armada']

os.makedirs(output_dir, exist_ok=True)

label_files = glob(os.path.join(labels_dir, '*.txt'))

for label_file in label_files:

    base_name = os.path.splitext(os.path.basename(label_file))[0]
    image_path = os.path.join(images_dir, f"{base_name}.jpg")

    image = cv2.imread(image_path)
    if image is None:
        print(f"Erro ao carregar a imagem: {image_path}")
        continue

    height, width, _ = image.shape

    with open(label_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        parts = line.strip().split()
        label = int(parts[0])
        x_center = float(parts[1])
        y_center = float(parts[2])
        box_width = float(parts[3])
        box_height = float(parts[4])

        xmin = int((x_center - box_width / 2) * width)
        ymin = int((y_center - box_height / 2) * height)
        xmax = int((x_center + box_width / 2) * width)
        ymax = int((y_center + box_height / 2) * height)

        class_name = class_names[label]

        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        cv2.putText(image, class_name, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    output_path = os.path.join(output_dir, f"{base_name}.jpg")
    cv2.imwrite(output_path, image)
    print(f"Imagem salva: {output_path}")