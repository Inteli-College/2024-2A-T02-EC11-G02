import cv2
import numpy as np
from tools_image import ImageFilters
import os
import pathlib


tools = ImageFilters()
pathlib.Path('archive/Forest Segmented/Forest Segmented/masks/').mkdir(parents=True, exist_ok=True)


def save_image(image, path):
    cv2.imwrite(path, image)

def get_mask(image_path):
    # Carregar a imagem
    image = cv2.imread(image_path)
    
    # Separar os canais R, G, B
    _, _, R = cv2.split(image)

    # Aplicar as transformações no canal R
    R = tools.apply_brightness_contrast(R, 20, 1.5)
    R = tools.apply_curves(R, np.array([[0, 0], [105, 92], [146, 247], [255, 255]]))
    R = tools.apply_kernal_bluer(R, 5)
    R = tools.level_image_numpy(R, 200, 255, 9.9)
    
    # Normalizar a máscara para ter valores entre 0 e 255
    _mask = cv2.normalize(R, None, 0, 255, cv2.NORM_MINMAX)
    #_mask = cv2.merge([_mask, _mask, _mask])
    _mask_inverted = cv2.bitwise_not(_mask)

    return _mask_inverted



dir_images = os.listdir('archive/Forest_Segmented/images/')


for image_name in dir_images:
    image_path = 'archive/Forest_Segmented/images/' + image_name
    save_image(get_mask(image_path), 'archive/Forest_Segmented/masks/' + image_name)
    