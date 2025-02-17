import importlib

def escolher_detect():
    print("Escolha um detector:")
    print("1 - Detectar imagens")
    print("2 - Detectar camera")
    print("3 - Detectar Screenshot")
    escolha = input("Digite o número do detector: ")

    detectores = {
        "1": "domains.detecters.image_detecter",
        "2": "domains.detecters.webcam_detecter",
        "3": "domains.detecters.screenshot_detecter"
    }

    if escolha in detectores:
        modulo = importlib.import_module(detectores[escolha])
        modulo.run()
    else:
        print("Opção inválida!")

if __name__ == "__main__":
    escolher_detect()
