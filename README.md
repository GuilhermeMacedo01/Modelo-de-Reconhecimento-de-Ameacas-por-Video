# Sistema de Detecção de Ameaças por Vídeo

Este projeto implementa um sistema de detecção de ameaças em tempo real utilizando visão computacional e deep learning. O sistema é capaz de identificar potenciais ameaças através da webcam do computador.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Webcam funcional

## 🔧 Instalação

1. Crie e ative o ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

2.  Instale as dependências:

```bash
pip install -r requirements.txt
```

## 🎮 Como Usar

1. Ative o ambiente virtual (se ainda não estiver ativo):

```bash
# Linux/Mac
source venv/bin/activate
```

2. Execute o programa principal:

```bash
python main.py
```

3. Na interface gráfica:
   - Clique em "Iniciar Detecção por Webcam" para começar
   - Use o botão "Sair" para encerrar o programa

## 🛠️ Tecnologias Utilizadas

- Python
- OpenCV
- YOLOv8
- Tkinter
- Ultralytics

## 📝 Notas

- O sistema utiliza o modelo YOLOv8 para detecção
- A primeira execução pode demorar um pouco mais devido ao download do modelo
- Certifique-se de ter boa iluminação para melhor detecção

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
