import cv2
import numpy as np
import scipy.ndimage as ndi
import matplotlib.pyplot as plt

def get_height_by_channel(self, image, channel):
    channels = cv2.split(image)
    edited_image = super().apply_brightness_contrast(channels[channel], -80, 1.2)
    edited_image = super().apply_curves(edited_image, np.array([[0,0], [58,136], [62, 177], [135, 85], [139, 154]]))
    edited_image = super().level_image_numpy(edited_image, 33, 52, 1.72)

    # Se edited_image já for uma imagem em tons de cinza, não faça merge
    if len(edited_image.shape) == 3:
        edited_image = cv2.cvtColor(edited_image, cv2.COLOR_BGR2GRAY)
    
    print(f'shape: {edited_image.shape}')
    
    # Rotulagem de segmentos
    labeled_array, num_features = ndi.label(edited_image, structure=np.ones((3, 3)))  # Conectividade de 8 vizinhos
    
    print(f'Número de componentes conectados: {num_features}')
    
    # Criar imagem colorida para desenhar quadrados nos segmentos
    image_with_boxes = cv2.cvtColor(edited_image, cv2.COLOR_GRAY2BGR)
    
    # Encontrar os limites de cada segmento
    for label in range(1, num_features + 1):
        segment_mask = (labeled_array == label).astype(np.uint8)
        contours, _ = cv2.findContours(segment_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Desenhar retângulos ao redor dos segmentos
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image_with_boxes, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Desenhar quadrado vermelho
    
    # Exibir imagem com quadrados vermelhos
    self.plot_images(image_with_boxes, f"Numero de segmentos encontrados {num_features}", 1, "gray")
    plt.show()
