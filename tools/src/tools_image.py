import cv2
import numpy as np
import matplotlib.pyplot as plt
import colorsys

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
    
    def apply_brightness_contrast(self,image, brightness, contrast):
        image = image.astype(np.float32)
        image = image * contrast + brightness
        image = np.clip(image, 0, 255).astype(np.uint8)
        return image
    
    def apply_kernal_bluer(self,image,kernal_size):
        return cv2.blur(image,(kernal_size,kernal_size))

    def rgb_to_hsv_array(self,rgb_array):
    # Normalize RGB values to [0, 1]
        rgb_array = rgb_array / 255.0
        # Convert to HSV
        hsv_array = np.zeros_like(rgb_array)
        for i in range(rgb_array.shape[0]):
            for j in range(rgb_array.shape[1]):
                r, g, b = rgb_array[i, j]
                hsv_array[i, j] = colorsys.rgb_to_hsv(r, g, b)
        return hsv_array

    def hsv_to_rgb_array(self,hsv_array):
        # Convert back to RGB
        rgb_array = np.zeros_like(hsv_array)
        for i in range(hsv_array.shape[0]):
            for j in range(hsv_array.shape[1]):
                h, s, v = hsv_array[i, j]
                rgb_array[i, j] = colorsys.hsv_to_rgb(h, s, v)
        # Denormalize to [0, 255]
        return (rgb_array * 255).astype(np.uint8)

    def level_image_numpy(self,image_np, minv=0, maxv=255, gamma=1.0):
        # Convert image to RGB if it is grayscale
        if len(image_np.shape) == 2:  # Grayscale image
            image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
        
        # Convert image to numpy array
        np_image = image_np.astype(np.float32)
        
        # Convert to HSV
        hsv_image = self.rgb_to_hsv_array(np_image)
        
        # Apply level adjustment to V channel
        v = hsv_image[..., 2]
        v = np.clip((v - minv/255.0) / ((maxv - minv)/255.0), 0, 1)
        v = np.power(v, 1.0 / gamma)
        
        # Reconstruct HSV
        hsv_image[..., 2] = v
        
        # Convert back to RGB
        rgb_image = self.hsv_to_rgb_array(hsv_image)
        
        return rgb_image



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