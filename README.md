# 🧬 Genera IA — Assistente de Interpretacao Genetica

**Sprint 2 — Enterprise Challenge DASA | FIAP 2026**

Sistema de consulta inteligente baseado em **RAG (Retrieval-Augmented Generation)** que permite a pacientes compreenderem seus relatorios geneticos da **Dasa Genomica** — a divisao de medicina genomica da Dasa, lider em medicina diagnostica no Brasil com mais de 23 milhoes de atendimentos por ano.

---

## 📋 Indice

1. [Visao Geral](#visao-geral)
2. [Contexto — Dasa Genomica](#contexto--dasa-genomica)
3. [Arquitetura do Sistema](#arquitetura-do-sistema)
4. [Design System — Cores e Acessibilidade](#design-system--cores-e-acessibilidade)
5. [Stack Tecnologica](#stack-tecnologica)
6. [Estrategia de RAG e Busca Semantica](#estrategia-de-rag-e-busca-semantica)
7. [Engenharia de Prompts](#engenharia-de-prompts)
8. [Como Executar](#como-executar)
9. [Estrutura do Repositorio](#estrutura-do-repositorio)
10. [Fluxos — Paciente e Medico](#fluxos--paciente-e-medico)
11. [Governanca e Riscos](#governanca-e-riscos)
12. [Testes de Qualidade](#testes-de-qualidade)
13. [Video de Demonstracao](#video-de-demonstracao)
14. [Equipe](#equipe)

---

## Visao Geral

O **Genera IA** implementa o motor de inteligencia artificial que permite ao paciente conversar com seu proprio codigo genetico por meio de uma interface de chat acessivel e intuitiva, projetada considerando usuarios idosos.

O projeto se alinha a missao da **Dasa Genomica**: oferecer um modelo de cuidado **preventivo, preditivo, personalizado e por toda a vida**.

### Funcionalidades principais

| Funcionalidade | Descricao |
|---|---|
| 🔍 **Busca Semantica** | Recupera trechos relevantes do relatorio usando embeddings NVIDIA NeMo |
| 💬 **Chat com IA** | Interface conversacional com respostas fundamentadas (RAG) |
| 📖 **Fontes rastreaveis** | Cada resposta exibe os trechos do relatorio que basearam a geracao |
| 🛡️ **Guardrails** | Validações pos-geracao para evitar linguagem alarmista e diagnosticos |
| ⚠️ **Disclaimer obrigatorio** | Aviso legal em toda resposta + mencao ao NAM |
| 📅 **Agendamento** | Paciente agenda proxima reavaliacao diretamente pelo chat |
| 👩‍⚕️ **Portal medico** | Metallados, exames complementares, prontuario por paciente |
| 🔬 **Exames complementares** | Sugestoes de codigo TUSS com justificativa genetica (visao medica) |

---

## Contexto — Dasa Genomica

A **Dasa** e a maior rede de saude integrada do Brasil e lider em medicina diagnostica. Sua atuacao abrange **medicina diagnostica, genetica, patologia, imunizacao e pesquisa clinica**, alem da plataforma digital **Nav Dasa**.

A **Dasa Genomica** nasceu da uniao de **GeneOne + Chromosome + Genia + Insitus**. Suas areas de atuacao:

- **Oncologia** — testes geneticos para tratamento personalizado do cancer
- **Onco-Hematologia** — perfil molecular de neoplasias hematologicas
- **Farmacogenomica** — resposta a medicamentos (HLA-B*1502, CYP2C19, TPMT)
- **Doencas Raras e Neurologia** — diagnostico de condicoes hereditarias
- **Reproducao Humana e Medicina Fetal** — BabyGenes (triagem neonatal)
- **Cardiologia** — variantes de cardiopatias hereditarias
- **Oftalmologia** — doencas oculares geneticas
- **Imunologia e Infectologia** — perfil de resposta imune

O **Nucleo de Assessoria Medica (NAM)** oferece suporte clinico especializado para medicos.

---

## Arquitetura do Sistema

```
┌──────────┐     ┌─────────────┐     ┌──────────────┐
│ Relatorio │────▶│  Chunking   │────▶│   ChromaDB   │
│   JSON    │     │ (por secao) │     │  (persist)   │
└──────────┘     └─────────────┘     └──────┬───────┘
                                            │
┌──────────┐     ┌─────────────┐            │
│ Pergunta │────▶│  Embedding  │────▶ busca │
│ usuario  │     │ (NVIDIA)    │     semantica
└──────────┘     └─────────────┘            │
                                     ┌──────▼───────┐
┌──────────┐     ┌─────────────┐    │ Top-K chunks │
│ Resposta │◀────│  LLM NIM +  │◀───┤  + Prompt    │
│ + fontes │     │  OpenRouter │    │  Template    │
│ + agenda │     └─────────────┘    └──────────────┘
└──────────┘
```

---

## Design System — Cores e Acessibilidade

Cores extraidas do site oficial [dasa.com.br](https://dasa.com.br):

| Token | Hex | Uso |
|---|---|---|
| Primary | `#ABE6FF` | Headers, highlights, cards |
| Text | `#000F40` | Navy blue — corpo de texto |
| Secondary | `#333333` | Subtitulos, metadata |
| Accent | `#FF4F33` | Botoes, CTAs, alertas |
| Gold | `#D4B484` | Risco moderado |
| Success | `#2D8B4E` | Confirmado, risco baixo |

**Fonte**: Roboto (16px base, 18px links) — sans-serif, alta legibilidade.

**Acessibilidade para idosos**:
- Texto minimo 16px
- Botoes com min 48px (touch target)
- Alto contraste (navy `#000F40` sobre branco `#FFFFFF`)
- Icones sempre acompanhados de texto
- 1 acao principal por tela
- Indicadores visuais de risco: 🔵 baixo, 🟡 moderado, 🔴 atencao

---

## Stack Tecnologica

| Camada | Tecnologia | Justificativa |
|---|---|---|
| **Frontend** | Chainlit 2.x | Framework Python para chat apps, melhor UX que Streamlit para conversacao |
| **LLM Primario** | NVIDIA NIM — `meta/llama-3.3-70b-instruct` | 70B parametros, API OpenAI-compatible, creditos gratuitos NVIDIA |
| **LLM Fallback** | OpenRouter — `openai/gpt-4o-mini` | Resiliencia automatica em caso de falha |
| **Embeddings** | NVIDIA NeMo — `nvidia/nv-embed-v1` | 4096 dims, suporte passage vs query |
| **Vector DB** | ChromaDB (persistente) | Local, open-source, busca por cosseno |
| **Linguagem** | Python 3.10+ | Ecossistema IA/NLP |

---

## Fluxos — Paciente e Medico

### Paciente

```
Login → Lista de relatorios (cards com indicador de risco)
          ↓
   Seleciona um relatorio
          ↓
   Chat com IA sobre o relatorio
          ↓
   Resposta + dados do relatorio + botao [Agendar]
          ↓
   Popup "Confirmar agendamento?" → [Sim] / [Nao]
```

### Medico

```
Login → Lista de pacientes (busca, ultimo exame)
          ↓
   Seleciona paciente → Prontuario completo
          ↓
   Ve: metadados, dados geneticos, exames complementares (TUSS)
          ↓
   Chat com IA sobre dados do paciente
```

---

## Como Executar

```bash
cd genera-rag
source venv/bin/activate
pip install -r requirements.txt

# Configure .env com as API keys
cp .env.example .env

# Execute
chainlit run src/app.py
```

Acesse `http://localhost:8000`.

No primeiro acesso, clique em "Gerar e Indexar Relatorios Demo" e selecione seu perfil.

---

## Estrutura do Repositorio

```
genera-rag/
├── src/
│   ├── app.py                     # Chainlit — login + routing paciente/medico
│   ├── config.py                  # Config central (.env)
│   ├── data/
│   │   ├── generator.py           # 3 relatorios com metallados completos
│   │   └── reports/               # JSONs gerados
│   ├── embeddings/
│   │   └── embedder.py            # NVIDIA NeMo embeddings
│   ├── vector_store/
│   │   └── chroma_store.py        # ChromaDB — index, search, persist
│   ├── llm/
│   │   ├── client.py              # NVIDIA NIM + OpenRouter fallback
│   │   └── prompts.py             # System prompt + RAG template + guardrails
│   └── rag/
│       └── pipeline.py            # Orquestracao RAG completa
├── public/
│   └── style.css                  # Tema DASA — cores, fontes, acessibilidade
├── chainlit.md                    # Welcome screen Chainlit
├── chroma_db/                     # Persistencia ChromaDB
├── requirements.txt
├── .env.example
└── README.md
```

---

## Governanca e Riscos

### Limites do Agente

| O agente PODE | O agente NAO PODE |
|---|---|
| Interpretar dados do relatorio | Dar diagnosticos medicos |
| Explicar termos tecnicos | Prescrever medicamentos |
| Contextualizar riscos geneticos | Afirmar que o paciente tem/tera doenca |
| Mostrar fontes do relatorio | Inventar dados nao presentes |
| Sugerir conversar com o medico | Substituir consulta medica |

### Separacao de papeis

| Informacao | Paciente | Medico |
|---|---|---|
| Dados geneticos interpretados | ✅ | ✅ |
| Fontes do relatorio | ✅ | ✅ |
| Agendamento de reavaliacao | ✅ (com botao) | ✅ (informativo) |
| Metallados do exame (protocolo, CRM) | ❌ | ✅ |
| Exames complementares sugeridos (TUSS) | ❌ | ✅ |
| Anotacoes clinicas | ❌ | ✅ |

---

## Testes de Qualidade

| Pergunta | Resultado | Verificacao |
|---|---|---|
| "Qual minha ancestralidade?" | Percentuais + interpretacao | Fontes da secao ancestralidade |
| "Tenho restricao com medicamentos?" | Alertas HLA-B + CYP2C19 | Fontes da secao farmacogenetica |
| "Qual o sentido da vida?" | "Nao consta no relatorio" | Negacao adequada |
| Pergunta fora do escopo | Resposta negando | Guardrails verificam |

---

## Video de Demonstracao

**Link**: [INSERIR LINK APOS GRAVACAO]

---

## Equipe

| Nome | RM | Responsabilidade |
|---|---|---|
| Bruno | XXXXX | Desenvolvimento completo |

---

**FIAP — Enterprise Challenge — Sprint 2 — DASA Genera — Maio/2026**
