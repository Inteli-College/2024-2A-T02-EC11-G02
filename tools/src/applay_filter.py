import cv2
import numpy as np
import scipy.ndimage as ndi
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
        plt.subplot(1, 1, position)
        plt.title(title)
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), cmap=cmap)

    def remuve_background_and_plot(self,image_path):
        # Carregar a imagem
        image = cv2.imread(image_path)

        # Separar os canais R, G, B
        channels = cv2.split(image)

        # Aplicar a máscara à imagem original
        mask = self.get_mask_by_channel(image_path, self.B)
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
        image_transform = super().apply_brightness_contrast(channels[channel], 40, 1.5)
        image_transform = super().apply_curves(image_transform, np.array([[0, 0], [105, 92], [146, 247], [255, 255]]))
        image_transform = super().apply_kernal_bluer(image_transform, 5)
        image_transform = super().level_image_numpy(image_transform, 200, 255, 9.9)
        
        # Normalizar a máscara para ter valores entre 0 e 255
        _mask = cv2.normalize(image_transform, None, 0, 255, cv2.NORM_MINMAX)
        #_mask = cv2.merge([_mask, _mask, _mask])
        _mask_inverted = cv2.bitwise_not(_mask)

        return _mask_inverted
    
    def get_height_by_channel(self,edited_image, channel, normal_image):
       
        channels = cv2.split(edited_image)
        image_transform = super().apply_brightness_contrast(channels[channel], -80, 1.2)
        image_transform = super().apply_curves(image_transform, np.array([[0,0], [58,136], [62, 177], [135, 85], [139, 154]])
)
        image_transform = super().level_image_numpy(image_transform, 33, 52, 1.72)

        if len(image_transform.shape) == 3:
            image_transform = cv2.cvtColor(image_transform, cv2.COLOR_BGR2GRAY)


        print(f'shape: {image_transform.shape}')
        labeled_array, num_features = ndi.label(image_transform, structure=np.ones((3, 3)))  # Conectividade de 8 vizinhos
        
        print(f'Número de componentes conectados: {num_features}')
        
        # Criar imagem colorida para desenhar quadrados nos segmentos
        image_with_boxes = cv2.cvtColor(image_transform, cv2.COLOR_GRAY2BGR)
        
        # Encontrar os limites de cada segmento
        for label in range(1, num_features + 1):
            # Achar os pixels que pertencem ao segmento
            segment_mask = (labeled_array == label).astype(np.uint8)
            
            # Encontrar os contornos do segmento
            contours, _ = cv2.findContours(segment_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Para cada contorno, desenhar um retângulo em torno do segmento
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(normal_image, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Desenhar quadrado vermelho
        
        # Mostrar a imagem original com os quadrados vermelhos
        self.plot_images(normal_image, f"Numero de segmentos encontrados {num_features}", 1, "gray")
        plt.show()


        return "image_transform"

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

        # Analisar a densidade de cor da imagem por canal para pegar o que há mais brilho.
        channels_mean = self.color_density_mean(image)
        channels_mean['blue'] = 255 - channels_mean['blue']
        channels_mean['green'] = 255 - channels_mean['green']
        channels_mean['red'] = 255 - channels_mean['red']
        channel_hailht = min(channels_mean)

        # 
        channels = {
            'blue': self.B,
            'green': self.G,
            'red': self.R
        }
        channels[channel_hailht]
        masked_image = cv2.bitwise_and(image, self.get_mask_by_channel(image_path, self.B))
        hailhts = self.get_height_by_channel(masked_image, channels[channel_hailht], image)

        return channels_mean
        

if __name__ == "__main__":
    pipeline = FilteringSegmentation()
    # for filename in os.listdir("dataset"):
    #     if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
    #         image_path = os.path.join("dataset", filename)
    #         print(f'{filename} _ {pipeline.hailht_extractor(image_path)} \n')
    #pipeline.remuve_background_and_plot("dataset/test/Screenshot-2024-03-18-at-10-26-14-PM_png.rf.6038092fa420596b01e462125dfdf0c0.jpg")
    pipeline.hailht_extractor("dataset/train/06.png")


