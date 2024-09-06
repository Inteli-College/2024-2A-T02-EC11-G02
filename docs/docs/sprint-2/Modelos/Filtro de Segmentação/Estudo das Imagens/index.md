---
title: Ánalise das Imagens
sidebar_position: 0
---

Este documento apresenta as investigações e transformações realizadas para identificar as características mais relevantes das imagens que podem ser úteis para o modelo. O objetivo é aprimorar a compreensão e otimizar o uso dessas características.

# Imagens Analisadas

Utilizamos tanto as imagens de drones fornecidas pelo nosso parceiro quanto [datasets de satelite](https://www.kaggle.com/datasets/mskorski/tree-counting-image-dataset).


## Transformações 

Começamos analisando cada canal (RGB) de cor.

**Proximidades da Aurora Verde**

![1](/img/filter_segmtation/01.png)
**Aurora Verde**
![2](/img/filter_segmtation/02.png)
**Ibirapuera**
![3](/img/filter_segmtation/03.png)

Com base nessas três imagens de locais distintos, além de outras 15 analisadas, foi possível observar um padrão na tonalidade das imagens. Há um realce mais pronunciado nas regiões de vegetação em um canal de cor específico.

Diante dessa hipótese, desenvolvi rapidamente um código que aplica filtros de **Curves** e **Levels** para acentuar ainda mais esse realce nas regiões de vegetação. Chegando nos seguintes resultados:

### Proximidades da Aurora Verde
![4](/img/filter_segmtation/04.png)
### Aurora Verde
![5](/img/filter_segmtation/05.png)
### Ibirapuera
![6](/img/filter_segmtation/06.png)

### Filtro de Levels aplicado em python
![code-01](/img/filter_segmtation/code01.png)

### Filtro de Curves aplicado em python
![code-02](/img/filter_segmtation/code02.png)

A partir desse ponto, percebi a possibilidade de abordar o problema por outro caminho. Após a leitura de alguns artigos acadêmicos, descobri uma área da computação gráfica focada na detecção de objetos por meio de filtros.

# Filters and Segmentation

A área de **Filtros e Segmentação** na computação gráfica é voltada para a detecção e separação de objetos em imagens com base em características visuais, como cor, textura, bordas e formas.

Os filtros, como aqueles aplicados em diferentes canais de cor ou em frequências espaciais, são usados para realçar detalhes específicos das imagens. Por exemplo, filtros de borda, como Sobel ou Canny, podem destacar contornos, enquanto filtros de suavização podem remover ruídos.

Já a segmentação é o processo de dividir uma imagem em regiões distintas, agrupando pixels com propriedades semelhantes. Técnicas comuns incluem a segmentação por limiar, onde regiões são separadas com base em valores de cor ou intensidade, e métodos mais avançados como a segmentação por agrupamento ou aprendizado profundo, usados para identificar e classificar objetos em imagens complexas.

