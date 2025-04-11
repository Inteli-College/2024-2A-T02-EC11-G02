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
        if len(image.shape) == 2:  
            image_adjusted = cv2.LUT(image, curve)
        else:  # Imagem colorida
            channels = cv2.split(image)  # Divide os canais B, G, R
            channels_adjusted = [cv2.LUT(channel, curve) for channel in channels]
            image_adjusted = cv2.merge(channels_adjusted)  # Mescla os canais de volta

        return image_adjusted

    def apply_color(self,image, rgb_filter):
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

    def apply_levels(image, levels):
        return 
    
    def apply_brightness_contrast(self, image, brightness, contrast):
        # Escalar o brilho para o intervalo de -255 a 255
        brightness = int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))
        
        # Escalar o contraste para o intervalo de -127 a 127
        contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))

        # Aplicar o brilho
        if brightness != 0:
            if brightness > 0:
                shadow = brightness
                max_value = 255
            else:
                shadow = 0
                max_value = 255 + brightness
            
            alpha = (max_value - shadow) / 255.0 
            gamma = shadow
            image = cv2.addWeighted(image, alpha, image, 0, gamma)
        
        # Aplicar o contraste
        if contrast != 0:
            alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
            gamma = 127 * (1 - alpha)
            image = cv2.addWeighted(image, alpha, image, 0, gamma)

        # # Garantir que os valores estejam entre 0 e 255
        # image = np.clip(image, 0, 255).astype(np.uint8)

        # print(f"Brightness: {brightness}, Contrast: {contrast}")
        # print(f"Alpha: {alpha}, Gamma: {gamma}")

        # # Verificar se a imagem tem valores esperados
        # print(f"Image min: {image.min()}, Image max: {image.max()}")

        
        return image


    
    def apply_kernal_bluer(self,image,kernal_size):
        return cv2.blur(image,(kernal_size,kernal_size))

    def rgb_to_hsv_array(self, rgb_array):
        # Convertendo para o formato correto para OpenCV (de [0, 255])
        rgb_array = rgb_array.astype(np.uint8)
        # Convertendo de RGB para HSV
        hsv_array = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2HSV)
        return hsv_array

    def hsv_to_rgb_array(self, hsv_array):
        # Convertendo de HSV para RGB
        rgb_array = cv2.cvtColor(hsv_array, cv2.COLOR_HSV2RGB)
        return rgb_array

    def level_image_numpy(self, image_np, minv=0, maxv=255, gamma=1.0):
        # Verifica se a imagem é grayscale e converte para RGB se necessário
        if len(image_np.shape) == 2:  # Imagem grayscale
            image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
        
        # Converte imagem para numpy array float32
        np_image = image_np.astype(np.float32)
        
        # Converte para HSV
        hsv_image = self.rgb_to_hsv_array(np_image)
        
        # Aplica o ajuste no canal V
        v = hsv_image[..., 2] / 255.0  # Normaliza o canal V para [0, 1]
        v = np.clip((v - minv/255.0) / ((maxv - minv)/255.0), 0, 1)
        v = np.power(v, 1.0 / gamma)
        
        # Reconstrói a imagem HSV ajustando o canal V
        hsv_image[..., 2] = (v * 255).astype(np.uint8)  # Desnormaliza para [0, 255]
        
        # Converte de volta para RGB
        rgb_image = self.hsv_to_rgb_array(hsv_image)
        
        return rgb_image
    def get_filters(self):
        return ['apply_curves','apply_color','apply_levels','apply_brightness_contrast','apply_kernal_bluer','level_image_numpy']

    def color_density_mean(self,image):
        # Verifica se a imagem tem 3 canais (RGB)
        if len(image.shape) == 3:
            # Calcula a média para cada canal de cor (B, G, R)
            mean_blue = np.mean(image[:, :, 0])
            mean_green = np.mean(image[:, :, 1])
            mean_red = np.mean(image[:, :, 2])
            
            return {
                'blue': float(mean_blue),
                'green': float(mean_green),
                'red': float(mean_red)
            }
        else:
            # Se a imagem for em escala de cinza
            mean_gray = np.mean(image)
            return {'gray': mean_gray}
        
    def apply_kmeans(self,image, k=3):
        # Converte a imagem para o formato adequado
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.reshape((-1, 3))
        image = np.float32(image)
        
        # Define os critérios de parada
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        
        # Aplica o algoritmo K-Means
        _, labels, centers = cv2.kmeans(image, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        # Converte de volta para o tipo de imagem original
        centers = np.uint8(centers)
        segmented_image = centers[labels.flatten()]
        segmented_image = segmented_image.reshape(image.shape)
        
        return segmented_image
    
    def apply_kernel(self,image, kernel):
        """
        Espera uma imagem e um kernel e retorna a convolução.
        """
        return cv2.filter2D(image, -1, kernel)


 
        
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