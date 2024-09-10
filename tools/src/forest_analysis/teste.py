import cv2
import numpy as np
import scipy.ndimage as ndi
import matplotlib.pyplot as plt


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


def plot_images(self,image, title, position, cmap=None, nrows=2, ncols=3):
    plt.subplot(nrows, ncols, position)
    plt.title(title)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), cmap=cmap)


def get_mask_by_channel(self,image_path, channel):

    # Carregar a imagem
    image = cv2.imread(image_path)
    
    # Separar os canais R, G, B
    channels = cv2.split(image)

    # Aplicar as transformações no canal R
    image_transform = super().apply_brightness_contrast(channels[channel], 40, 1.5)
    image_transform = super().apply_curves(image_transform, np.array([[0, 0], [105, 92], [146, 247], [255, 255]]))
    image_transform = super().apply_kernal_bluer(image_transform, 5)
    image_transform = super().level_image_numpy(image_transform, 200, 255, 9.9)
    
    # Normalizar a máscara para ter valores entre 0 e 255
    _mask = cv2.normalize(image_transform, None, 0, 255, cv2.NORM_MINMAX)
    #_mask = cv2.merge([_mask, _mask, _mask])
    _mask_inverted = cv2.bitwise_not(_mask)

    return _mask_inverted



def main():
    pass


if __name__ == '__main__':
    pass