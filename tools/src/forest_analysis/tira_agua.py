import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import cv2

# Carregar uma imagem em escala de cinza
image = cv2.imread('../dataset/train/maps_01.png', cv2.IMREAD_GRAYSCALE)

# Aplicar um desfoque (blur) alto usando um filtro Gaussiano
blurred_image = cv2.GaussianBlur(image, (1, 1), 0)

# Calcular gradiente (derivada) da imagem desfocada
sobel_x = ndimage.sobel(blurred_image, axis=0)
sobel_y = ndimage.sobel(blurred_image, axis=1)
magnitude = np.hypot(sobel_x, sobel_y)

# Mostrar a imagem original e a imagem com gradiente de magnitude
plt.figure(figsize=(20, 10))

plt.subplot(1, 1, 1)
plt.title("Magnitude do Gradiente")
plt.imshow(magnitude, cmap='gray')


plt.show()
