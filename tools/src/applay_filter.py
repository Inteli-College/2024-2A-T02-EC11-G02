import cv2
import numpy as np
import matplotlib.pyplot as plt
from tools_image import ImageFilters


tools = ImageFilters()

def plot_images(image, title, position, cmap=None):
    plt.subplot(2, 3, position)
    plt.title(title)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), cmap=cmap)

def remuve_background_and_plot(image_path):
    # Carregar a imagem
    image = cv2.imread(image_path)
    
    # Separar os canais R, G, B
    B, G, R = cv2.split(image)

    # Aplicar a máscara à imagem original
    mask = get_mask(image_path)
    masked_image = cv2.bitwise_and(image, mask)



    image = np.clip(image, 0, 255).astype(np.uint8)
    # Criar uma figura para plotar as imagens
    plt.figure(figsize=(15, 10))

    # Plotar canais R, G, B em escala de cinza
    plot_images(R, "Canal R", 1,"gray")
    plot_images(G, "Canal G", 2,"gray")
    plot_images(B, "Canal B", 3,"gray")
    plot_images(image, "Original", 4,)
    plot_images(mask, "mask", 5)
    plot_images(masked_image, "Final", 6)
    
    # Mostrar as imagens
    plt.show()

def save_image(image, path):
    cv2.imwrite(path, image)

def get_mask(image_path):
    # Carregar a imagem
    image = cv2.imread(image_path)
    
    # Separar os canais R, G, B
    B, G, R = cv2.split(image)

    # Aplicar as transformações no canal R
    R = tools.apply_brightness_contrast(R, 20, 1.5)
    R = tools.apply_curves(R, np.array([[0, 0], [105, 92], [146, 247], [255, 255]]))
    R = tools.apply_kernal_bluer(R, 5)
    R = tools.level_image_numpy(R, 200, 255, 9.9)
    
    # Normalizar a máscara para ter valores entre 0 e 255
    _mask = cv2.normalize(R, None, 0, 255, cv2.NORM_MINMAX)
    #_mask = cv2.merge([_mask, _mask, _mask])
    _mask_inverted = cv2.bitwise_not(_mask)

    return _mask_inverted

def segment_and_plot(image_path):
    image = cv2.imread(image_path)
    image = tools.apply_color(image,[ 0, 0, 100 ])
    masked_image = cv2.bitwise_and(image, get_mask(image_path))
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(masked_image, cv2.COLOR_BGR2RGB))
    plt.show()

def remuve_background(image_path):
    image = cv2.imread(image_path)
    target_image = cv2.bitwise_and(image, get_mask(image_path))
    return target_image




# Exemplo de uso
image_path = f'dataset/02.png'  


# for filename in os.listdir("pasta_de_saida"):
#     if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
#         image_path = os.path.join("pasta_de_saida", filename)
#         save_image(remuve_background(image_path), f"processed_images/masked_{filename}.jpg")
#         print(f"Image {filename} processed")

remuve_background_and_plot(image_path)
#segment_and_plot(image_path)
#plot_images(remuve_background(image_path), "Final", 1)
#plt.show()
