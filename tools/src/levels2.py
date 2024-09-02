import numpy as np
import colorsys
import matplotlib.pyplot as plt
import cv2

def rgb_to_hsv_array(rgb_array):
    # Normalize RGB values to [0, 1]
    rgb_array = rgb_array / 255.0
    # Convert to HSV
    hsv_array = np.zeros_like(rgb_array)
    for i in range(rgb_array.shape[0]):
        for j in range(rgb_array.shape[1]):
            r, g, b = rgb_array[i, j]
            hsv_array[i, j] = colorsys.rgb_to_hsv(r, g, b)
    return hsv_array

def hsv_to_rgb_array(hsv_array):
    # Convert back to RGB
    rgb_array = np.zeros_like(hsv_array)
    for i in range(hsv_array.shape[0]):
        for j in range(hsv_array.shape[1]):
            h, s, v = hsv_array[i, j]
            rgb_array[i, j] = colorsys.hsv_to_rgb(h, s, v)
    # Denormalize to [0, 255]
    return (rgb_array * 255).astype(np.uint8)

def level_image_numpy(image_np, minv=0, maxv=255, gamma=1.0):
    # Convert image to RGB if it is grayscale
    if len(image_np.shape) == 2:  # Grayscale image
        image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
    
    # Convert image to numpy array
    np_image = image_np.astype(np.float32)
    
    # Convert to HSV
    hsv_image = rgb_to_hsv_array(np_image)
    
    # Apply level adjustment to V channel
    v = hsv_image[..., 2]
    v = np.clip((v - minv/255.0) / ((maxv - minv)/255.0), 0, 1)
    v = np.power(v, 1.0 / gamma)
    
    # Reconstruct HSV
    hsv_image[..., 2] = v
    
    # Convert back to RGB
    rgb_image = hsv_to_rgb_array(hsv_image)
    
    return rgb_image

def main():
    # Exemplo de uso
    image = cv2.imread('dataset/04.png')
    imagem_cinza = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    adjusted_image = level_image_numpy(imagem_cinza, minv=55, maxv=150, gamma=10)

    # Exibe a imagem original e a ajustada
    plt.figure(figsize=(10, 5))

    # Exibir imagem original
    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # Converte BGR para RGB para exibir corretamente


    # Exibir imagem ajustada
    plt.subplot(1, 2, 2)
    plt.title("Ajustada")
    plt.imshow(adjusted_image)


    plt.show()

if __name__ == '__main__':
    main()