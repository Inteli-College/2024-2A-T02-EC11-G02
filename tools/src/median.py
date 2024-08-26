import cv2
import numpy as np
import matplotlib.pyplot as plt
from processed_image import ImageFilters

tools = ImageFilters()


def plot_images(image, title, position):
    plt.subplot(2, 3, position)
    plt.title(title)
    plt.imshow(image, cmap='gray')
    plt.axis('off')

def combined_rgb_and_edge_detection(image_path):
    # Carregar a imagem
    image = cv2.imread(image_path)
    
    # Separar os canais R, G, B
    B, G, R = cv2.split(image)

    R = tools.apply_brightness_contrast(R, 20, 1.5)
    R = tools.apply_curves(R, np.array([[0, 0], [105, 92], [146, 247], [146, 247], [255, 255], [255, 255], [255, 255]]))
    R = tools.apply_curves(R, np.array([[0, 0], [105, 92], [146, 247], [146, 247], [255, 255], [255, 255], [255, 255]]))
    R = tools.apply_kernal_bluer(R, 5)


    
    
    # Criar uma figura para plotar as imagens
    plt.figure(figsize=(15, 10))
    
    # Plotar canais R, G, B em escala de cinza
    plot_images(R, "Canal R", 1)
    plot_images(G, "Canal G", 2)
    plot_images(B, "Canal B", 3)
    plot_images(image, "Original", 4)
    
    
    # Mostrar as imagens
    plt.show()

# Exemplo de uso
image_path = 'dataset/04.png'  # Insira o caminho correto para sua imagem
combined_rgb_and_edge_detection(image_path)
