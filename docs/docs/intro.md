---
sidebar_position: 1
---

# Introdução

O projeto foi realizado em parceria com a Abundance, uma Climate-Tech focada em impulsionar a restauração ambiental por meio do Abundance Token, do Ecossistema ESG e da Educação. A empresa tem como propósito a preservação de regiões florestais, por meio da tokenização dos ativos ambientais presentes nesse ecossistema. Cada árvore plantada pela Abundance está atrelada a uma representação digital por meio de um token registrado na Blockchain. Desse modo, busca-se contribuir para a transição rumo a uma economia sustentável.

Uma das principais dificuldades enfrentadas pela Abundance está relacionada ao atual processo de monitoramento das regiões florestais sob sua gestão. Um dado essencial, tanto para a empresa quanto para seus clientes, é a quantidade de árvores plantadas pela iniciativa, uma vez que isso reforça a transparência e a robustez do processo de monitoramento e controle de informações, o que é crucial para a obtenção de determinadas certificações. Dessa forma, foi concebida uma solução que utiliza um modelo de visão computacional para realizar a contagem de árvores, por meio de um sistema embarcado acoplável a drones capaz de capturar imagens das regiões de plantio da empresa. Por meio de uma aplicação robusta, o parceiro será capaz de submeter imagens de diferentes origens — tanto de drones, quanto de satélites — a um modelo que utiliza a técnica de filtragem e segmentação para contabilizar os ativos florestais presentes no local. Espera-se contribuir, portanto, para o aprimoramento do processo de contagem de árvores, até então realizado manualmente, de modo a reforçar a transparência de informações relacionadas ao principal ativo com o qual a Abundance trabalha.

## Sprint I

A primeira sprint do projeto foi dedicada ao entendimento inicial da proposta apresentada pelo parceiro de projeto do atual módulo: a Abundance. A partir da introdução ao problema a ser solucionado, foi possível desenvolver uma versão inicial da arquitetura da solução, refletir e discorrer sobre aspectos éticos relacionados ao projeto, realizar a elicitação de requisitos funcionais e não funcionais e elaborar a proposta de valor da solução. Abaixo, é possível conferir a apresentação desenvolvida com a finalidade de validar os elementos mencionados com o parceiro após as duas primeiras semanas do projeto.

[Link da Apresentação](https://www.canva.com/design/DAGNpmUOvWY/Gw6Dxmuhb92pNnTuBn0p7w/view?utm_content=DAGNpmUOvWY&utm_campaign=designshare&utm_medium=link&utm_source=editor)


<iframe loading="lazy"
    style={{ display: 'block', margin: 'auto', width: '100%', height: '66vh' }}
    src="https:&#x2F;&#x2F;www.canva.com&#x2F;design&#x2F;DAGNpmUOvWY&#x2F;sLBiKmd1eifRcLapwvwGMQ&#x2F;view?embed">
</iframe>

## Sprint II

Na segunda sprint do projeto, após uma melhor compreensão acerca das expectativas do parceiro quanto à solução a ser entregue, o grupo se dedicou a iniciar os artefatos técnicos, assim como uma análise que reflete o impacto da iniciativa em caráter político, econômico, social, tecnológico, ecológico e legal. Diferentes técnicas de pré-processamento de imagens foram desenvolvidas e testadas. Além disso, foram explorados diferentes modelos de visão computacional pré-treinados, a exemplo do Yolo e do Deep Forest. Por fim, foram feitos a configuração inicial do back-end, um wireframe que reflete a interface a ser entregue para o parceiro e avanços na parte de IoT.

[Link da Apresentação](https://www.canva.com/design/DAGOq_xx3ew/MySbNL7Xq7jQawBKOJSjwg/view?utm_content=DAGOq_xx3ew&utm_campaign=designshare&utm_medium=link&utm_source=editor)

<iframe loading="lazy"
    style={{ display: 'block', margin: 'auto', width: '100%', height: '66vh' }}
    src="https:&#x2F;&#x2F;www.canva.com&#x2F;design&#x2F;DAGOq_xx3ew&#x2F;CoKnZH9W0i4J-JkrzlFbrQ&#x2F;view?embed">
</iframe>

## Sprint III

A terceira sprint do projeto foi dedicada ao refinamento do modelo de visão computacional a ser utilizado na solução, bem como à continuidade do desenvolvimento do back-end e das telas da interface gráfica destinada ao parceiro. No que concerne ao modelo, a técnica de filtragem e segmentação empregada passou por uma fase de otimização, a fim de que a contagem de árvores para imagens de drone e satélite se tornasse mais precisa. Além disso, o modelo pré-treinado do Deep Forest permaneceu como uma opção válida para outros tipos de imagem. O sistema embarcado também obteve progresso, uma vez que foi configurado o módulo da câmera responsável pela captura de imagens. A entrega da sprint também conta com uma matriz de riscos e oportunidades.

[Link da Apresentação](https://www.canva.com/design/DAGQSCSuBtE/6tyOzo8CLOO-KwYEjYuZBQ/view?utm_content=DAGQSCSuBtE&utm_campaign=designshare&utm_medium=link&utm_source=editor)

<iframe loading="lazy"
    style={{ display: 'block', margin: 'auto', width: '100%', height: '66vh' }}
    src="https:&#x2F;&#x2F;www.canva.com&#x2F;design&#x2F;DAGQSCSuBtE&#x2F;k_o24i_FEs8oyepbN0qYOw&#x2F;view?embed">
</iframe>

## Sprint IV

Na quarta sprint do projeto, foi produzida uma análise financeira, a fim de que fosse possível estabelecer uma previsão do investimento necessário para a implementação da solução na rotina da empresa. Além disso, a equipe de desenvolvimento focou em refinar o pipeline de pré-processamento das imagens submetidas ao modelo de visão computacional. O back-end da aplicação foi finalizado e as telas do front-end foram refinadas, restando, para a próxima sprint, a integração completa entre os múltiplos componentes da solução.

[Link da Apresentação](https://www.canva.com/design/DAGR3VpNoA8/awAvnATskHF7mnkez3gPhg/view?utm_content=DAGR3VpNoA8&utm_campaign=designshare&utm_medium=link&utm_source=editor)

<iframe loading="lazy"
    style={{ display: 'block', margin: 'auto', width: '100%', height: '66vh' }}
    src="https://www.canva.com/design/DAGR3VpNoA8/28rJrZwGOn3LgoOFcpyXqQ/view?embed">
</iframe>
