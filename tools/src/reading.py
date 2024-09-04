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
        if frame_count == 0 or ( frame_count % 3 == 0 ):
          frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
          # Salva o frame como arquivo JPEG
          cv2.imwrite(frame_filename, frame)

        # Incrementa o contador de frames
        frame_count += 1

    # Libera a captura de vídeo
    video_capture.release()

    print(f"Extração concluída. {frame_count} frames foram salvos em {output_folder}")


def create_movie(input_folder:str,output_folder:str, fps:int=30, codec:str="mp4v", name:str="output_video.mp4"):
    # Verifica se a pasta de saída existe, se não, cria
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define o caminho do arquivo de vídeo de saída
    output_video_path = os.path.join(output_folder, f"{name}.mp4")

    # Define o codec de vídeo
    fourcc = cv2.VideoWriter_fourcc(*codec)

    # Inicializa o objeto de escrita do vídeo
    video_writer = None

    # Loop para ler cada frame da pasta de entrada
    for filename in os.listdir(input_folder):
        # Verifica se o arquivo é um arquivo de imagem
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            # Lê o arquivo de imagem
            image = cv2.imread(os.path.join(input_folder, filename))

            # Se o objeto de escrita do vídeo não foi inicializado, inicializa
            if video_writer is None:
                # Obtém as dimensões do frame
                frame_height, frame_width, _ = image.shape

                # Inicializa o objeto de escrita do vídeo
                video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

            # Escreve o frame no vídeo
            video_writer.write(image)
            print(f"Frame {filename} adicionado ao vídeo")

    # Libera o objeto de escrita do vídeo
    video_writer.release()

    print(f"Vídeo criado em {output_video_path}")
# Exemplo de uso
#extract_frames("../archive/drone_image/DJI_0624.MOV", "pasta_de_saida")


create_movie("processed_images","processed_images", fps=15)