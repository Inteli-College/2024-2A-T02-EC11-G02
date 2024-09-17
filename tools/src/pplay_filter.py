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

    def choice_channel(self, image: cv2.typing.MatLike) -> int:
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
        image_transform = super().pply_brightness_contrast(channels[channel], 40, 1.5)
        image_transform = super().pply_curves(image_transform, np.array([[0, 0], [105, 92], [146, 247], [255, 255]]))
        image_transform = super().pply_kernal_bluer(image_transform, 5)
        image_transform = super().level_image_numpy(image_transform, 200, 255, 9.9)
        
        # Normalizar a máscara para ter valores entre 0 e 255
        _mask = cv2.normalize(image_transform, None, 0, 255, cv2.NORM_MINMAX)
        #_mask = cv2.merge([_mask, _mask, _mask])
        _mask_inverted = cv2.bitwise_not(_mask)

        return _mask_inverted
    
    def get_highlights_by_channel(self,edited_image: cv2.typing.MatLike, channel) -> cv2.typing.MatLike:
       
        channels = cv2.split(edited_image)
        image_transform = super().pply_brightness_contrast(channels[channel], -80, 1.2)
        image_transform = super().pply_curves(image_transform, np.array([[0,0], [58,136], [62, 177], [135, 85], [139, 154]])
)
        image_transform = super().level_image_numpy(image_transform, 33, 52, 1.72)

        return image_transform

    def segment_and_plot(self,image_path):
        image = cv2.imread(image_path)
        image = super().pply_color(image,[ 0, 0, 100 ])
        masked_image = cv2.bitwise_and(image, self.get_mask_by_channel(image_path, self.R))
        plt.figure(figsize=(10, 10))
        plt.imshow(cv2.cvtColor(masked_image, cv2.COLOR_BGR2RGB))
        plt.show()

    def remove_background(self,image: cv2.typing.MatLike) -> cv2.typing.MatLike:
        target_image = cv2.bitwise_and(image, self.get_mask_by_channel(image, self.choice_channel(image)))
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

        masked_image = cv2.bitwise_and(image, self.get_mask_by_channel(image, self.choice_channel(image)))
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

    def trash():
        # cria uma pasta chamada "output" no mesmo diretório
        # os.makedirs('output/tst',exist_ok=True)
        #pipeline.hailht_extractor(teste)
        # image = cv2.imread(teste)
        # pipeline.save_image(pipeline.remove_background(image),'output/tst/01.png')
        # mask_image = pipeline.get_mask_by_channel(image, pipeline.choice_channel(image))
        # pipeline.save_image(mask_image,'output/tst/02.png')
        # hailht = pipeline.get_highlights_by_channel(cv2.bitwise_and(image, mask_image),0)
        # pipeline.save_image(hailht,'output/tst/03.png')
        # pipeline.save_image(pipeline.draw_rectangle(image,hailht),'output/tst/04.png')
        # image_transform = cv2.imread("dataset/train/tst_alpha.png")
        # pipeline.draw_rectangle(_and_plotimage,image_transform)
        #pipeline.choice_channel(image)
        pass


def calcular_circularidade(imagem_caminho):

    imagem = cv2.imread(imagem_caminho)


    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

   
    _, imagem_thresh = cv2.threshold(imagem_cinza, 127, 255, cv2.THRESH_BINARY)

   
    contornos, _ = cv2.findContours(imagem_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    erro = 0




    for i, contorno in enumerate(contornos):

        area = cv2.contourArea(contorno)
        perimetro = cv2.arcLength(contorno, True)

    
        if perimetro > 10:

            circularidade = (4 * np.pi * area) / (perimetro ** 2)

            if circularidade > 0.2 and perimetro > 10:
                print(f"Objeto {i+1}:")
                print(f"  Área: {area:.2f} pixels")
                print(f"  Perímetro: {perimetro:.2f} pixels")
                print(f"  Circularidade: {circularidade:.4f} \n")

    
                cv2.drawContours(imagem, [contorno], -1, (0, 255, 0), 2)
            else:
                erro += 1

    print(f"Total de objetos: {len(contornos) - erro}")

    # Exibir a imagem com contornos
    cv2.imshow('Objetos detectados', imagem)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def iterar_diretorio(diretorio):
    arquivos = os.listdir(diretorio)
    indice = 9
    
    while indice < len(arquivos):
        arquivo_atual = arquivos[indice]
        print(f"Processando arquivo: {arquivo_atual}")
        
        teste = f"dataset/train/{arquivo_atual}"   
        pipeline.remove_background_and_plot(teste)     

        indice += 1


def aplicar_filtro_sobel(imagem_caminho):
    # Carregar a imagem
    imagem = cv2.imread(imagem_caminho)


    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    sobelx = cv2.Sobel(imagem_cinza, cv2.CV_64F, 1, 0, ksize=3)  # Sobel em x
    sobely = cv2.Sobel(imagem_cinza, cv2.CV_64F, 0, 1, ksize=3)  # Sobel em y


    bordas_sobel = cv2.magnitude(sobelx, sobely)


    bordas_sobel = np.uint8(bordas_sobel)


    cv2.imshow('Bordas - Sobel', bordas_sobel)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def plot_histogramas(imagem_caminho):
    # Carregar a imagem
    imagem = cv2.imread(imagem_caminho)
    
    # Converter de BGR (OpenCV usa BGR) para RGB
    imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    
    # Separar os canais de cor: R, G, B
    canais = ('r', 'g', 'b')
    
    # Criar um gráfico com 4 subplots (3 para os canais individuais e 1 para o RGB completo)
    plt.figure(figsize=(10, 7))
    
    # Plotar histogramas para cada canal
    for i, canal in enumerate(canais):
        histograma = cv2.calcHist([imagem_rgb], [i], None, [256], [0, 256])
        plt.subplot(2, 2, i+1)
        plt.plot(histograma, color=canal)
        plt.title(f'Histograma do canal {canal.upper()}')
        plt.xlim([0, 256])
    
    # Plotar o histograma combinado de todos os canais RGB
    plt.subplot(2, 2, 4)
    cores = ('r', 'g', 'b')
    for i, cor in enumerate(cores):
        histograma = cv2.calcHist([imagem_rgb], [i], None, [256], [0, 256])
        plt.plot(histograma, color=cor)
    plt.title('Histograma RGB')
    plt.xlim([0, 256])

    # Exibir o gráfico
    plt.tight_layout()
    plt.show()

def fake_ndvi(image_path):
    # Carregar a imagem
    imagem = cv2.imread(image_path)

    # Separar os canais de cor (G = verde, R = vermelho, B = azul)
    B, G, R = cv2.split(imagem)

    # Calcular o NDVI (normalizado)
    # Adiciona uma pequena constante ao denominador para evitar divisão por zero
    ndvi = (G.astype(float) - R.astype(float)) / (G.astype(float) + R.astype(float) + 1e-5)

    # Normalizar os valores de NDVI para o intervalo [0, 255]
    ndvi_normalizado = cv2.normalize(ndvi, None, 0, 255, cv2.NORM_MINMAX)

    # Converter o NDVI normalizado para formato uint8 (imagem)
    ndvi_normalizado = ndvi_normalizado.astype(np.uint8)

    # Exibir a imagem NDVI
    cv2.imshow('Fake NDVI', ndvi_normalizado)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def to_grayscale(img: np.ndarray):
    R_COEF = 0.2989
    G_COEF = 0.5870
    B_COEF = 0.1140

    # expecting the format of img to be BGR
    b, g, r = img[..., 0], img[..., 1], img[..., 2]
    grayscale_image = B_COEF * b + G_COEF * g + R_COEF * r

    return grayscale_image





if __name__ == "__main__":
    # image to np.array
    img = cv2.imread('dataset/train/03.png')


    img_blur1 = cv2.GaussianBlur(src=to_grayscale(img), ksize=(5, 5), sigmaX=3)

    # plot the image
    plt.imshow(img_blur1, cmap='gray')

    plt.show()



