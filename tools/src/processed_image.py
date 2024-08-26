import cv2
import numpy as np
import matplotlib.pyplot as plt

class ImageFilters:
    def __init__(self):
        pass

    def apply_curves(self,image, curve_points):
        # Cria uma curva de interpolação linear a partir dos pontos fornecidos
        curve = np.interp(np.arange(256), curve_points[:, 0], curve_points[:, 1]).astype(np.uint8)
        
        # Aplica a curva a cada canal da imagem
        if len(image.shape) == 2:  # Imagem em escala de cinza
            image_adjusted = cv2.LUT(image, curve)
        else:  # Imagem colorida
            channels = cv2.split(image)  # Divide os canais B, G, R
            channels_adjusted = [cv2.LUT(channel, curve) for channel in channels]
            image_adjusted = cv2.merge(channels_adjusted)  # Mescla os canais de volta

        return image_adjusted

    def apply_color(self,image, rgb_filter):
        out = np.zeros_like(image)
        
        out[:, :, 0] = image[:, :, 0]  + rgb_filter[0] # R
        out[:, :, 1] = image[:, :, 1]  + rgb_filter[1] # G
        out[:, :, 2] = image[:, :, 2]  + rgb_filter[2] # B
        return out

    def apply_levels(image, levels):
        return 
    
    def apply_brightness_contrast(self,image, brightness, contrast):
        image = image.astype(np.float32)
        image = image * contrast + brightness
        image = np.clip(image, 0, 255).astype(np.uint8)
        return image
    
    def apply_kernal_bluer(self,image,kernal_size):
        return cv2.blur(image,(kernal_size,kernal_size))


def main():
        
    a = ImageFilters()

    image = cv2.imread('dataset/04.png')  # Carrega a imagem


    # Aplica as funçãos para ajustar a imagem
    rgb_filter = [120,60,0]
    curve_points = np.array([[0, 0], [105, 92], [146, 247], [146, 247], [255, 255], [255, 255], [255, 255]])

    image_adjusted_color = a.apply_color(image, rgb_filter)
    imagem_cinza = cv2.cvtColor(image_adjusted_color, cv2.COLOR_BGR2GRAY)
    image_adjusted_curves = a.apply_curves(image, curve_points)


    # Ajusta os valores para o intervalo de 0 a 255 e converte para uint8
    image_adjusted = np.clip(image_adjusted_curves, 0, 255).astype(np.uint8)


    # Exibe a imagem original e a ajustada
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.subplot(1, 2, 2)
    plt.title("Ajustada")
    plt.imshow(cv2.cvtColor(image_adjusted, cv2.COLOR_BGR2RGB))
    plt.show()

if __name__ == '__main__':
    ImgFilters = ImageFilters()

    image = cv2.imread('dataset/04.png')  # Carrega a imagem
    img = ImgFilters.apply_brightness_contrast(image, 100, 1.5)
    
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.subplot(1, 2, 2)
    plt.title("Ajustada")
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()