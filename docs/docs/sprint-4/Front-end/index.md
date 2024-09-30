---
title: Front-end
sidebar_position: 2
---

# Front-end: Interface do Usuário

Este projeto trata-se de um sistema de processamento de imagens de árvores em áreas florestais. O frontend, como parte da aplicação, é responsável por receber as imagens de sensores IoT ou através de uploads feitos pelos usuários, e enviá-las ao backend para processamento. Após o processamento, o sistema retorna a imagem segmentada e informa a contagem de árvores identificadas. Essas informações são, então, adicionadas a um histórico para posterior consulta, incluindo métricas como número de árvores e áreas cobertas por vegetação.

# Funcionalidades Principais

**Recepção de Imagens:**
O sistema permite a inserção de imagens de duas formas:
Upload manual feito pelo usuário através da interface.
Upload automático de imagens capturadas por sensores IoT.

**Envio ao Backend:**
Após o upload, as imagens são enviadas automaticamente para o backend, onde ocorrem os processamentos de segmentação e contagem de árvores.
Processamento de Imagens:
O backend realiza a análise da imagem enviada, identificando e segmentando as árvores na imagem. Com base nessa segmentação, o sistema também realiza a contagem das árvores presentes.
Exibição dos Resultados:
Uma vez processadas, as imagens retornam ao frontend com as árvores destacadas e o número de árvores identificadas. O usuário poderá visualizar a imagem original lado a lado com a imagem segmentada, facilitando a comparação.

**Histórico e Métricas:**
As imagens processadas, junto com as métricas (como número de árvores, data de envio e área de cobertura), são armazenadas em um histórico acessível ao usuário. Isso permite que ele acompanhe a evolução ao longo do tempo e faça comparações entre diferentes áreas monitoradas.

# Fluxo de Uso

O usuário acessa a interface e faz o upload manual da imagem ou aguarda a chegada automática de imagens do sistema IoT.
As imagens são enviadas ao backend, que realiza o processamento.
O sistema retorna ao usuário a imagem segmentada e a contagem de árvores, exibindo os dados na interface.
A imagem e as métricas são armazenadas no histórico, onde o usuário pode consultar resultados de imagens anteriores e as informações associadas.

**Histórico de Processamento**

Cada imagem processada possui um conjunto de informações associadas que são armazenadas no histórico do usuário. As principais métricas incluem:

Data de Processamento: Data e hora em que a imagem foi enviada e processada.
Número de Árvores: Contagem de árvores identificadas na imagem.
Área Coberta: Área florestal detectada, permitindo um acompanhamento do estado das matas ao longo do tempo.
Interface do Usuário

A interface do usuário é amigável e intuitiva, possibilitando:

Visualização simultânea das imagens originais e processadas.
Acesso rápido às métricas e resultados do processamento.
Consulta ao histórico com facilidade, através de filtros por data, quantidade de árvores ou área de cobertura.