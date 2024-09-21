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
        self.rgb = [
            'blue',
            'green',
            'red'
        ]

    def choice_channel(self, image) -> int:
        B, G, R = cv2.split(image)

        trashold = 40

        B = B < trashold
        G = G < trashold
        R = R < trashold

        #print(f'Blue: {np.sum(B)} \n Green: {np.sum(G)} \n Red: {np.sum(R)}')

        choice = np.argmax([np.sum(B), np.sum(G), np.sum(R)])

        return choice

    def plot_images(self,image: cv2.typing.MatLike, title, position, cmap=None, nrows=2, ncols=3):
        plt.subplot(nrows, ncols, position)
        plt.title(title)
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), cmap=cmap)

    def remove_background_and_plot(self,image_path):
        # Carregar a imagem
        image = cv2.imread(image_path)
        choice = self.choice_channel(image)


        # Separar os canais R, G, B
        channels = cv2.split(image)

        
        # Aplicar a máscara à imagem original
        mask = self.get_mask_by_channel(image, choice)
        masked_image = cv2.bitwise_and(image, mask)
        mask_1 = self.get_texture_mask(masked_image, 1, 100)
        mask_1 = cv2.bitwise_and(masked_image, mask_1)



        image = np.clip(image, 0, 255).astype(np.uint8)
        # Criar uma figura para plotar as imagens
        plt.figure(figsize=(15, 10))

        # Plotar canais R, G, B em escala de cinza
        self.plot_images(channels[0], "Canal B", 3,"gray")
        self.plot_images(channels[1], "Canal G", 2,"gray")
        self.plot_images(channels[2], "Canal R", 1,"gray")
        self.plot_images(image, "Original", 4,)
        self.plot_images(mask, f"mask - {self.rgb[choice]}", 5)
        self.plot_images(mask_1, "Final", 6)
        
        # Mostrar as imagens
        plt.show()

    def save_image(self,image: cv2.typing.MatLike, path):
        cv2.imwrite(path, image)

    def get_mask_by_channel(self,image: cv2.typing.MatLike, channel) -> cv2.typing.MatLike:
        
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
    
    def get_highlights_by_channel(self,edited_image: cv2.typing.MatLike, channel) -> cv2.typing.MatLike:
       
        channels = cv2.split(edited_image)
        image_transform = super().apply_brightness_contrast(channels[channel], -80, 1.2)
        image_transform = super().apply_curves(image_transform, np.array([[0,0], [58,136], [62, 177], [135, 85], [139, 154]])
)
        image_transform = super().level_image_numpy(image_transform, 33, 52, 1.72)

        return image_transform

    def segment_and_plot(self,image_path):
        image = cv2.imread(image_path)
        image = super().apply_color(image,[ 0, 0, 100 ])
        masked_image = cv2.bitwise_and(image, (self.get_mask_by_channel(image, self.B)))
        plt.figure(figsize=(10, 10))
        plt.imshow(cv2.cvtColor(masked_image, cv2.COLOR_BGR2RGB))
        plt.show()

    def remove_background(self,image: cv2.typing.MatLike) -> cv2.typing.MatLike:
        target_image = cv2.bitwise_and(image, (self.get_mask_by_channel(image, self.choice_channel(image))))
        return target_image

    def hailht_extractor(self, image_path: str) -> dict: # Anasilzar com mais calma
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

        masked_image = cv2.bitwise_and(image, (self.get_mask_by_channel(image, self.choice_channel(image))))
        hailhts = self.get_highlights_by_channel(masked_image, channels[channel_hailht])
        self.draw_rectangle_and_plot(image,hailhts)

        return channels_mean
        
    def draw_rectangle_and_plot(self,normal_image: cv2.typing.MatLike, image_transform: cv2.typing.MatLike):
        if len(image_transform.shape) == 3:
            image_transform = cv2.cvtColor(image_transform, cv2.COLOR_BGR2GRAY)


        print(f'shape: {image_transform.shape}')
        labeled_array, num_features = ndi.label(image_transform, structure=np.ones((3, 3)))
        
        print(f'Número de componentes conectados: {num_features}')
        
        # Encontrar os limites de cada segmento
        for label in range(1, num_features + 1):
            # Achar os pixels que pertencem ao segmento
            segment_mask = (labeled_array == label).astype(np.uint8)
            
            # Encontrar os contornos do segmento
            contours, _ = cv2.findContours(segment_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Para cada contorno, desenhar um retângulo em torno do segmento
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(normal_image, (x, y), (x + w, y + h), (0, 0, 255), 1)  # ! Restringir por area minima e maxima !
                

        
        # Mostrar a imagem original com os quadrados vermelhos
        self.plot_images(normal_image, f"Numero de segmentos encontrados {num_features}", 1, "gray", 2, 1)
        self.plot_images(image_transform, f"Numero de segmentos encontrados", 2, "gray", 2, 1)
        plt.show()

    def draw_rectangle(self,normal_image: cv2.typing.MatLike, image_transform: cv2.typing.MatLike):
            if len(image_transform.shape) == 3:
                image_transform = cv2.cvtColor(image_transform, cv2.COLOR_BGR2GRAY)


            print(f'shape: {image_transform.shape}')
            labeled_array, num_features = ndi.label(image_transform, structure=np.ones((3, 3)))
            
            print(f'Número de componentes conectados: {num_features}')
            
            # Encontrar os limites de cada segmento
            for label in range(1, num_features + 1):
                # Achar os pixels que pertencem ao segmento
                segment_mask = (labeled_array == label).astype(np.uint8)
                
                # Encontrar os contornos do segmento
                contours, _ = cv2.findContours(segment_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                # Para cada contorno, desenhar um retângulo em torno do segmento
                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(normal_image, (x, y), (x + w, y + h), (0, 0, 255), 1)  # ! Restringir por area minima e maxima !
            return normal_image

    def get_texture_mask(self, image: cv2.typing.MatLike, kernel_size=3, threshold_value=100) -> cv2.typing.MatLike:
        """
        Gera uma máscara binária a partir de uma imagem, aplicando um filtro de suavização 
        e usando o gradiente de magnitude.
        
        Parâmetros:
            image (cv2 image): imagem.
            kernel_size (int): Tamanho do kernel para o filtro de suavização (default: 9).
            threshold_value (int): Valor de limiar para a geração da máscara (default: 100).
        
        Retorna:
            mask (numpy array): Máscara binária gerada a partir da imagem suavizada.
        """
        
        # Calcular gradiente (derivada) da imagem
        sobel_x = ndi.sobel(image, axis=0)
        sobel_y = ndi.sobel(image, axis=1)
        magnitude = np.hypot(sobel_x, sobel_y)

        # Normalizar a magnitude para o intervalo [0, 255] e converter para uint8
        magnitude = np.uint8(255 * (magnitude / np.max(magnitude)))

        # Criar um kernel nxn onde todos os valores são 1/(kernel_size^2)
        kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size)

        # Aplicar o filtro de média
        smoothed_image = cv2.filter2D(magnitude, -1, kernel)

        # Aplicar um limiar (threshold) para criar uma máscara binária
        _, mask = cv2.threshold(smoothed_image, threshold_value, 255, cv2.THRESH_BINARY)

        return mask

    def segment_image(self,image_path: str) -> cv2.typing.MatLike:
        image = cv2.imread(image_path)
        choice = self.choice_channel(image)
        masked_image = cv2.bitwise_and(image, (self.get_mask_by_channel(image, choice)))
        highlights = self.get_highlights_by_channel(masked_image, self.G)
        image_segmented = self.draw_rectangle(image,highlights)
        return image_segmented


if __name__ == '__main__':
    image_path = 'dataset/train/04.png'
    filter_segmentation = FilteringSegmentation()
    filter_segmentation.remove_background_and_plot(image_path)
    image = cv2.imread(image_path)
    #filter_segmentation.segment_and_plot(image_path)
    filter_segmentation.hailht_extractor(image_path)

    # masked_image = cv2.bitwise_and(image, (filter_segmentation.get_mask_by_channel(image, filter_segmentation.choice_channel(image))))
    # hailhts = filter_segmentation.get_highlights_by_channel(masked_image, 2)
    # filter_segmentation.plot_images(hailhts, "Hailhts", 1, "gray", 2, 1)
    # plt.show()

    # image_segmented = filter_segmentation.segment_image(image_path)
    # filter_segmentation.save_image(image_segmented, 'dataset/train/maira.png')