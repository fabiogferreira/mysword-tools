# Backlog do Projeto - MySword Tools

Este documento mapeia o status atual do projeto e lista os itens prioritários pendentes para que o MySword Tools atinja uma **versão usável em produção (pronta para a comunidade)**.

---

## 🔍 Status Atual e Diagnóstico Técnico

### 1. Gargalo Crítico de Performance (Lentidão no Processamento)
* **Problema:** A conversão de documentos Word com listas (por exemplo, `UICP-2026.docx`) é excessivamente lenta, levando vários minutos para processar poucas centenas de parágrafos.
* **Causa Raiz:** O método [_get_list_tag](file:///c:/projects/mysword-tools/src/word_to_journal.py#L641-L690) realiza o carregamento, parsing com `lxml` e busca XPath do arquivo XML `numbering.xml` do pacote docx **a cada parágrafo de lista** encontrado no documento.
* **Solução:** Fazer o parse do `numbering_part` uma única vez na inicialização da classe [WordToJournalConverter](file:///c:/projects/mysword-tools/src/word_to_journal.py#L112) e armazenar os formatos em cache na memória.

### 2. Problema da "Sessão Única" (Documento sem Divisão de Lições)
* **Problema:** A maioria dos documentos é convertida como uma única entrada gigante no Journal, em vez de ser dividida em múltiplos tópicos (aulas/lições).
* **Causa Raiz:** O documento real frequentemente usa estilos como `Heading 2` ou `Heading 3` para as divisões principais, enquanto o conversor tem a opção de divisão automática [_detect_best_heading_level](file:///c:/projects/mysword-tools/src/word_to_journal.py#L453) desativada por padrão. O valor padrão de `heading_level` é forçado como **`1`** tanto no endpoint do FastAPI ([app.py](file:///c:/projects/mysword-tools/src/web/app.py#L97)) quanto no estado React do frontend ([page.tsx](file:///c:/projects/mysword-tools/src/web/frontend/src/app/page.tsx#L21)).
* **Solução:** Alterar o valor padrão do parâmetro `heading_level` no backend e frontend para **`0`** (detecção automática inteligente) quando não especificado manualmente pelo usuário.

### 3. Modelo de Cobrança / Stripe Checkout Sandbox
* **Problema:** O fluxo do Stripe Sandbox está implementado visualmente na tabela de preços, mas o botão de conversão definitiva ([/api/convert](file:///c:/projects/mysword-tools/src/web/app.py#L89)) funciona de forma gratuita e irrestrita no frontend.
* **Solução:** Para uma versão de produção SaaS, é necessário acoplar a conversão definitiva a um sistema de autenticação e controle de créditos no banco de dados. Caso o objetivo seja disponibilizar uma ferramenta 100% gratuita para a comunidade, os planos e o fluxo do Stripe devem ser removidos ou ocultados da interface.

---

## 📋 Itens de Ação (Backlog)

### Alta Prioridade (Impeditivos de Usabilidade)

- [ ] **Otimização de Performance no Core:**
  - Refatorar o método `_get_list_tag` em [word_to_journal.py](file:///c:/projects/mysword-tools/src/word_to_journal.py) para carregar o `numbering.xml` uma única vez e cachear o mapeamento de níveis e tipos de lista.
  - *Resultado Esperado:* Tempo de processamento reduzido de minutos para menos de 5 segundos em arquivos médios/grandes.

- [ ] **Ajuste de Divisão Automática de Seções (Padrão Auto):**
  - Alterar o default de `heading_level` de `1` para `0` no FastAPI ([app.py](file:///c:/projects/mysword-tools/src/web/app.py)) e no state do React ([page.tsx](file:///c:/projects/mysword-tools/src/web/frontend/src/app/page.tsx)).
  - *Resultado Esperado:* Documentos que usam Título 2 ou Título 3 serão divididos corretamente por padrão, sem exigir configuração manual.

### Média Prioridade (Polimento & Configuração)

- [ ] **Decisão do Modelo do Web App (SaaS vs. Ferramenta Gratuita):**
  - Definir se a aplicação será monetizada (necessitando de integração banco de dados + autenticação para os tokens do Stripe) ou se será uma ferramenta comunitária de uso livre (necessitando a remoção visual da tabela de preços e do Stripe).

- [ ] **Testes de Validação E2E com Documentos de Estudo:**
  - Executar a validação fim a fim do conversor utilizando o arquivo `UICP-2026.docx` e conferir a estrutura final gerada do banco SQLite `.jor.mybible` em dispositivos Android.
