import cv2
import numpy as np
from scipy.ndimage import label, find_objects
import matplotlib.pyplot as plt

# Função para calcular um mapa de calor a partir da imagem binária
def generate_heatmap(binary_image):
    # Aplicar um filtro gaussiano para criar um mapa de calor
    heatmap = cv2.GaussianBlur(binary_image.astype(np.float32), (15, 15), 0)
    return heatmap

# Função para segmentar árvores com base em mapa de calor e componentes conectados
def count_trees_with_adjustments_and_plot(image_path):
    # Carregar a imagem em tons de cinza
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if image is None:
        raise FileNotFoundError(f"Arquivo de imagem não encontrado: {image_path}")
    
    # Binarizar a imagem (ajuste fino do limiar)
    _, binary_image = cv2.threshold(image, 150, 1, cv2.THRESH_BINARY)
    
    # Aplicar uma abertura morfológica mais agressiva para remover pequenos ruídos
    kernel = np.ones((1, 1), np.uint8)  # Aumentasse o kernel para remover mais ruído
    binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)
    
    # Gerar o mapa de calor a partir da imagem binária
    heatmap = generate_heatmap(binary_image)
    
    # Limiar para converter o mapa de calor de volta em uma imagem binária
    _, heatmap_binary = cv2.threshold(heatmap, 0.4, 1, cv2.THRESH_BINARY)  # Ajustar o limiar de acordo com a densidade
    
    # Segmentar componentes conectados no mapa de calor binário
    structure = np.ones((3, 3), dtype=int)
    labeled_image, num_trees = label(heatmap_binary, structure=structure)

    # Filtrar componentes pequenos com um valor mínimo ajustado
    min_size = 13  # Aumentar o tamanho mínimo para remover mais ruídos
    predicted_objects = []

    for obj in find_objects(labeled_image):
        y_slice, x_slice = obj
        if (x_slice.stop - x_slice.start) * (y_slice.stop - y_slice.start) > min_size:
            predicted_objects.append([x_slice.start, y_slice.start, x_slice.stop, y_slice.stop])

    # Exibir o número de árvores detectadas
    print(f"Número de árvores detectadas após ajustes: {len(predicted_objects)}")
    
    # Desenhar as caixas delimitadoras
    output_image = cv2.cvtColor(binary_image * 255, cv2.COLOR_GRAY2BGR)

    for box in predicted_objects:
        top_left = (box[0], box[1])
        bottom_right = (box[2], box[3])
        cv2.rectangle(output_image, top_left, bottom_right, (0, 255, 0), 2)

    # Exibir a imagem resultante com as caixas delimitadoras
    plt.figure(figsize=(8, 6))
    plt.imshow(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))
    plt.title(f'Número de árvores detectadas após ajustes: {len(predicted_objects)}')
    plt.axis('off')
    plt.show()

    return len(predicted_objects)


def count_trees_with_adjustments(transform_image, output_image,  min_size: float = 13.0):
    if transform_image is None:
        raise FileNotFoundError(f"Arquivo de imagem não encontrado")
    
    # Binarizar a imagem (ajuste fino do limiar)
    _, binary_image = cv2.threshold(transform_image, 150, 1, cv2.THRESH_BINARY)
    
    # Aplicar uma abertura morfológica mais agressiva para remover pequenos ruídos
    kernel = np.ones((1, 1), np.uint8)  # Aumentasse o kernel para remover mais ruído
    binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)
    
    # Gerar o mapa de calor a partir da imagem binária
    heatmap = generate_heatmap(binary_image)
    
    # Limiar para converter o mapa de calor de volta em uma imagem binária
    _, heatmap_binary = cv2.threshold(heatmap, 0.4, 1, cv2.THRESH_BINARY)  # Ajustar o limiar de acordo com a densidade
    
    # Segmentar componentes conectados no mapa de calor binário
    structure = np.ones((3, 3), dtype=int)
    labeled_image, _ = label(heatmap_binary, structure=structure)

    # Filtrar componentes pequenos com um valor mínimo ajustado
    predicted_objects = []

    for obj in find_objects(labeled_image):
        y_slice, x_slice = obj
        if (x_slice.stop - x_slice.start) * (y_slice.stop - y_slice.start) > min_size:
            predicted_objects.append([x_slice.start, y_slice.start, x_slice.stop, y_slice.stop])

    # Exibir o número de árvores detectadas
    print(f"Número de árvores detectadas após ajustes: {len(predicted_objects)}")

    for box in predicted_objects:
        top_left = (box[0], box[1])
        bottom_right = (box[2], box[3])
        cv2.rectangle(output_image, top_left, bottom_right, (0, 255, 0), 2)

    return (len(predicted_objects), output_image)




def main():
    # Caminho da imagem fornecida
    image_path = 'dataset/test/Patrica_teste.png'
    tree_count = count_trees_with_adjustments_and_plot(image_path)
    print(tree_count)


