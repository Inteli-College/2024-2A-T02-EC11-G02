"""Cimulação de NVDI usando o canal verde como NIR"""

import numpy as np
import cv2
import matplotlib.pyplot as plt

# Função para calcular NDVI com canais RGB
def calculate_ndvi_from_png(image):
    # Extrair os canais da imagem RGB
    red = image[:, :, 2].astype(float)
    nir_simulated = image[:, :, 1].astype(float)  # Usar canal verde como simulação de NIR
    
    # Calcular o NDVI
    ndvi = (nir_simulated - red) / (nir_simulated + red + 1e-6)  # Adicionar uma constante pequena para evitar divisão por zero
    return ndvi

# Carregar a imagem PNG
image = cv2.imread('../dataset/train/03.png')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Calcular NDVI
ndvi = calculate_ndvi_from_png(image_rgb)

# Mostrar o antes (imagem original)
plt.subplot(1, 2, 1)
plt.imshow(image_rgb)
plt.title("Imagem Original")

# Mostrar o depois (NDVI)
plt.subplot(1, 2, 2)
plt.imshow(ndvi, cmap='RdYlGn')
plt.colorbar(label="NDVI")
plt.title("NDVI (Simulado)")

plt.show()

