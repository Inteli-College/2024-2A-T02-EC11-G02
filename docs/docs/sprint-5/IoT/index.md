---
title: IoT
---

# Sistema de Processamento de Imagens com Câmera no Raspberry Pi

Para captura de imagens no sistema IoT, foi utilizada uma câmera integrada ao Raspberry Pi, que faz parte do kit do Braço Robótico Dobot Magician. O sistema realiza a captura das imagens em tempo real e as armazena no dispositivo. Em seguida, as imagens são compactadas em um arquivo ZIP e enviadas para um servidor remoto via protocolo HTTP.

# Funcionalidades

## 1. Captura de Imagens:

- Captura imagens em tempo real utilizando a câmera conectada ao Raspberry Pi.
- Exibe as imagens capturadas em uma janela de visualização.
- Permite ao usuário salvar imagens pressionando a tecla ``s``.
- A captura pode ser finalizada pressionando a tecla ``q``.

## 2. Compactação das Imagens:

- Compacta todas as imagens salvas em um diretório específico em um arquivo ZIP.
- Utiliza a biblioteca libzip para a compactação.

## 3. Upload do Arquivo ZIP:

- Envia o arquivo ZIP gerado para um servidor remoto via requisição HTTP POST.
- Utiliza a biblioteca libcurl para realizar a requisição.

# Dependências

### O projeto utiliza as seguintes bibliotecas:

- OpenCV: Para captura e exibição de imagens.
- libzip: Para compactação dos arquivos de imagem.
- libcurl: Para enviar o arquivo compactado para um servidor.
- std::filesystem: Para manipulação de diretórios e arquivos (necessário compilador com suporte a C++17 ou superior).

# Pré-requisitos
Antes de compilar e executar o programa, certifique-se de que todas as dependências estão instaladas no sistema.

### Atualizar o Sistema
``
sudo apt-get update
sudo apt-get upgrade
``

### Instalar o OpenCV
``
sudo apt-get install libopencv-dev
``
### Instalar a libzip
``
sudo apt-get install libzip-dev
``
### Instalar a libcurl
``
sudo apt-get install libcurl4-openssl-dev
``
### Verificar o Compilador
Certifique-se de que o compilador suporta C++17 ou superior:
``
g++ --version
``
Se necessário, instale uma versão mais recente do g++:
``
sudo apt-get install g++-8
``
### Compilação
Salve o código em um arquivo chamado ``main.cpp``.

### Compile o programa usando o seguinte comando:
``
g++ main.cpp -o image_processor -std=c++17 `pkg-config --cflags --libs opencv4` -lzip -lcurl
``

**_Observações:_**

Se estiver utilizando uma versão diferente do OpenCV, ajuste opencv4 para a versão instalada.
O parâmetro ``-std=c++17`` é necessário para utilizar a biblioteca ``std::filesystem.``

# Execução
Para executar o programa, use o comando:

``
./image_processor
``

# Instruções de Uso

### Iniciar o Programa:

- Execute o programa conforme indicado na seção de execução.
- Uma janela chamada Camera será aberta exibindo o feed em tempo real da câmera.

### Capturar Imagens:

- Pressione a tecla ``s`` para salvar a imagem atual.
- As imagens serão salvas no diretório imagens com o nome image_N.jpg, onde N é um número incremental.

### Finalizar a Captura:

- Pressione a tecla ``q ``para encerrar a captura e fechar o programa.

### Pós-Processamento:

- Após a finalização, o programa compactará as imagens salvas em um arquivo imagens.zip.
- Em seguida, enviará o arquivo ZIP para o servidor especificado.

# Fluxo de Execução
### Inicialização:

- O programa inicia abrindo a câmera conectada ao Raspberry Pi.
- Configura a resolução da câmera para 640x480 pixels.
- Cria um diretório chamado imagens para salvar as imagens capturadas.

### Captura de Imagens:

- Entra em um loop onde captura e exibe os quadros da câmera em tempo real.
- Aguarda por entradas do usuário:
- Pressionar s salva a imagem atual.
- Pressionar q encerra o loop de captura.

### Compactação:

- Utiliza a função zip_folder para compactar todas as imagens do diretório imagens em um arquivo imagens.zip.

### Upload:

- Utiliza a função upload_zip para enviar o arquivo ZIP para o servidor via HTTP POST.
- Exibe mensagens de sucesso ou erro com base no resultado do upload.

# Possíveis Erros e Soluções

### Erro ao abrir a câmera:

- Verifique se a câmera está conectada corretamente e não está sendo usada por outro aplicativo.

### Erro ao compilar devido a bibliotecas não encontradas:

- Certifique-se de que todas as dependências estão instaladas e que o comando de compilação aponta para as versões corretas.

### Erro ao enviar o arquivo para o servidor:

- Verifique a conectividade de rede e se o endereço do servidor (url) está correto.

# Personalizações

### Alterar o diretório de salvamento das imagens:

- Modifique a variável folder_name no código para o caminho desejado.

### Alterar o endereço do servidor para upload:

- Modifique a variável url no código para o endereço do seu servidor.

### Ajustar a resolução da câmera:

- Altere os valores de ``cv::CAP_PROP_FRAME_WIDTH`` e ``cv::CAP_PROP_FRAME_HEIGHT.``