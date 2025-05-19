import tkinter as tk
from tkinter import ttk
import importlib
from PIL import Image, ImageTk
import cv2

class DetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector de Ameaças")
        self.root.geometry("800x600")
        
        # Configurar estilo
        style = ttk.Style()
        style.configure("TButton", padding=10, font=('Helvetica', 12))
        style.configure("TLabel", font=('Helvetica', 12))
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Sistema de Detecção de Ameaças", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Botão de detecção
        self.detect_button = ttk.Button(
            main_frame,
            text="Iniciar Detecção",
            command=self.iniciar_deteccao,
            style="TButton"
        )
        self.detect_button.pack(pady=20)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Status: Aguardando início da detecção")
        self.status_label.pack(pady=10)
        
        # Frame para preview da webcam
        self.preview_frame = ttk.Frame(main_frame)
        self.preview_frame.pack(pady=20)
        
        self.preview_label = ttk.Label(self.preview_frame)
        self.preview_label.pack()
        
        # Botão de sair
        exit_button = ttk.Button(
            main_frame,
            text="Sair",
            command=root.quit,
            style="TButton"
        )
        exit_button.pack(pady=20)

    def iniciar_deteccao(self):
        self.status_label.config(text="Status: Iniciando detecção...")
        self.detect_button.config(state='disabled')
        
        try:
            modulo = importlib.import_module("domains.detecters.webcam_detecter")
            modulo.run()
        except Exception as e:
            self.status_label.config(text=f"Erro: {str(e)}")
        finally:
            self.detect_button.config(state='normal')
            self.status_label.config(text="Status: Aguardando início da detecção")

def main():
    root = tk.Tk()
    app = DetectorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
