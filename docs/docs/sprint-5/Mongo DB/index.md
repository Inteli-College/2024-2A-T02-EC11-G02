---
title: Integração MongoDB
sidebar_position: 1
---


# Documentação de Integração com MongoDB

## Configuração do MongoDB

Para a interação com o MongoDB, utilizamos a biblioteca `pymongo` para conectar e interagir com o banco de dados. A configuração inicial da conexão é feita da seguinte forma:

```python
from pymongo import MongoClient

client = MongoClient("mongodb://root:example@localhost:27017")
db = client["analise_ambiental"]
collection = db["resultados_modelo"]
```

### Descrição dos Parâmetros de Conexão
- **URL de Conexão**: `"mongodb://root:example@localhost:27017"`
  - `root`: usuário do MongoDB.
  - `example`: senha do usuário.
  - `localhost`: endereço do servidor MongoDB.
  - `27017`: porta padrão do MongoDB.
- **Database (`analise_ambiental`)**: Banco de dados onde os resultados do processamento são armazenados.
- **Collection (`resultados_modelo`)**: Coleção dentro do banco de dados que armazena os documentos com os resultados das análises das imagens processadas.

---

## Estrutura dos Documentos Armazenados

Cada documento inserido na coleção `resultados_modelo` representa o resultado do processamento de uma imagem, contendo informações como a URL da imagem processada, a quantidade de árvores detectadas e a área estimada de vegetação. Um exemplo de documento é:

```json
{
    "modelo": "V1",
    "margem_de_erro": 25,
    "img": {
        "url_imagem_processada": "https://link_para_a_imagem_processada.png",
        "quantidade_de_arvores": 150,
        "metros_quadrados_vegetacao": 5000
    }
}
```

### Descrição dos Campos
- **`modelo`**: Versão do modelo utilizado para processamento.
- **`margem_de_erro`**: Margem de erro estimada (em percentual) para a contagem de árvores.
- **`img`**: Objeto que contém as informações da imagem processada:
  - **`url_imagem_processada`**: URL pública da imagem processada.
  - **`quantidade_de_arvores`**: Número de árvores detectadas no processamento.
  - **`metros_quadrados_vegetacao`**: Área estimada de vegetação em metros quadrados.

---

## Inserção de Documentos no MongoDB

Durante o processamento de cada imagem, um documento é criado e inserido na coleção `resultados_modelo`. A inserção é feita com o seguinte trecho de código:

```python
documento = {
    "modelo": "V1",
    "margem_de_erro": 25,  # Margem de erro em percentual
    "img": {
        "url_imagem_processada": processed_blob.public_url,
        "quantidade_de_arvores": pipeline.counted,
        "metros_quadrados_vegetacao": 5000
    }
}

# Inserir o documento na coleção
resultado = collection.insert_one(documento)
print(f"Documento inserido com ID: {resultado.inserted_id}")
```

### Descrição do Processo
1. **Criação do Documento**: O documento é montado com as informações do processamento da imagem.
2. **Inserção no MongoDB**: A função `insert_one()` é utilizada para inserir o documento na coleção.
3. **Confirmação da Inserção**: Após a inserção, o ID do documento inserido é retornado e pode ser utilizado para futuras consultas ou verificações.

---

## Uso no Endpoint `/upload_and_process/`

O endpoint `/upload_and_process/` é responsável por receber um arquivo ZIP contendo imagens, processá-las e armazenar os resultados no MongoDB. O fluxo de execução do endpoint é:

1. **Upload e Extração**: Recebe o arquivo ZIP e extrai as imagens.
2. **Processamento das Imagens**: Utiliza a classe `FilteringSegmentation` para realizar a segmentação e contagem das árvores.
3. **Armazenamento dos Resultados**: Cada imagem processada gera um documento que é inserido na coleção `resultados_modelo` no MongoDB.
4. **Retorno das URLs**: Retorna as URLs das imagens originais e processadas.

Claro, aqui está uma versão refinada do trecho, com mais detalhes e uma abordagem mais formal:

---

## Escalabilidade da Solução - Cenário Ideal

Atualmente, esta solução utiliza uma instância do MongoDB em um contêiner Docker, o que facilita a criação de um ambiente local para testes e desenvolvimento. Nesse caso, os dados são armazenados diretamente no contêiner, o que é adequado para exemplificar o funcionamento do sistema e para uso em pequenos ambientes controlados.

Para um cenário de produção escalável, recomenda-se a utilização do **MongoDB Atlas**, uma plataforma de banco de dados em nuvem gerenciada que oferece alta disponibilidade, segurança e escalabilidade. O MongoDB Atlas permite que o banco de dados seja distribuído em múltiplos datacenters, garantindo um desempenho consistente e confiável, mesmo em casos de grandes volumes de dados e altos níveis de tráfego.

### Vantagens do MongoDB Atlas em relação ao MongoDB Dockerizado
- **Alta Disponibilidade**: Implementação automática de réplicas para garantir a continuidade do serviço em caso de falhas.
- **Escalabilidade Horizontal**: Permite a adição de novos shards conforme o aumento do volume de dados e das necessidades de desempenho.
- **Backup Automatizado e Recuperação de Desastres**: Garante a integridade dos dados e facilita a restauração em situações de falhas.
- **Segurança Integrada**: Inclui recursos como criptografia de dados em trânsito e em repouso, controle de acesso detalhado, e integração com redes privadas virtuais (VPNs).
- **Facilidade de Gestão**: Interface amigável para monitoramento de desempenho, ajustes de configurações e análise de uso, permitindo uma administração mais eficiente do banco de dados.

Ao migrar para o MongoDB Atlas, é possível manter as mesmas funcionalidades desenvolvidas nesta arquitetura, com a vantagem de um ambiente altamente disponível e preparado para crescer conforme a demanda do projeto.