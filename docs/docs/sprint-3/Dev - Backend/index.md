---
title: Desenvolvimento Back-End
sidebar_position: 1
---

# Processamento de Imagens com Câmera no Rapsberry

Para captura de imagens no sistema IoT, foi utilizada uma câmera integrada ao Raspberry Pi, que faz parte do kit do Braço Robótico Dobot Magician. O sistema realiza a captura das imagens em tempo real e as armazena no dispositivo. Em seguida, as imagens são compactadas em um arquivo ZIP e enviadas para um servidor remoto via protocolo HTTP.

## Funcionalidades

**1. Captura de Imagens:**

- O sistema captura imagens de uma câmera em tempo real.
- As imagens são salvas localmente quando o usuário aciona um comando (tecla s), e a captura pode ser finalizada com a tecla q.

**2- Compactação das Imagens:**

- Todas as imagens capturadas são compactadas em um arquivo ZIP, utilizando a biblioteca libzip.

**3 - Upload do Arquivo ZIP:**

- O arquivo ZIP criado é enviado automaticamente para um servidor remoto via uma requisição HTTP, usando a biblioteca libcurl.

## Dependências

**As bibliotecas utilizadas neste projeto são:**

- OpenCV: Para capturar e exibir imagens.
- libzip: Para compactação dos arquivos de imagem.
- libcurl: Para enviar o arquivo compactado para um servidor.
- std::filesystem: Para manipulação de diretórios e arquivos.

## Descrição das Funcionalidades

**1. Captura de Imagens com OpenCV**

- O programa utiliza a câmera padrão do sistema para capturar imagens.
- As imagens são exibidas em uma janela em tempo real.
- Quando o usuário pressiona a tecla s, o quadro atual é salvo como uma imagem em um diretório local.
- A captura pode ser encerrada a qualquer momento pressionando a tecla q.

**2. Compactação das Imagens**

- Após o término da captura, o programa compacta todas as imagens salvas no diretório em um arquivo ZIP.
- O arquivo ZIP é criado no diretório de trabalho e contém todas as imagens capturadas.

**3. Upload do Arquivo ZIP para um Servidor**

- O arquivo ZIP gerado é enviado para um servidor via uma requisição HTTP POST.
- O envio é feito utilizando o protocolo MIME, anexando o arquivo como parte do corpo da requisição.
- Caso o upload seja bem-sucedido, o programa exibe uma mensagem de sucesso; caso contrário, uma mensagem de erro é mostrada.

## Fluxo de Execução

- Inicialização: A câmera é aberta, e uma janela é exibida mostrando os quadros capturados em tempo real.
- Captura de Imagens: O usuário pode pressionar a tecla s para salvar imagens no formato JPEG em um diretório específico.
- Finalização da Captura: O loop de captura é finalizado ao pressionar a tecla q.
- Compactação: As imagens capturadas são compactadas em um arquivo ZIP.
- Upload: O arquivo ZIP é enviado para o servidor especificado.

# Desenvolvimento do Backend para Processamento de Imagem com Firebase

Este backend foi desenvolvido em Python utilizando FastAPI para gerenciar rotas HTTP e sincroniza com o Firebase para armazenamento de arquivos. O projeto implementa um pipeline de processamento de imagem que tem como objetivo a contagem de árvores em imagens enviadas pelo usuário.

## Tecnologias Utilizadas

- **Python**: Linguagem principal de desenvolvimento.
- **FastAPI**: Framework para a construção de APIs rápidas e eficientes.
- **Firebase Storage**: Usado para armazenamento de arquivos enviados.
- **FilteringSegmentation**: Pipeline utilizado para o processamento de imagens e extração de informações.

## Rotas Disponíveis

### 1. **POST /modelversion**

Essa rota recebe um arquivo de imagem, processa-o utilizando o pipeline de extração e retorna a imagem processada.

- **URL**: `/modelversion`
- **Método HTTP**: `POST`
- **Parâmetros**:
  - `file`: Um arquivo de imagem (png) enviado pelo usuário.
- **Resposta**: Retorna a imagem processada.
- **Tratamento de Erros**: Retorna um erro 500 se houver falha no processamento.

#### Exemplo de Requisição

```bash
curl -X POST "http://localhost:8000/modelversion" -F "file=@imagem.png"
```

#### Exemplo de Resposta

```json
{
  "imagem": "imagem processada com a contagem de árvores"
}
```

### 2. **POST /modelfb**

Essa rota recebe um arquivo de imagem, realiza o processamento de extração e faz o upload do arquivo para o Firebase Storage. Retorna a URL pública do arquivo e a imagem processada.

- **URL**: `/modelfb`
- **Método HTTP**: `POST`
- **Parâmetros**:
  - `file`: Um arquivo de imagem (jpeg, jpg, png) enviado pelo usuário.
- **Resposta**: Retorna a URL pública do arquivo no Firebase e a imagem processada.
- **Tratamento de Erros**:
  - Erro 400 se o formato do arquivo for inválido.
  - Erro 500 em caso de falhas no processamento ou upload para o Firebase.

#### Exemplo de Requisição

```bash
curl -X POST "http://localhost:8000/modelfb" -F "file=@imagem.jpeg"
```

#### Exemplo de Resposta

```json
{
  "file_url": "https://storage.googleapis.com/seu-bucket/uploads/imagem.jpeg",
  "imagem": "imagem processada com a contagem de árvores"
}
```

## Erros Comuns

- **400 - Formato de arquivo inválido**: Ocorre quando o arquivo enviado não está em um dos formatos permitidos (.jpeg, .jpg, .png).
- **500 - Erro interno do servidor**: Ocorre quando há uma falha no processamento da imagem ou no upload para o Firebase.