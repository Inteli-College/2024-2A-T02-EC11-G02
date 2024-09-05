import cv2
import numpy as np
import matplotlib.pyplot as plt


# Precisa de ajustes ainda

def adjust_levels(image, in_black, in_white, gamma, out_black, out_white):
    # Passo 1: Normalizar e mapear valores de entrada
    image_normalized = np.clip((image - in_black) / (in_white - in_black), 0, 1)

    # Passo 2: Aplicar correção de gama
    image_gamma_corrected = image_normalized ** gamma

    # Passo 3: Mapear para os níveis de saída
    image_output = image_gamma_corrected * (out_white - out_black) + out_black
    
    # Garantir que os valores estão dentro do intervalo [0, 255]
    return np.clip(image_output, 0, 255).astype(np.uint8)

# Carregar a imagem
image = cv2.imread('dataset/02.png')

# Verificar se a imagem foi carregada corretamente
if image is None:
    print("Erro: Não foi possível carregar a imagem. Verifique o caminho e tente novamente.")
else:
    # Convertendo para escala de cinza
    imagem_cinza = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    adjusted_image = adjust_levels(imagem_cinza, 0, 255, 1, 0, 255)

    # Exibe a imagem original e a ajustada
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.subplot(1, 2, 2)
    plt.title("Ajustada")
    plt.imshow(adjusted_image, cmap='gray')
    plt.show()
