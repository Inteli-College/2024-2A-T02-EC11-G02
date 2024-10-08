import numpy as np
import matplotlib.pyplot as plt
import cv2

# Converte de RGB para HSV usando OpenCV
def rgb_to_hsv_array(rgb_array):
    # Convertendo para o formato correto para OpenCV (de [0, 255])
    rgb_array = rgb_array.astype(np.uint8)
    # Convertendo de RGB para HSV
    hsv_array = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2HSV)
    return hsv_array

# Converte de HSV para RGB usando OpenCV
def hsv_to_rgb_array(hsv_array):
    # Convertendo de HSV para RGB
    rgb_array = cv2.cvtColor(hsv_array, cv2.COLOR_HSV2RGB)
    return rgb_array

def level_image_numpy(image_np, minv=0, maxv=255, gamma=1.0):
    # Verifica se a imagem é grayscale e converte para RGB se necessário
    if len(image_np.shape) == 2:  # Imagem grayscale
        image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
    
    # Convertendo imagem para float32
    np_image = image_np.astype(np.float32)
    
    # Converte para HSV
    hsv_image = rgb_to_hsv_array(np_image)
    
    # Aplica o ajuste no canal V
    v = hsv_image[..., 2] / 255.0  # Normaliza o canal V para [0, 1]
    v = np.clip((v - minv / 255.0) / ((maxv - minv) / 255.0), 0, 1)
    v = np.power(v, 1.0 / gamma)
    
    # Reconstroi a imagem HSV ajustando o canal V
    hsv_image[..., 2] = (v * 255).astype(np.uint8)  # Desnormaliza o canal V para [0, 255]
    
    # Converte de volta para RGB
    rgb_image = hsv_to_rgb_array(hsv_image)
    
    return rgb_image

def main():
    # Exemplo de uso
    image = cv2.imread('dataset/test/01_test.png')  # Lê a imagem no formato BGR
    imagem_cinza = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Converte para grayscale
    adjusted_image = level_image_numpy(imagem_cinza, minv=55, maxv=150, gamma=10)

    # Exibe a imagem original e a ajustada
    plt.figure(figsize=(10, 5))

    # Exibir imagem original
    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # Converte BGR para RGB para exibir corretamente

    # Exibir imagem ajustada
    plt.subplot(1, 2, 2)
    plt.title("Ajustada")
    plt.imshow(adjusted_image)

    plt.show()

if __name__ == '__main__':
    main()
