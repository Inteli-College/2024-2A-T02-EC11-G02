---
title: Desenvolvimento Back-End
sidebar_position: 1
---

# Documentação do Backend para Processamento de Imagem com Firebase

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