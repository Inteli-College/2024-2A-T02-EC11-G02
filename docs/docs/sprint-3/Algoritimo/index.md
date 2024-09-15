---
title: Algoritmo de transformação para Imagens
sidebar_position: 0
---

Conjunto de ferramentas desenvolvidas para resolução do problema proposto.

# Estrutura de Pastas e Arquivos

```plaintext
.github/
docs/
tools/   ---------------------------------------------------> Ferramentas para tranformações em imagens
    src/
        __pycache__/
        dataset/  --------------------------------------------> Imagens usadas para validar o algoritmo
        filters/  -------------------------------------------------------> Filtros obtidos do Photoshop
        forest_analysis/
        output/
            filter_extractor.py  -----------------------> Ferramenta de extração de filtros do photoshop
            levels.py  ------------------------> Implementação do filtro levels sem transformação em HSV 
            levels2.py  --------------------------> Implementação do filtro levels com transformação HSV
            model_count_tree.py  --------------> Implementação de um algoritmo de segmentação e contagem
            pplay_filter.py  ------------------> Conjunto de aplicação de filtros em sequência
            reading.py  -----------------------> Leitor de videos
            requirements.txt
            tools_image.py  -------------------> Conjunto de filtros
    create_mask.py
```

## Ferramentas principais

### Conjunto de filtros 

O arquivo **tools_image.py** é responsável pela implementação da classe **ImageFilters** que contem os seguintes filtros:
- curves
- color
- brightness and contrast
- rgb to hsv
- hsv to rgb
- levels
- kmeans
- kernel

```python

    def pply_curves(self,image, curve_points):

        # Cria uma curva de interpolação linear a partir dos pontos fornecidos
        curve = np.interp(np.arange(256), curve_points[:, 0], curve_points[:, 1]).astype(np.uint8)
        
        # Aplica a curva a cada canal da imagem
        if len(image.shape) == 2:  
            image_adjusted = cv2.LUT(image, curve)
        else:  # Imagem colorida
            channels = cv2.split(image)  # Divide os canais B, G, R
            channels_adjusted = [cv2.LUT(channel, curve) for channel in channels]
            image_adjusted = cv2.merge(channels_adjusted)  # Mescla os canais de volta

        return image_adjusted

    def pply_color(self,image, rgb_filter):
        """
        Realçe um dos canais RGB de cor da imagem.

        Args: ragb_filter: lista com 3 valores inteiros no intervalo de 1 a 0, para cada canal RGB.

        Returns: Imagem com os canais RGB realçados.
        """
        out = np.zeros_like(image)
        


        out[:, :, 0] = image[:, :, 0]  + rgb_filter[0] # R
        out[:, :, 1] = image[:, :, 1]  + rgb_filter[1] # G
        out[:, :, 2] = image[:, :, 2]  + rgb_filter[2] # B
        return out

    def pply_brightness_contrast(self,image, brightness, contrast):
        image = image.astype(np.float32)
        image = image * contrast + brightness
        image = np.clip(image, 0, 255).astype(np.uint8)
        return image

    def pply_kernal_bluer(self,image,kernal_size):
        return cv2.blur(image,(kernal_size,kernal_size))


    def rgb_to_hsv_array(self,rgb_array): # Passa os valores de RGB para HSV
    # Normaliza os valores de RGB para [0, 1]
        rgb_array = rgb_array / 255.0
        # Converte para HSV
        hsv_array = np.zeros_like(rgb_array)
        for i in range(rgb_array.shape[0]):
            for j in range(rgb_array.shape[1]):
                r, g, b = rgb_array[i, j]
                hsv_array[i, j] = colorsys.rgb_to_hsv(r, g, b)
        return hsv_array


    def level_image_numpy(self,image_np, minv=0, maxv=255, gamma=1.0):
        # Converte imagem para RGB se for escala de cinza
        if len(image_np.shape) == 2: 
            image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
        
        # Converte para um array de ponto flutuante
        np_image = image_np.astype(np.float32)
        
        # Converte para HSV
        hsv_image = self.rgb_to_hsv_array(np_image)
        
        # Aplica o ajuste de níveis na componente de valor (V)
        v = hsv_image[..., 2]
        v = np.clip((v - minv/255.0) / ((maxv - minv)/255.0), 0, 1)
        v = np.power(v, 1.0 / gamma)
        
        # Refaz a imagem HSV
        hsv_image[..., 2] = v
        
        # Converte para RGB
        rgb_image = self.hsv_to_rgb_array(hsv_image)
        
        return rgb_image

# ...

```

### Aplicação dos filtros em sequência

O arquivo **pplay_filter.py** é responsável pela implementação da classe FilteringSegmentation, que contém diversas ferramentas, sendo as principais:

- Detector de canal predominante ( choice_channel )
- Criador de janela com gráficos ( plot_images )
- Criador de máscara pelo canal de cor ( get_mask_by_channel )
- Removedor de fundo ( remuve_background )
- Estrator picos de luz ( get_highlights_by_channel )
- Desenhador de segmentos ( draw_rectangle )
- Criador de máscara pela textura ( get_texture_mask )


```python

    def choice_channel(self, image: cv2.typing.MatLike) -> int:
        B, G, R = cv2.split(image)

        trashold = 40 # Define o valor minimo de itensidade para os pixels

        # Trasforma o canal de cor em uma matriz de 0 e 1, onde 0 é o pixel mais intenso que o trashold e 1 os que são menos
        B = B < trashold
        G = G < trashold
        R = R < trashold

        # Define qual canal de cor contém mais pixels dentro do limite do trashold
        choice = np.argmax([np.sum(B), np.sum(G), np.sum(R)])

        return choice

    def plot_images(self,image: cv2.typing.MatLike, title, position, cmap=None, nrows=2, ncols=3):
        # Uma abstração para a função de plotar images do matplotlib
        plt.subplot(nrows, ncols, position)
        plt.title(title)
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), cmap=cmap)

    def get_mask_by_channel(self,image: cv2.typing.MatLike, channel) -> cv2.typing.MatLike:

        # Separar os canais R, G, B
        channels = cv2.split(image)

        # Aplicar as transformações no canal escolhido
        image_transform = super().pply_brightness_contrast(channels[channel], 40, 1.5)
        image_transform = super().pply_curves(image_transform, np.array([[0, 0], [105, 92], [146, 247], [255, 255]]))
        image_transform = super().pply_kernal_bluer(image_transform, 5)
        image_transform = super().level_image_numpy(image_transform, 200, 255, 9.9)
        
        # Normalizar a máscara para ter valores entre 0 e 255
        _mask = cv2.normalize(image_transform, None, 0, 255, cv2.NORM_MINMAX)

        # Inverte o valor da máscara
        _mask_inverted = cv2.bitwise_not(_mask)

        return _mask_inverted

    def remuve_background(self,image: cv2.typing.MatLike) -> cv2.typing.MatLike:
        # Aplica a máscara de canal de cor a uma imagem usando o detector de canal predominante
        target_image = cv2.bitwise_and(image, self.get_mask_by_channel(image, self.choice_channel(image)))
        return target_image
    
    def get_highlights_by_channel(self,edited_image: cv2.typing.MatLike, channel) -> cv2.typing.MatLike:
        
        # Separar os canais R, G, B
        channels = cv2.split(edited_image)
        image_transform = super().pply_brightness_contrast(channels[channel], -80, 1.2) # Nivela por baixo o brilho da imagem
        image_transform = super().pply_curves(image_transform, np.array([[0,0], [58,136], [62, 177], [135, 85], [139, 154]]) # Faz uma destribuição das tonalidades pela curva
)
        image_transform = super().level_image_numpy(image_transform, 33, 52, 1.72) # Altera os valors de saída do histograma da image

        return image_transform

    def draw_rectangle(self,normal_image: cv2.typing.MatLike, image_transform: cv2.typing.MatLike):
        # Recebe a imagem produto da função get_highlights_by_channel

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
                    cv2.rectangle(normal_image, (x, y), (x + w, y + h), (0, 0, 255), 1) 
            return normal_image

```


Foi o uso em conjuto dessas ferramentas que possibilitou alcançar os resultados dessa sprint.


**Imagem de entrada**

![Imagem normal](/img/filter_segmtation/sprint3/normal.png)


**remuve_background_and_plot('tools\src\output\01.png')**

![Imagem após aplicação remuve_background](/img/filter_segmtation/sprint3/01.png)


**get_highlights_by_channel('tools\src\output\01.png')**

![Imagem após aplicação get_highlights_by_channel](/img/filter_segmtation/sprint3/03.png)


**segment_and_plot(tools\src\dataset\train\02.png)**

![Imagem após aplicação segment_and_plot](/img/filter_segmtation/sprint3/04.png)


