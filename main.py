import importlib

def escolher_detect():
    print("Quando estiver pronto, pressione:")
    print("1 - Detectar camera")
    escolha = input("Digite o número do detector: ")

    detectores = {
        "1": "domains.detecters.webcam_detecter",
    }

    if escolha in detectores:
        modulo = importlib.import_module(detectores[escolha])
        modulo.run()
    else:
        print("Opção inválida!")

if __name__ == "__main__":
    escolher_detect()
