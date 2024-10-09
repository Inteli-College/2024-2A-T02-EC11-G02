import cv2
import numpy as np
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
from routers.tools.image_filters import ImageFilters
from routers.tools.model_count_tree import count_trees_with_adjustments



class FilteringSegmentation(ImageFilters):
    def __init__(self):
        super().__init__()
        self.image = None
        self.mask = None
        self.masked_image = None
        self.counted = 0
        self.model_version = None
        self.R = 2
        self.G = 1
        self.B = 0
        self.rgb = [
            'blue',
            'green',
            'red'
        ]

    def get_brightness(self,imagem: cv2.typing.MatLike) -> float:
        
        # Se a imagem estiver colorida, converta para escala de cinza
        if len(imagem.shape) == 3:
            img = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        else:
            img = imagem
        # Calcular a média da intensidade de cada pixel
        media = np.mean(img)

        y = 15435/89 - 95*media/89

        return y + 120
    
    def get_highlights(self,imagem: cv2.typing.MatLike) -> float:
            
            # Se a imagem estiver colorida, converta para escala de cinza
            if len(imagem.shape) == 3:
                img = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            else:
                img = imagem
            # Calcular a média da intensidade de cada pixel
            media = np.mean(img)

            y = 15435/89 - 95*media/89

            return y + 200
        
    def choice_channel(self, image) -> int:
        B, G, R = cv2.split(image)

        trashold = 40

        B = B < trashold
        G = G < trashold
        R = R < trashold

        #print(f'Blue: {np.sum(B)} \n Green: {np.sum(G)} \n Red: {np.sum(R)}')

        choice = np.argmax([np.sum(B), np.sum(G), np.sum(R)])

        return choice
    
    def choice_highlights_channel(self, image) -> int:
        B, G, R = cv2.split(image)

        trashold = 120

        B = B > trashold
        G = G > trashold
        R = R > trashold

        print(f'Blue: {np.sum(B)} \n Green: {np.sum(G)} \n Red: {np.sum(R)}')

        choice = np.argmax([np.sum(B), np.sum(G), np.sum(R)])

        return choice

    def plot_images(self, image: cv2.typing.MatLike, title, position, cmap=None, nrows=2, ncols=3):
        plt.subplot(nrows, ncols, position)
        plt.title(title)

        # Verificar se a imagem é 2D ou 3D
        if len(image.shape) == 2:
            # Imagem em escala de cinza ou binária (1 canal)
            if cmap is None:
                cmap = 'gray'  # Define cmap como 'gray' para imagens 2D
            plt.imshow(image, cmap=cmap)
        elif len(image.shape) == 3:
            if image.shape[2] == 3:
                # Imagem com 3 canais (BGR), converter para RGB
                plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), cmap=cmap)
            elif image.shape[2] == 4:
                # Imagem com 4 canais (BGRA), converter para RGBA
                plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA), cmap=cmap)
            else:
                raise ValueError("Formato de imagem inesperado")
        else:
            raise ValueError("Formato de imagem inesperado")

        plt.show()

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
        plt.show()

    def save_image(self,image: cv2.typing.MatLike, path):
        cv2.imwrite(path, image)

    def get_mask_by_channel(self, image: cv2.typing.MatLike, channel) -> cv2.typing.MatLike:
        brightness_value = self.get_brightness(image)
        print(f'Brightness: {brightness_value}')

        # Separar os canais R, G, B
        channels = cv2.split(image)

        image_transform = super().apply_brightness_contrast(channels[channel], brightness_value, 1.2)
        image_transform = super().apply_curves(image_transform, np.array([[0, 0], [105, 92], [146, 247], [255, 255]]))
        image_transform = super().apply_kernal_bluer(image_transform, 5)
        image_transform = super().level_image_numpy(image_transform, 150, 255, 9.9)

        _mask = cv2.normalize(image_transform, None, 0, 255, cv2.NORM_MINMAX)

        if _mask.shape[2] == 3:
            _mask = cv2.cvtColor(_mask, cv2.COLOR_BGR2GRAY)

       # Converter a máscara para um formato binário (0 e 255)
        _, binary_mask = cv2.threshold(_mask, 40, 255, cv2.THRESH_BINARY)

        return binary_mask  
        
    def get_highlights_by_channel(self, edited_image: cv2.typing.MatLike, channel, debug:bool = False) -> cv2.typing.MatLike:
        # Validação do canal selecionado
        if channel < 0 or channel > 2:
            raise ValueError("O canal deve ser 0 (B), 1 (G) ou 2 (R).")

        # Separar os canais RGB e o canal alfa
        bgr, alpha = edited_image[:, :, :3], edited_image[:, :, 3]

        # Normaliza o canal alfa (valores entre 0 e 1)
        alpha_normalizado = alpha.astype(float) / 255.0

        self.mask = alpha_normalizado

        # Aplica o canal alfa aos canais RGB
        image_rgb_mascarado = bgr * alpha_normalizado[:, :, None]

        # Converte o resultado de volta para uint8
        image_rgb_mascarado = image_rgb_mascarado.astype(np.uint8)

        # Divide a imagem mascarada em seus canais BGR
        channels = cv2.split(image_rgb_mascarado)

        # Converte o canal escolhido de cinza para BGR para exibição
        channel_choiced = cv2.cvtColor(channels[channel], cv2.COLOR_GRAY2BGR)

        #invertendo a imagem
        #channel_choiced = cv2.bitwise_not(channel_choiced)

        # Plota o canal escolhido após a aplicação da máscara alfa
        if debug == True:
             self.plot_images(channel_choiced, f"[ Inicio Pepi 2 ] Inversa do canal {self.rgb[channel]}", 1, ncols=1, nrows=1)


        #print(self.get_highlights(channel_choiced))

        curve_points = np.array([[0, 0], [72, 72], [84, 247], [255, 255], [255, 255], [255, 255], [255, 255]])
        image_transform = super().apply_curves(channel_choiced, curve_points)
        image_transform = super().level_image_numpy(image_transform, 60, 255, 1.86)
        
        
        # Plota a imagem após aplicação dos filtros
        if debug == True:
             self.plot_images(image_transform, f"Segunda Máscara Após Filtros", 1, ncols=1, nrows=1)


        # Aplica limiarização para criar a máscara binária
        _, binary_mask = cv2.threshold(image_transform, 120, 255, cv2.THRESH_BINARY)

        # Plota a máscara binária
        if debug == True:
             self.plot_images(binary_mask, f"Máscara Binária", 1, ncols=1, nrows=1)

        # Inverte a máscara binária [ Vesão 1 ] -> Somente na versão 1
        # mask_inverted = cv2.bitwise_not(binary_mask)

        # Plota a máscara invertida
        # if debug == True:
        #      self.plot_images(mask_inverted, f"Máscara Invertida", 1, ncols=1, nrows=1)

        # Normalizar o canal alpha para o intervalo de 0 a 1
        alpha_normalized = alpha.astype(np.float32) / 255.0

        # Expandir as dimensões do canal alpha para que ele tenha 3 canais
        alpha_expanded = np.stack((alpha_normalized,) * 3, axis=-1)  # Repetindo ao longo do eixo de canais
    
        # Aplicar a máscara multiplicando a imagem em escala de cinza pelo canal alpha
        result_image = binary_mask[:, :, :] * alpha_expanded

        if debug == True:
             self.plot_images(result_image, f"Máscara Cortada", 1, ncols=1, nrows=1)        

        # Verifica o formato da máscara gerada
        print(f"Mask_high shape: {binary_mask.shape}")

        # --------------------------------- [ Vesão 1 ] ----------------------------------------- #
        # image_transform = super().level_image_numpy(channel_choiced, 0, 28, 0.37)
        # image_transform = super().level_image_numpy(image_transform, 0, 28, 0.37)
        # -------------------------------------------------------------------------------------- #


        return result_image

    def segment_and_plot(self,image_path):
        image = cv2.imread(image_path)
        image = super().apply_color(image,[ 0, 0, 100 ])
        masked_image = cv2.bitwise_and(image, (self.get_mask_by_channel(image, self.G)))
        plt.figure(figsize=(10, 10))
        plt.imshow(cv2.cvtColor(masked_image, cv2.COLOR_BGR2RGB))
        plt.show()

    def remove_background(self, image: cv2.typing.MatLike, debug:bool = False) -> cv2.typing.MatLike:
        # Obter a máscara pelo canal selecionado
        mask = self.get_mask_by_channel(image, self.choice_channel(image))

        if debug == True:
             self.plot_images(mask,"Primeira Máscara", 1, ncols=1, nrows=1)

        #print(f"Mask shape : {mask.shape}")
        
        # Inverter a máscara para que o fundo seja 0 e o objeto 255
        mask_inverted = cv2.bitwise_not(mask)

        if debug == True:
             self.plot_images(mask_inverted,"Inversa Primeira Máscara", 1, ncols=1, nrows=1)

        # Separar os canais da imagem original e garantir que estão no formato correto
        b, g, r = cv2.split(image)
        
        # Garantir que todos os canais estejam em formato 8-bit
        b = b.astype(np.uint8)
        g = g.astype(np.uint8)
        r = r.astype(np.uint8)

        # Criar a imagem RGBA com a máscara como canal alfa
        rgba = cv2.merge([b, g, r, mask_inverted])

        
        if debug == True:
             self.plot_images(rgba,"Primeira Máscara Aplicada", 1, ncols=1, nrows=1)

        return rgba

    def hailht_extractor(self, image_path: str):
        image = cv2.imread(image_path)
        masked_image = cv2.bitwise_and(image, (self.get_mask_by_channel(image, self.choice_channel(image))))
        choice = self.choice_channel(masked_image)
        print(f"Mask channel: {choice}")
        hailhts = self.get_highlights_by_channel(masked_image, choice)
        self.draw_rectangle_and_plot(image,hailhts)
        return
        
    def draw_rectangle_and_plot(self,normal_path: str, transform_path: str):
        normal_image =  cv2.imread(normal_path)
        image_transform =  cv2.imread(transform_path)
        
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

    def draw_rectangle(self, normal_image: cv2.typing.MatLike, image_transform: cv2.typing.MatLike, min_area: float = 12.0):
        if len(image_transform.shape) == 3:
            image_transform = cv2.cvtColor(image_transform, cv2.COLOR_BGR2GRAY)

        counted, normal_image = count_trees_with_adjustments(image_transform, normal_image, min_area)
        self.counted = counted
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
    
    async def segment_image(self,image: cv2.typing.MatLike, debug:bool = False) -> cv2.typing.MatLike:
        masked_image = self.remove_background(image, debug)
        highlights = self.get_highlights_by_channel(masked_image, self.B, debug)
        self.masked_image = await self.image_colorizer(image)
        image_segmented = self.draw_rectangle(image,highlights)
        return image_segmented

    async def image_colorizer(self, image:cv2.typing.MatLike) -> cv2.typing.MatLike: # Ser assyncrono
        # Verificar se é um array ou se estar vazio
        if not isinstance(self.mask, np.ndarray):
            print("ERRO in image_colorizer(): Máscara não encontrada")
            return
        
        alpha = self.mask.astype(np.uint8)

        color = np.array([0, 0, 255])  # Cor verde (BGR no OpenCV)

        color_mask = np.zeros_like(image)  # Cria uma máscara com as mesmas dimensões da imagem
        color_mask[alpha == 1] = color  # Aplica a cor apenas nas áreas onde a máscara é 1

        # Sobrepor a máscara colorida na imagem
        result = cv2.addWeighted(image, 1.0, color_mask, 0.5, 0)
        return result
        
        


    async def segment_image_async(self,image_path: str, model_version="v1") -> cv2.typing.MatLike: # Ser assyncrono
        image = cv2.imread(image_path)
        self.model_version = model_version
        final_image = await self.segment_image(image)
        return final_image
    
    def get_counted_value(self):
        if self.counted == 0:
            return 'Nenhum segmento encontrado'
        return self.counted


