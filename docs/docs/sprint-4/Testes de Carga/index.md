---
title: Testes de Carga
sidebar_position: 4
---

Testes de carga são comumente aplicados a sistemas que exigem significativo poder de processamento, uma vez que tendem a receber múltiplas requisições em curtos intervalos de tempo. No caso do sistema desenvolvido, entretanto, optou-se pela não realização de testes de carga, uma vez que a solução será utilizada periodicamente e não deverá receber um volume significativo de requisições.

Considerando o atual fluxo da solução — em que imagens tiradas pela câmera são compactadas, enviadas para o back-end, e submetidas ao modelo de visão computacional conforme demanda do cliente —, a equipe avaliou que nenhuma das rotas do back-end será sobrecarregada quando as funcionalidades do projeto estiverem em uso. Esta análise foi realizada com base no comportamento esperado dos usuários e no perfil da aplicação, que não prevê picos súbitos ou grandes volumes de acessos simultâneos.

Portanto, é possível afirmar que, dado o perfil de uso da solução e a ausência de requisitos críticos relacionados à escalabilidade em grandes volumes, os testes de carga podem ser considerados desnecessários nesta fase. Contudo, cabe ressaltar que, caso o escopo da solução ou o volume de usuários venha a mudar, a execução de testes de carga poderá ser reavaliada para garantir a performance adequada da solução em cenários futuros.