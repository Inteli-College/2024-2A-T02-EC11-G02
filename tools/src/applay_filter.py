import cv2
import numpy as np
import matplotlib.pyplot as plt
from tools_image import ImageFilters
import os


class FilteringSegmentation(ImageFilters):
    def __init__(self):
        super().__init__()
        self.image = None
        self.mask = None
        self.masked_image = None
        self.R = 2
        self.G = 1
        self.B = 0
        
    def plot_images(self,image, title, position, cmap=None):
        plt.subplot(2, 3, position)
        plt.title(title)
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), cmap=cmap)

    def remuve_background_and_plot(self,image_path):
        # Carregar a imagem
        image = cv2.imread(image_path)

        # Separar os canais R, G, B
        channels = cv2.split(image)

        # Aplicar a máscara à imagem original
        mask = self.get_mask_by_channel(image_path, self.R)
        masked_image = cv2.bitwise_and(image, mask)



        image = np.clip(image, 0, 255).astype(np.uint8)
        # Criar uma figura para plotar as imagens
        plt.figure(figsize=(15, 10))

        # Plotar canais R, G, B em escala de cinza
        self.plot_images(channels[0], "Canal B", 3,"gray")
        self.plot_images(channels[1], "Canal G", 2,"gray")
        self.plot_images(channels[2], "Canal R", 1,"gray")
        self.plot_images(image, "Original", 4,)
        self.plot_images(mask, "mask", 5)
        self.plot_images(masked_image, "Final", 6)
        
        # Mostrar as imagens
        plt.show()

    def save_image(self,image, path):
        cv2.imwrite(path, image)

    def get_mask_by_channel(self,image_path, channel):

        # Carregar a imagem
        image = cv2.imread(image_path)
        
        # Separar os canais R, G, B
        channels = cv2.split(image)

        # Aplicar as transformações no canal R
        image_transform = super().apply_brightness_contrast(channels[channel], 20, 1.5)
        image_transform = super().apply_curves(image_transform, np.array([[0, 0], [105, 92], [146, 247], [255, 255]]))
        image_transform = super().apply_kernal_bluer(image_transform, 5)
        image_transform = super().level_image_numpy(image_transform, 200, 255, 9.9)
        
        # Normalizar a máscara para ter valores entre 0 e 255
        _mask = cv2.normalize(image_transform, None, 0, 255, cv2.NORM_MINMAX)
        #_mask = cv2.merge([_mask, _mask, _mask])
        _mask_inverted = cv2.bitwise_not(_mask)

        return _mask_inverted

    def segment_and_plot(self,image_path):
        image = cv2.imread(image_path)
        image = super().apply_color(image,[ 0, 0, 100 ])
        masked_image = cv2.bitwise_and(image, self.get_mask_by_channel(image_path, self.R))
        plt.figure(figsize=(10, 10))
        plt.imshow(cv2.cvtColor(masked_image, cv2.COLOR_BGR2RGB))
        plt.show()

    def remuve_background(self,image_path):
        image = cv2.imread(image_path)
        target_image = cv2.bitwise_and(image, self.get_mask_by_channel(image_path, self.R))
        return target_image

    def hailht_extractor(self, image_path):
        image = cv2.imread(image_path)
        channels_mean = self.color_density_mean(image)
        channels_mean['blue'] = abs(channels_mean['blue']-255)
        channels_mean['green'] = abs(channels_mean['green']-255)
        channels_mean['red'] = abs(channels_mean['red']-255)
        return channels_mean
        

if __name__ == "__main__":
    pipeline = FilteringSegmentation()
    # for filename in os.listdir("dataset"):
    #     if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
    #         image_path = os.path.join("dataset", filename)
    #         print(f'{filename} _ {pipeline.hailht_extractor(image_path)} \n')
    pipeline.remuve_background_and_plot("dataset/02.png")