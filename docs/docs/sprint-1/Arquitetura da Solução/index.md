---
title: Arquitetura da Solução
sidebar_position: 1
---

Uma vez realizada a elicitação de requisitos do projeto, foi elaborada a versão inicial da arquitetura proposta pelo grupo. Para melhor visualizar os diferentes componentes da solução, foi feito um diagrama de blocos — que demonstra, em alto nível, o fluxo pelo qual a solução deverá passar para operar de forma bem-sucedida. Abaixo, é possível consultar o diagrama.

![diagrama-blocos](/img/arquitetura_g2.drawio.png)

## Fluxo da solução

A solução seguirá o seguinte fluxo: os sensores correspondentes ao GPS e à câmera serão conectados ao microcontrolador Raspberry Pi, o qual será acoplado ao drone. O GPS será responsável pela captura dos dados de localização das árvores, enquanto a câmera será responsável por capturar as imagens das árvores. Os dados de localização serão armazenados em um banco não relacional em nuvem, já no back-end da solução. As imagens geradas pelo drone, por outro lado, serão submetidas ao modelo de visão computacional em execução no microcontrolador, o qual deverá processá-la, realizar o processo de identificação das árvores e retornar as imagens processadas. As imagens processadas pelo modelo serão enviadas para um bucket, também em cloud, no back-end do projeto. Será desenvolvida uma API capaz de interagir com os dados produzidos, os quais poderão ser transformados em diferentes visualizações para que sejam apresentados em um dashboard destinado aos clientes da Abundance. Espera-se que o dashboard possa ser integrado à plataforma da Abundance para os clientes que adquirem tokens.