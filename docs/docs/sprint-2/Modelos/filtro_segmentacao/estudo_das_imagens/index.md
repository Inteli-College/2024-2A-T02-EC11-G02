---
title: Ánalise das Imagens
sidebar_position: 0
---

# Configuração Inicial da Raspberry Pi 5 para IoT

## Descrição
Estudo das imagens fornecidas pelo parceiro e das imagens de satélite.

### Detalhes da Configuração

- **Sistema Operacional**: Ubuntu para Raspberry Pi
  - A imagem do Ubuntu foi baixada e gravada em um cartão microSD utilizando o Raspberry Pi Imager.
  - Após a inserção do cartão microSD na Raspberry Pi 5, foi realizada a configuração inicial do sistema, incluindo configuração de conexão à internet.
  - O sistema foi atualizado para garantir que todos os pacotes estivessem na versão mais recente.

- **Ambiente de Programação**:
  - **Instalação do VSCode**:
    - Ambiente de programação para utilizar o IOT.

## GPS - GY-GPS6MV2 (Descontinuidade)

Durante a tentativa de utilização do módulo GPS GY-GPS6MV2 com a Raspberry Pi 5, o dispositivo não funcionou como esperado. O problema identificado foi a ausência de um circuito intermediário para alinhar e filtrar as frequências do sinal do GPS, algo necessário para garantir o funcionamento do dispositivo.

- **Tentativas de Solução**:
  - Foi considerada a utilização de um Arduino ou ESP32 como controlador externo para o GPS, com o objetivo de realizar o processamento dos sinais antes de enviá-los para a Raspberry Pi. No entanto, essa abordagem foi descartada..

### Motivos da Descontinuidade do Uso do GPS

O grupo decidiu descontinuar o foco na integração do módulo GPS GY-GPS6MV2 por vários motivos:

- **Indisponibilidade do circuito na Faculdade**: A Faculdade não tinha a aquisição do cirtuito para dar continuidade do desenvolvimento.

- **Aumento do Custo**: A adição de componentes como Arduino ou ESP32, elevaria os custos do projeto.

- **Aumento da Complexidade da Arquitetura**: A inclusão de dispositivos adicionais na arquitetura aumentaria significativamente a complexidade do projeto, exigindo mais tempo e recursos para integração e testes.

- **Prazo Curto**: Dado o tempo limitado disponível para o desenvolvimento do projeto (10 semanas), a equipe optou por concentrar esforços em outras áreas críticas da solução IoT (IA, Front-end e Back-end), evitando o risco de atrasos que poderiam comprometer o sucesso do projeto.

- **Redundância**: As mesmas informações que seriam utilizadas do sensor de GPS, podem ser também consultadas diretamente do Google Maps de forma manual.