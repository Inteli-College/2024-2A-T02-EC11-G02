Com base nas informações do documento e nas funcionalidades descritas, segue a documentação dos requisitos funcionais e não funcionais implementados:

---

## Requisitos Funcionais Implementados

Os requisitos funcionais referem-se às funcionalidades que o sistema deve fornecer para atender às necessidades dos usuários e às especificações do projeto. Abaixo estão os principais requisitos funcionais que foram implementados na solução:

### 1. Processamento de Imagens para Contagem de Árvores
   - **Descrição**: A solução recebe imagens e realiza a contagem de árvores utilizando um modelo de visão computacional.
   - **Implementação**: O upload de imagens é feito via API, e o processamento é realizado utilizando o módulo `FilteringSegmentation`, que segmenta e conta as árvores nas imagens enviadas.
   - **Resultado**: O sistema armazena os resultados da análise, incluindo a quantidade de árvores e a estimativa de cobertura de vegetação, em uma base de dados MongoDB.

### 2. Upload e Processamento de Arquivos ZIP
   - **Descrição**: Permite ao usuário enviar um arquivo ZIP contendo múltiplas imagens para processamento.
   - **Implementação**: As imagens são extraídas do arquivo ZIP, processadas individualmente e os resultados são armazenados e retornados ao usuário.
   - **Resultado**: URLs das imagens originais e processadas são geradas e retornadas como resposta, facilitando a visualização dos resultados.

### 3. Geração de Relatórios de Resultados
   - **Descrição**: O sistema permite ao usuário acessar os resultados dos processos de contagem de árvores.
   - **Implementação**: As informações geradas são armazenadas no banco de dados e podem ser consultadas para a visualização de métricas como a quantidade de árvores detectadas e a área estimada de vegetação.

### 4. Interface de Visualização de Dados
   - **Descrição**: Oferece uma interface gráfica para visualização dos dados de contagem de árvores, incluindo gráficos e mapas.
   - **Implementação**: O design da interface segue princípios de usabilidade, como visibilidade do status do sistema e consistência visual, conforme descrito no documento.

---

## Requisitos Não Funcionais Implementados

Os requisitos não funcionais descrevem as características de qualidade e desempenho do sistema. A seguir, estão os principais requisitos não funcionais que foram abordados na solução:

### 1. Usabilidade e Interface de Usuário
   - **Descrição**: A interface foi projetada para ser intuitiva e fácil de usar, atendendo tanto a usuários novos quanto a experientes.
   - **Implementação**: A interface gráfica exibe o status do sistema e resultados em tempo real, usando gráficos e mapas para melhorar a compreensão. O design é minimalista, com cores que facilitam a leitura e navegação.
   - **Resultado**: Isso garante que os usuários possam interagir de maneira eficiente, reconhecendo e corrigindo erros de forma rápida.

### 2. Desempenho e Tempo de Resposta
   - **Descrição**: O sistema deve ser capaz de processar múltiplas imagens de forma eficiente, garantindo tempos de resposta aceitáveis para o upload e processamento de arquivos ZIP.
   - **Implementação**: A solução foi desenvolvida para processar imagens de forma assíncrona, permitindo que a interface permaneça responsiva durante o processamento dos dados.
   - **Resultado**: Os tempos de processamento foram otimizados para garantir que as imagens sejam processadas e os resultados retornados em um prazo adequado.

### 3. Armazenamento e Persistência de Dados
   - **Descrição**: O sistema deve armazenar os resultados das análises de forma segura e persistente.
   - **Implementação**: Utilização de MongoDB para persistência dos dados, com estrutura organizada para armazenar informações de cada imagem processada, garantindo a integridade dos dados.
   - **Resultado**: A base de dados permite fácil acesso aos resultados, possibilitando a criação de relatórios e consultas posteriores.

### 4. Confiabilidade do Algoritmo
   - **Descrição**: A solução deve fornecer resultados precisos e confiáveis na contagem de árvores.
   - **Implementação**: Testes de confiabilidade foram realizados, comparando as contagens do algoritmo com contagens manuais em uma pequena base de imagens.
   - **Métricas Avaliadas**: Foram analisadas métricas como precisão e acurácia para verificar a assertividade do modelo.
   - **Resultado**: O sistema demonstrou um bom nível de precisão na contagem, mas também foram identificadas limitações devido ao método manual utilizado para comparação.