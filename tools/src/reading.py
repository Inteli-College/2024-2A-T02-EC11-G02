import cv2
import os

def extract_frames(video_path, output_folder):
    # Verifica se a pasta de saída existe, se não, cria
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Captura o vídeo
    video_capture = cv2.VideoCapture(video_path)
    
    # Inicializa o contador de frames
    frame_count = 0

    # Loop para ler frame por frame
    while True:
        # Lê o frame
        success, frame = video_capture.read()

        # Se não conseguir ler mais frames (fim do vídeo), interrompe o loop
        if not success:
            break

        # Define o nome do arquivo com base no contador de frames
        if frame_count == 0 or ( frame_count % 60 == 0 ):
          frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
          # Salva o frame como arquivo JPEG
          cv2.imwrite(frame_filename, frame)

        # Incrementa o contador de frames
        frame_count += 1

    # Libera a captura de vídeo
    video_capture.release()

    print(f"Extração concluída. {frame_count} frames foram salvos em {output_folder}")

# Exemplo de uso
extract_frames("DJI_0599.MOV", "pasta_de_saida")
