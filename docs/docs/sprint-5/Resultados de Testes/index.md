---
title: Resultados de Testes
---

# Resultados de Testes

Este documento apresenta os resultados dos testes realizados na solução desenvolvida, abordando os **Testes de Carga** e os **Testes do Modelo de Visão Computacional**. As análises foram conduzidas para garantir a adequação da solução ao seu uso esperado, com foco em eficiência e precisão.

## Testes de Carga

### Introdução

Os testes de carga são frequentemente aplicados em sistemas que processam um grande volume de requisições em intervalos curtos de tempo. No entanto, considerando o perfil da solução desenvolvida, que será utilizada periodicamente e com um volume reduzido de requisições, optou-se por não realizar testes de carga nesta fase.

### Análise do Sistema

O fluxo atual da solução envolve a captura de imagens por uma câmera, que são então compactadas, enviadas para o back-end e processadas pelo modelo de visão computacional conforme a demanda. Após análise do comportamento esperado dos usuários e do perfil da aplicação, a equipe concluiu que as rotas do back-end não serão sobrecarregadas durante o uso regular da solução. Não são previstos picos significativos de acesso ou grandes volumes de requisições simultâneas.

Dado o perfil de uso da solução e a ausência de requisitos críticos relacionados à escalabilidade, os testes de carga são considerados desnecessários nesta fase do projeto. No entanto, caso o escopo da solução ou o volume de usuários aumente, a necessidade de testes de carga será reavaliada para garantir o desempenho adequado em cenários futuros.

---

## Testes do Modelo de Visão Computacional

### Introdução

O modelo de visão computacional desenvolvido é responsável por analisar imagens de áreas florestais, utilizando técnicas de filtragem e segmentação para identificar e contar árvores. Esta seção descreve o pipeline de processamento utilizado e os resultados obtidos com os testes realizados para avaliar a precisão do modelo.

### Pipeline de Processamento

O modelo segue as seguintes etapas para processar as imagens:

1. **Conversão para escala de cinza**: Simplifica a análise dos canais de cor.
2. **Seleção do canal de maior brilho**: Destaca as regiões das árvores em relação ao fundo.
3. **Aplicação de máscara**: Remove o fundo da imagem, isolando as árvores.

Após essas etapas, o sistema detecta os segmentos correspondentes às árvores e desenha retângulos ao redor delas. O modelo então realiza a contagem das árvores com base nos segmentos identificados.

### Testes Manuais

Para avaliar a precisão do modelo, foi realizada a contagem manual das árvores em uma imagem de teste. Cada árvore foi marcada manualmente, representando o cenário ideal esperado após o processamento. Em seguida, a imagem foi processada automaticamente pelo pipeline, e os resultados das contagens manuais e automáticas foram comparados.

#### Imagens de Referência

- Imagem original: ![imagem-original](/img/imagem_teste.png)
- Segmentação manual: ![segmentacao-manual](/img/manual_counting.png)
- Segmentação pelo pipeline: ![segmentacao-pipeline](/img/pre_processing.png)

### Resultados

Na comparação entre as contagens manuais e as geradas pelo modelo:

- Contagem manual: **1219 árvores**
- Contagem pelo modelo: **1681 segmentos**

A precisão do modelo foi calculada em **aproximadamente 73%**, com base na discrepância entre a contagem manual e os segmentos detectados automaticamente.

Embora o modelo tenha demonstrado uma precisão razoável, pequenas interseções entre os segmentos podem impactar a contagem final. Testes adicionais e ajustes no pipeline poderão melhorar a assertividade do modelo, tornando-o mais eficaz para aplicações que exigem maior precisão.

---

## Tabelas de Resultados

| Imagem       | Contagem Manual | Contagem do Algoritmo |
|--------------|-----------------|-----------------------|
| 01_test      | 1219            | 1419                  |
| 02_test      | 762             | 830                   |
| 03_test      | 236             | 290                   |

Cada linha da tabela representa uma imagem diferente utilizada nos testes. A coluna Contagem Manual indica o número de árvores contadas manualmente por especialistas, enquanto a coluna Contagem do Algoritmo mostra a quantidade de segmentos detectados automaticamente pelo modelo após o processamento das imagens.

### Interpretação dos Resultados
Imagem 01_test:
Contagem Manual: 1219 árvores
Contagem pelo Algoritmo: 1419 segmentos
A diferença observada de 200 segmentos a mais indica que o algoritmo identificou mais elementos na imagem do que as árvores reais contadas manualmente. Esse excesso pode ser resultado de sobreposições de segmentos ou falsos positivos, onde o algoritmo interpretou outras características da imagem, como sombras ou áreas densamente florestadas, como árvores adicionais.

Imagem 02_test:
Contagem Manual: 762 árvores
Contagem pelo Algoritmo: 830 segmentos
A diferença de 68 segmentos também sugere que o modelo identificou elementos adicionais que não correspondem a árvores reais. Novamente, fatores como a densidade das árvores e variações nas características visuais (como iluminação e contraste) podem ter causado essa discrepância.

Imagem 03_test:
Contagem Manual: 236 árvores
Contagem pelo Algoritmo: 290 segmentos
Neste caso, o algoritmo detectou 54 segmentos a mais do que o número real de árvores. Assim como nas outras imagens, a presença de ruído visual ou a falha na distinção entre árvores individuais em áreas sobrepostas podem ter causado essa variação.

Conclusões da Análise
Precisão Média: A diferença geral entre a contagem manual e a contagem automática revela que o modelo tem uma precisão média de aproximadamente 73%, como calculado anteriormente. Apesar de detectar com sucesso uma grande parte das árvores, o modelo apresenta uma tendência a contar elementos adicionais, o que sugere que ele pode estar superestimando o número de árvores em imagens com características mais complexas.

Falsos Positivos: Em todas as imagens, houve um aumento na contagem gerada pelo algoritmo em comparação à contagem manual, o que indica a presença de falsos positivos. Isso pode ser causado por imperfeições no processo de segmentação, onde o modelo pode interpretar regiões não correspondentes como árvores.

Possíveis Melhorias: Para aumentar a precisão, é possível ajustar o pipeline de processamento de imagens, como refinar os critérios de segmentação e implementar filtros mais robustos para distinguir melhor as árvores de outros elementos visuais, como sombras ou folhagens densas. Testes adicionais com uma base de dados maior e mais variada também podem ajudar a melhorar o modelo.

Em resumo, a tabela reflete uma visão quantitativa sobre o desempenho atual do modelo de visão computacional, destacando tanto sua capacidade de detectar árvores quanto as áreas onde ajustes são necessários para reduzir falsos positivos e melhorar a precisão geral.

---

## Considerações Finais

Os testes realizados indicam que, embora a solução não exija testes de carga nesta fase, sua precisão em contagem de árvores pode ser melhorada. A análise do pipeline de visão computacional revelou uma precisão de 73%, destacando o potencial de otimização futura. A reavaliação do modelo pode ser necessária em caso de mudanças no escopo ou no perfil de uso da solução.
