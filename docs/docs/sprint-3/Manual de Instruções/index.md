---
title: Desenvolvimento Back-End
sidebar_position: 2
---

# Manual de Implementação do Projeto: Contagem de Árvores com Visão Computacional

## 1. Visão Geral
Este projeto visa desenvolver um sistema de contagem de árvores utilizando técnicas de visão computacional e IOT. O backend foi implementado em Python com FastAPI. As imagens gerados por uma câmera são processadas e armazenadas no Firebase Storage, e os links gerados são salvos em um banco de dados MongoDB.

## 2. Requisitos

### 2.1 Requisitos de Hardware
- Microcomputador conectado a uma câmera para registrar imagens.
- Servidor Backend para processar as imagens.

### 2.2 Requisitos de Software
- Python
- FastAPI
- Uvicorn
- MongoDB
- Firebase Admin SDK
- Ubuntu (MicroComputador - SO)
- Docker (Aplicativo)

## 3. Instalação

### 3.1 Clonando o Repositório
```bash
git clone https://github.com/Inteli-College/2024-2A-T02-EC11-G02.git
cd cd 2024-2A-T02-EC11-G02
```

### 3.2 Configuração do Ambiente
Instale as dependências necessárias:
```bash
cd src/backend/
pip install -r requirements.txt
```

### 3.3 Configurando Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto (`./backend`) com as seguintes variáveis:
```bash
MONGODB_URI=mongodb://seu_usuario:sua_senha@localhost:27017/contagem_arvores
FIREBASE_STORAGE_BUCKET="grupo2-93568.appspot.com"
FIREBASE_KEY_PATH="grupo2-93568-firebase-adminsdk-ck9m1-0d01c16655.json"
```

### 3.4 Configurando Firebase
- Baixe as credenciais do Firebase como arquivo JSON e salve-o como `firebase_credentials.json`.

## 4. Execução do Projeto (Para Dev)

### 4.1 Executando o Servidor
Inicie o servidor FastAPI com Uvicorn:
```bash
uvicorn app.main:app --reload
```

### 4.2 Testando a API
Após iniciar o servidor, as rotas da API estarão disponíveis em `http://localhost:8000`. Use ferramentas como `Postman` ou `cURL` para testar as seguintes rotas:

- **Upload de Imagens para Processamento**:  
  `POST /modelversion`  
  Envia uma imagem para o servidor, que será processada para contagem de árvores e retorna a imagem processada para o cliente.
  
## 4. Execução do Projeto (Para Prod)

### 4.1 Usando Docker para Executar o Projeto

#### 4.1.1 Build da Imagem Docker
Para evitar a necessidade de instalação manual das dependências, você pode construir uma imagem Docker do projeto. Certifique-se de que o `Dockerfile` está configurado corretamente. 

Para construir a imagem, execute o seguinte comando na raiz do projeto `./backend` onde se encontra o arquivo `Dockerfile`:

```bash
docker build -t contagem-arvores:v1 .
```

## 5. Estrutura do Projeto

```text
.
.
.
src/
├── backend/
│   ├── routers/
│   │   ├── code/
│   │   │   ├── modelVersion.py   # Lógica para contagem de árvores e processamento
│   │   │   └── saveImage.py      # Lógica para salvar imagens no Firebase
│   │   └── __pycache__/          # Cache de Python (gerado automaticamente)
│   └── __pycache__/              # Cache de Python (gerado automaticamente)
├── .env                          # Arquivo de configuração com variáveis de ambiente
├── .gitignore                    # Arquivo de exclusão para Git
├── dockerfile                    # Arquivo Docker para configurar o ambiente
├── grupo2-93568-firebase-adminsdk.json  # Credenciais Firebase
├── main.py                       # Ponto de entrada da aplicação
└── requirements.txt              # Dependências do projeto

```

## 6. Fluxo de Funcionamento

1. **Upload de Imagem**: O cliente faz o upload de uma imagem via API, que será processada pelo modelo de visão computacional.
2. **Processamento**: A imagem é analisada pelo modelo de contagem de árvores e o resultado é salvo no Firebase Storage.
3. **Salvar Resultados**: Os links das imagens processadas são salvos no MongoDB para referência futura.
4. **Recuperação**: O cliente pode consultar o link da imagem processada e a contagem de árvores pela API ou diretamente pelo Dashboard Desenvolvido.