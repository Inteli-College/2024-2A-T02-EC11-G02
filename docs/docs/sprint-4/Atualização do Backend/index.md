# Documentação da API de Processamento de Imagens

## Visão Geral

Atualização do Backend. Foram criados novas rotas ára agregar valor ao projeto.

### Avanços da Sprint Anterior

Na última sprint, foram desenvolvidas duas novas rotas:
- **/firebase_url**: Para realizar o upload de imagens no Firebase Storage e retornar a URL pública.
- **/upload_and_process**: Para realizar o upload de um arquivo ZIP, processar suas imagens, e armazenar os resultados processados no Firebase Storage, retornando as URLs públicas.

Além disso, a rota **/modelversion** foi revisada e aprimorada.

---

## Rota 1: `POST /modelversion`

### Descrição:
Esta rota recebe uma imagem PNG, utiliza o pipeline de segmentação para contar as árvores na imagem e retorna a imagem processada.

### Detalhes da Rota:
- **Método HTTP**: `POST`
- **URL**: `/modelversion`
- **Parâmetro**:
  - `file`: (obrigatório) Arquivo de imagem PNG a ser processado.
  
### Exemplo de Requisição:
```bash
curl -X 'POST' \
  'http://localhost:8000/modelversion' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@image.png'
```

### Exemplo de Resposta (Sucesso):
- **Código**: `200 OK`
- **Resposta**: Retorna a imagem processada no formato PNG.

### Códigos de Resposta:
- `200 OK`: Imagem processada com sucesso.
- `500 Internal Server Error`: Ocorreu um erro durante o processamento da imagem.

---

## Rota 2: `POST /firebase_url`

### Descrição:
Esta rota realiza o upload de uma imagem PNG, processa a imagem para contar as árvores, e armazena a imagem processada no Firebase Storage. A rota retorna a URL pública da imagem processada.

### Detalhes da Rota:
- **Método HTTP**: `POST`
- **URL**: `/firebase_url`
- **Parâmetro**:
  - `file`: (obrigatório) Arquivo de imagem PNG a ser processado.
  
### Exemplo de Requisição:
```bash
curl -X 'POST' \
  'http://localhost:8000/firebase_url' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@image.png'
```

### Exemplo de Resposta (Sucesso):
- **Código**: `200 OK`
- **Resposta**: 
```json
{
  "processed_image_url": "https://firebasestorage.googleapis.com/v0/b/seu-bucket/o/processed%2Fimage.png?alt=media"
}
```

### Códigos de Resposta:
- `200 OK`: Imagem processada e URL retornada com sucesso.
- `500 Internal Server Error`: Ocorreu um erro durante o processamento ou upload da imagem.

---

## Rota 3: `POST /upload_and_process/`

### Descrição:
Esta rota recebe um arquivo ZIP contendo várias imagens PNG, processa cada uma delas utilizando o pipeline de segmentação para contar as árvores e faz o upload das imagens originais e processadas no Firebase Storage. Ela retorna as URLs públicas das imagens originais e processadas.

### Detalhes da Rota:
- **Método HTTP**: `POST`
- **URL**: `/upload_and_process/`
- **Parâmetro**:
  - `file`: (obrigatório) Arquivo ZIP contendo as imagens PNG a serem processadas.
  
### Exemplo de Requisição:
```bash
curl -X 'POST' \
  'http://localhost:8000/upload_and_process/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@images.zip'
```

### Exemplo de Resposta (Sucesso):
- **Código**: `200 OK`
- **Resposta**:
```json
{
  "message": "Imagens processadas e enviadas com sucesso!",
  "original_urls": [
    "https://firebasestorage.googleapis.com/v0/b/seu-bucket/o/original%2Fimage1.png?alt=media",
    "https://firebasestorage.googleapis.com/v0/b/seu-bucket/o/original%2Fimage2.png?alt=media"
  ],
  "processed_urls": [
    "https://firebasestorage.googleapis.com/v0/b/seu-bucket/o/processada%2Fimage1.png?alt=media",
    "https://firebasestorage.googleapis.com/v0/b/seu-bucket/o/processada%2Fimage2.png?alt=media"
  ]
}
```

### Códigos de Resposta:
- `200 OK`: Imagens processadas e URLs retornadas com sucesso.
- `400 Bad Request`: Arquivo ZIP inválido ou problemas com os arquivos.
- `500 Internal Server Error`: Ocorreu um erro durante o processamento das imagens ou no upload para o Firebase.

---

## Modelo de Segmentação e Contagem de Árvores

O pipeline utilizado nas rotas acima se baseia no modelo desenvolvido internamente para segmentação de imagens e contagem de árvores em imagens PNG. O modelo, implementado na classe `FilteringSegmentation`, processa as imagens para identificar e segmentar áreas que contêm árvores, retornando a imagem processada que reflete os resultados dessa contagem.

```python
from .tools.filtering_segmentation import FilteringSegmentation
```

A classe `FilteringSegmentation` é responsável por realizar o processamento das imagens e foi integrada às rotas para permitir a automatização do processo de contagem de árvores.