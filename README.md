# MySword Tools

Ferramentas para criar conteúdo compatível com o aplicativo **MySword** (estudo bíblico para Android).

## Funcionalidades

### Conversor Word para Journal (.jor.mybible)
- Importa documentos Word (.docx) e converte para o formato Journal do MySword
- **Extração automática de metadados** das propriedades do documento
- Preserva formatação (negrito, itálico, sublinhado, cores)
- Converte tabelas para HTML
- Detecta e converte referências bíblicas em links clicáveis
- Divide documento em entradas baseado nos títulos (Heading 1)

## Instalação

### 1. Criar ambiente virtual

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

## Uso Rápido

### Conversão básica (detecta metadados automaticamente)

```bash
python -m src.word_to_journal documento.docx saida.jor.mybible
```

### Com parâmetros personalizados

```bash
python -m src.word_to_journal documento.docx saida.jor.mybible \
    --title "Meu Estudo Bíblico" \
    --author "Seu Nome" \
    --abbreviation "ESTUDO"
```

### Parâmetros disponíveis

| Parâmetro | Descrição |
|-----------|-----------|
| `--title`, `-t` | Título do Journal (extrai do documento se não fornecido) |
| `--description`, `-d` | Descrição do Journal |
| `--author` | Autor do Journal |
| `--abbreviation`, `-a` | Abreviação curta (sem espaços) |
| `--no-split` | Não dividir por títulos |
| `--heading-level`, `-h` | Nível do heading para divisão (1-6) |

## Estrutura do Documento Word

### Metadados Automáticos

O conversor extrai metadados de **duas fontes** (em ordem de prioridade):

#### 1. Propriedades do Documento (recomendado)

No Word, vá em **Arquivo → Informações → Propriedades**:

| Propriedade Word | Campo no MySword |
|------------------|------------------|
| **Título** | Título do Journal |
| **Autor** | Autor |
| **Assunto** | Descrição |
| **Palavras-chave** | Tags |

#### 2. Linhas no Início do Documento

Se as propriedades estiverem vazias, o conversor procura estes padrões no início do documento:

```
Autor: Seu Nome
Descrição: Uma breve descrição do estudo
Tags: estudo, bíblia, oração
Abreviação: MEUEST
```

### Estrutura do Conteúdo

```
┌─────────────────────────────────────────────────────────────┐
│ [Título] Título Principal do Estudo                          │ ← Título do Journal
│                                                              │
│ Autor: Seu Nome                  (opcional se usar props)    │
│ Descrição: Breve descrição       (opcional se usar props)    │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│ [Título 1] Primeira Entrada                                  │ ← Entrada 1
│                                                              │
│ Conteúdo da primeira entrada...                              │
│ Referências: João 3:16, Mateus 5:3-12                        │ ← Links automáticos
│                                                              │
├──────────────────────────────────────────────────────────────┤
│ [Título 1] Segunda Entrada                                   │ ← Entrada 2
│                                                              │
│   [Título 2] Subtítulo                                       │ ← Subdivisão
│   Conteúdo...                                                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Referências Bíblicas

Referências no texto são automaticamente convertidas em links clicáveis:

| Formato | Exemplo | Resultado |
|---------|---------|-----------|
| Livro Cap:Vers | João 3:16 | `<a href='bJoão 3:16'>João 3:16</a>` |
| Intervalo | Mt 5:3-12 | Link para Mateus 5:3-12 |
| Abreviado | Gn 1:1

 | Reconhece abreviações |
| Livros numerados | 1 Co 13:4 | Primeira Coríntios |
| Nomes em português | Gênesis 1:1 | Suporte completo |

### Abreviações Suportadas

- **Antigo Testamento**: Gn, Ex, Lv, Nm, Dt, Js, Jz, Rt, 1Sm, 2Sm, 1Rs, 2Rs, 1Cr, 2Cr, Ed, Ne, Et, Jó, Sl, Pv, Ec, Ct, Is, Jr, Lm, Ez, Dn, Os, Jl, Am, Ob, Jn, Mq, Na, Hc, Sf, Ag, Zc, Ml

- **Novo Testamento**: Mt, Mc, Lc, Jo, At, Rm, 1Co, 2Co, Gl, Ef, Fp, Cl, 1Ts, 2Ts, 1Tm, 2Tm, Tt, Fm, Hb, Tg, 1Pe, 2Pe, 1Jo, 2Jo, 3Jo, Jd, Ap

## Uso Programático

```python
from src.mysword_journal import MySwordJournal, create_bible_link

# Criar Journal programaticamente
journal = MySwordJournal(
    abbreviation="MEU_ESTUDO",
    title="Meu Estudo Bíblico",
    author="Seu Nome",
    description="Um estudo sobre oração"
)

# Adicionar entradas
journal.add_entry(
    title="Introdução",
    content="<p>Bem-vindo ao estudo...</p>"
)

journal.add_entry(
    title="O Poder da Oração",
    content=f"<p>Veja {create_bible_link('Filipenses 4:6-7')}</p>"
)

# Salvar
journal.save("meu_estudo.jor.mybible")
```

## Importando no MySword

1. Copie o arquivo `.jor.mybible` para seu dispositivo Android
2. Coloque na pasta: `/storage/emulated/0/mysword/journals/`
3. Abra o MySword e acesse a seção de Journals
4. O Journal aparecerá com a abreviação configurada

## Estrutura do Projeto

```
mysword-tools/
├── src/
│   ├── mysword_journal.py        # Classes para manipular Journal
│   ├── word_to_journal.py        # Conversor Word → Journal
│   └── cli.py                    # Interface de linha de comando
├── examples/
│   ├── sample_usage.py           # Exemplo programático
│   ├── create_template_docx.py   # Criar documento template
│   ├── template_estudo_biblico.docx  # Template Word
│   └── estudo_oracao.docx        # Exemplo de estudo
├── output/                       # Arquivos gerados
├── requirements.txt
└── README.md
```

## Arquivos de Exemplo

| Arquivo | Descrição |
|---------|-----------|
| `examples/template_estudo_biblico.docx` | Template completo com instruções |
| `examples/estudo_oracao.docx` | Exemplo de estudo sobre oração |
| `output/template_estudo.jor.mybible` | Template convertido |

## Licença

MIT License
