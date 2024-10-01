---
title: Arquitetura e Considerações sobre o Back-end
sidebar_position: 2
---

## Desafios na Implementação de Testes de Carga com Locust

O projeto enfrenta algumas limitações que tornam o uso do Locust para testes de carga inviável, principalmente devido às características da rota de processamento de imagem, à conexão com o Firebase e ao poder de processamento do back-end.

### 1. Rota de Processamento de Imagem

A rota responsável pelo processamento de imagens realiza contagens de árvores a partir de cada arquivo processado. Esse processo envolve os seguintes desafios:

- **Tempo de Processamento Variável**: O tempo necessário para processar uma imagem depende da quantidade de fotos enviadas para análise. Quanto maior o número de imagens, maior o tempo de processamento.
- **Impacto nos Testes de Carga**: Como os tempos de resposta podem variar consideravelmente, testar a capacidade do sistema em lidar com múltiplas requisições simultâneas se torna difícil de avaliar de forma consistente com o Locust. Esse comportamento variável torna a simulação de cargas irrealista, uma vez que não há previsibilidade no tempo de execução das tarefas.

### 2. Conexão com o Firebase

A integração com o Firebase foi realizada da seguinte forma:

- **Credenciais no Arquivo `.env`**: As credenciais sensíveis, como as chaves de acesso ao Firebase, foram armazenadas em um arquivo `.env`, permitindo que as variáveis sejam acessadas de forma segura no ambiente de execução.
- **Autenticação via JSON**: Além das variáveis de ambiente, algumas informações de autenticação foram configuradas através de um arquivo JSON específico que contém os dados necessários para estabelecer a conexão com o Firebase.
  
### 3. Poder de Processamento do Back-End

A rota de processamento de imagem foi arquitetada para ser consumida poucas vezes durante o dia. Esse design foi influenciado pelas seguintes considerações:

- **Baixa Frequência de Uso**: O back-end foi pensado para processar um número limitado de requisições por dia, refletindo um uso moderado da rota.
- **Arquitetura Sem Mensageria**: Devido à baixa expectativa de tráfego, a implementação não incluiu o uso de sistemas de mensageria e amortecimento como o **Kafka**. A adição de um sistema de mensageria traria complexidade adicional, sem uma real necessidade para o volume atual de requisições.
  
### Problemas Identificados:
- **Limitação no Teste de Autenticação**: A utilização de credenciais em um arquivo `.env`, combinada com as informações adicionais no arquivo JSON, dificulta a automação de testes de carga que envolvem múltiplas autenticações, uma vez que essas informações precisam ser manipuladas cuidadosamente para cada sessão de teste.
