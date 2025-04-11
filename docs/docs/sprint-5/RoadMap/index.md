---
title: Road Map
sidebar_position: 2
---

## Roadmap da Solução

O roadmap deste projeto destaca os principais desenvolvimentos, bem como as funcionalidades que foram planejadas, mas acabaram descontinuadas por limitações de tempo e recursos. Abaixo, detalhamos dois pontos que, embora não tenham sido finalizados, possuem potencial para futuras melhorias: a integração do módulo GPS e a implementação de um serviço de mensageria.

### GPS - GY-GPS6MV2 (Descontinuidade)

Durante a tentativa de utilização do módulo GPS GY-GPS6MV2 com a Raspberry Pi 5, o dispositivo não funcionou como esperado. O problema identificado foi a ausência de um circuito intermediário para alinhar e filtrar as frequências do sinal do GPS, algo necessário para garantir o funcionamento do dispositivo.

- **Tentativas de Solução**:
  - Foi considerada a utilização de um Arduino ou ESP32 como controlador externo para o GPS, com o objetivo de realizar o processamento dos sinais antes de enviá-los para a Raspberry Pi. No entanto, essa abordagem foi descartada devido a limitações de tempo e complexidade.

#### Motivos da Descontinuidade do Uso do GPS

O grupo decidiu descontinuar a integração do módulo GPS GY-GPS6MV2 por diversos motivos:

- **Indisponibilidade do Circuito**: A instituição não dispunha do circuito intermediário necessário para filtrar os sinais do GPS, impossibilitando a continuidade dos testes.
- **Aumento do Custo**: A adição de componentes como Arduino ou ESP32 aumentaria o custo do projeto, o que não era viável dentro das restrições orçamentárias.
- **Complexidade da Arquitetura**: Incluir um microcontrolador adicional como intermediário no processamento dos sinais do GPS aumentaria a complexidade do projeto, demandando mais tempo para a integração e a realização de testes.
- **Prazo Curto**: Com apenas 10 semanas para desenvolver a solução completa, a equipe optou por focar em outras áreas críticas, como Inteligência Artificial, Front-end e Back-end, para garantir a entrega dentro do prazo.
- **Redundância de Informações**: As informações de localização que o módulo GPS forneceria podem ser obtidas manualmente através de APIs de mapas, como o Google Maps, em situações onde a precisão do GPS integrado não é essencial.

### Mensageria - RabbitMQ (Funcionalidade a Ser Implementada)

Uma outra funcionalidade que poderia melhorar a escalabilidade e a arquitetura da solução seria a implementação de um sistema de mensageria utilizando **RabbitMQ**. A utilização de um broker de mensagens permitiria uma comunicação mais eficiente entre os diferentes serviços da solução, facilitando o processamento assíncrono e a distribuição de tarefas.

- **Potenciais Benefícios do RabbitMQ**:
  - **Processamento Assíncrono**: Permite que operações intensivas (como processamento de imagens e cálculos de IA) sejam processadas de forma assíncrona, liberando recursos para outras operações.
  - **Escalabilidade**: Facilita a adição de novos consumidores e produtores de mensagens, permitindo que a solução cresça conforme a demanda.
  - **Desacoplamento de Serviços**: Possibilita uma arquitetura mais desacoplada, onde cada componente pode operar de forma independente, melhorando a manutenção e a robustez do sistema.
  - **Resiliência**: Reduz o risco de perda de mensagens durante a comunicação entre serviços, garantindo que nenhuma tarefa crítica seja perdida em casos de falhas temporárias de rede.
  - **Administração de Altas Demandas**: Amortecimento de requisições no Backend quando existe um pico de demandas.


#### Motivos da Não Implementação Imediata

- **Tempo Limitado**: A complexidade de integrar um sistema de mensageria demandaria mais tempo de desenvolvimento e testes, algo que não era possível dentro do prazo de 10 semanas.
- **Recursos de Hardware**: O uso de RabbitMQ em ambientes de produção exige recursos de hardware adicionais e uma configuração adequada, que não estavam disponíveis durante o desenvolvimento inicial.
- **Foco em Funcionalidades Críticas**: Dada a prioridade de funcionalidades críticas como a Inteligência Artificial para contagem de árvores e a interface do usuário, a implementação do RabbitMQ foi adiada para uma versão futura da solução.