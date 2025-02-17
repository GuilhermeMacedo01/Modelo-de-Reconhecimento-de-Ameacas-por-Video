from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "runs" / "detect" / "train12" / "weights" / "best.pt"

model = YOLO("/Users/guilherme.macedo/ArmedPeopleDetecter/Modelo-de-Reconhecimento-de-Ameacas-por-Video/runs/detect/train12/weights/best.pt")

# Processa a imagem
def process_image(filepath):
    img = cv2.imread(filepath)
    results = model(img) 

    img_detected = results[0].plot()
    return img_detected

# Abre uma imagem
def open_image():
    filepath = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg;*.png;*.jpeg")])
    if not filepath:
        return

    img_detected = process_image(filepath)
    img_detected = cv2.cvtColor(img_detected, cv2.COLOR_BGR2RGB)
    img_detected = Image.fromarray(img_detected)
    img_detected = img_detected.resize((600, 400))
    img_tk = ImageTk.PhotoImage(img_detected)

    panel.config(image=img_tk)
    panel.image = img_tk

root = tk.Tk()
root.title("Detecção de Ameaças")
root.geometry("700x500")

btn = tk.Button(root, text="Selecionar Imagem", command=open_image)
btn.pack(pady=20)

panel = tk.Label(root)
panel.pack()

root.mainloop()
