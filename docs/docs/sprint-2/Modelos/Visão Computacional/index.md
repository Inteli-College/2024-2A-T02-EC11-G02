---
title: Visão Computacional
sidebar_position: 1
---

A fim de solucionar o principal problema apresentado pelo parceiro de projeto — a contagem de árvores por meio de imagens de satélite ou drone —, é possível a utilização de modelos de visão computacional pré-treinados para a identificação de objetos específicos, a exemplo do Yolo e do Deep Forest. Uma das abordagens utilizadas, nesse cenário, foi o [Deep Forest](https://www.weecology.org/software-projects/deepforest/).

### Deep Forest

DeepForest é uma biblioteca Python para treinamento e predição de objetos ecológicos em imagens aéreas. Ela oferece modelos pré-construídos para uso imediato, além de permitir o ajuste fino com anotações e treinamento de modelos personalizados. Os modelos do DeepForest podem ser estendidos para a classificação de espécies com base em novos dados. A biblioteca foi projetada para pesquisadores com pouca experiência em aprendizado de máquina, aplicações com dados limitados que podem usar modelos pré-construídos e cientistas que buscam uma linha de base fácil de usar para comparação de métodos. O DeepForest utiliza redes de detecção de objetos por aprendizado profundo para prever a localização de objetos ecológicos em imagens aéreas, sendo desenhada para ser simples, modular e reprodutível.

Para a implementação inicial do modelo Deep Forest, foi criado um arquivo <code>.ipynb</code> cujo código foi dividido em diferentes etapas: carregamento das imagens que seriam, posteriormente, submetidas ao modelo; redimensionamento das imagens; normalização das imagens; carregamento do modelo; implementação do modelo e output. O modelo, por fim, retornou as imagens submetidas com cada árvore identificada marcada por um retângulo, apresentando também o total de árvores detectadas. Ao final do output, é possível visualizar, também, a quantidade total de árvores identificadas em todo o dataset.

Abaixo, é possível visualizar algumas das imagens retornadas pelo modelo:

![1](/img/deepforest_1.png)
![2](/img/deepforest_2.png)
![3](/img/deepforest_3.png)

As imagens utilizadas foram disponibilizadas pelo parceiro, embora seja possível realizar testes com datasets mais amplos.