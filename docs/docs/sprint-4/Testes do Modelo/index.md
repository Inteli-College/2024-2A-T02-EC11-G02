---
title: Testes do Modelo
sidebar_position: 3
---

O modelo de visão computacional desenvolvido aplica técnicas de filtragem e segmentação para analisar imagens de áreas florestais. Utilizando uma série de funções que empregam diferentes filtros, o objetivo é tornar possível a distinção precisa entre as árvores presentes nas imagens. O processo de análise segue as seguintes etapas:

- Conversão da imagem para a escala de cinza, facilitando a análise dos canais de cor;

- Seleção do canal de cor que apresenta maior brilho, destacando as regiões das árvores em relação ao fundo;

- Aplicação de uma máscara para remover o fundo da imagem.

Após a aplicação dessas etapas, o sistema executa uma função que detecta e identifica os segmentos correspondentes às árvores, desenhando retângulos ao redor dessas áreas. Com isso, o modelo realiza a contagem dos retângulos, que representam as árvores identificadas. Ao final, a função retorna tanto a imagem original com os retângulos sobrepostos quanto a imagem com a máscara aplicada, permitindo visualizar como a segmentação foi realizada.

Para avaliar a precisão da contagem de segmentos utilizando o pipeline desenvolvido, foram realizados testes manuais. Uma imagem foi escolhida para que as árvores pudessem ser contadas visualmente, sem a necessidade de automatização. Nesta imagem, cada árvore foi marcada manualmente com um ponto, representando o cenário ideal esperado após o processamento. Sabendo-se que os pontos foram desenhados manualmente e são completamente distinguíveis entre si, a função que realiza a contagem de segmentos retornou a quantidade de árvores da imagem com exatidão. Desse modo, seria possível comparar com o resultado retornado quanto o processo de segmentação é automatizado, a fim de averiguar a assertividade do modelo.

Abaixo, é possível observar a imagem processada manualmente (com as árvores completamente distinguíveis) e a imagem processada pelo pipeline (com árvores segmentadas, mas com pequenas interseções que podem impactar a precisão da contagem).


Imagem original:

![imagem-original](/img/imagem_teste.png)


Imagem com segmentação preparada manualmente:

![segmentacao-manual](/img/manual_counting.png)


Imagem com segmentação preparada por pipeline de pré-processamento:

![segmentacao-pipeline](/img/pre_processing.png)


Contagem de árvores na primeira imagem:

![teste-ideal](/img/teste_modelo_ideal.png)


Contagem de árvores na segunda imagem:

![teste-modelo](/img/teste_modelo.png)


Conforme os retornos apresentados pelo modelo, a região considerada na imagem possui 1219 árvores, enquanto 1681 segmentos são contabilizados quando a imagem submetida passa pelo pré-processamento definido. É possível afirmar, para o exemplo em questão, que o modelo apresentou assertividade de, aproximadamente, 73%.
