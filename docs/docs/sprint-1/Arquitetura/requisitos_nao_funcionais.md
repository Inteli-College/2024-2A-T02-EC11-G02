# Requisitos Não Funcionais

Os requisitos não funcionais descrevem as qualidades e restrições do sistema, como desempenho, escalabilidade e segurança. Eles são cruciais para garantir que o sistema não apenas funcione corretamente, mas também ofereça uma boa experiência ao usuário, seja seguro e fácil de manter.

## Requisitos

1. **Desempenho**:
   - O processamento das imagens deve ser rápido o suficiente para fornecer resultados em no máximo 10 minutos.
   - A IA deve ter uma precisão de pelo menos 90% ao estimar o número de árvores, preferindo-se falsos positivos para os erros. 
   - A dashboard deve ser responsiva e suportar um grande volume de dados, referentes a uma quantidade estimada de centenas de milhares de árvores.

2. **Escalabilidade**:
   - O sistema deve ser escalável para suportar a análise de grandes áreas de floresta sem comprometer a performance.
   - O sistema também deve ser compátivel com os serviços e interfaces da Abundance.
   - Os dados devem ser processados pelo drone e enviados para um backend.

3. **Segurança**:
   - Os dados armazenados devem ser protegidos contra acessos não autorizados.
   - A solução deve estar em conformidade com regulamentos de proteção de dados e privacidade relevantes, especialmente considerando que envolve dados sensíveis de florestas.

4. **Confiabilidade**:
   - O sistema deve ter alta disponibilidade e ser resistente a falhas.
   - Deve haver mecanismos de backup e recuperação de dados.

5. **Usabilidade**:
   - A interface da dashboard deve ser intuitiva, com uma curva de aprendizado mínima.
   - A interação com o drone para captura de imagens deve ser simples e eficiente.

6. **Manutenibilidade**:
   - O código do sistema deve ser bem documentado para facilitar a manutenção e atualização.
   - Deve haver procedimentos claros para atualização do sistema de IA com novos dados.

7. **Compatibilidade**:
   - A dashboard deve ser acessível a partir de diferentes dispositivos e navegadores.
   - A solução deve ser compatível com os dispositivos que capturam as imagens (drones/satélites), garantindo que o modelo possa ser operacionalizado em ambientes reais.
