# Relatorio de Governanca e Riscos — Genera IA

**Projeto**: Genera IA — Sprint 2 — Enterprise Challenge DASA | FIAP 2026  
**Versao**: 1.0  
**Data**: Maio 2026

---

## 1. Escopo do Agente

### 1.1 O que o agente FAZ

- Interpreta dados contidos em relatorios geneticos da Dasa Genomica
- Explica termos tecnicos em linguagem acessivel (6ª serie)
- Recupera trechos especificos do relatorio via busca semantica
- Contextualiza riscos geneticos com comparacoes populacionais
- Sugere que o paciente converse com um profissional de saude
- Informa a data da proxima reavaliacao sugerida
- Permite que o paciente confirme o agendamento da reavaliacao
- Exibe as fontes (trechos do relatorio) que basearam cada resposta

### 1.2 O que o agente NAO FAZ

- **NAO** emite diagnosticos medicos
- **NAO** prescreve medicamentos ou tratamentos
- **NAO** afirma que o paciente tem ou tera uma doenca
- **NAO** substitui consulta medica
- **NAO** inventa dados, genes, variantes ou percentuais
- **NAO** responde perguntas fora do escopo do relatorio
- **NAO** revela informacoes pessoais do paciente alem do necessario
- **NAO** interpreta exames que nao sejam os do relatorio carregado

---

## 2. Separacao de Papeis — Paciente vs Medico

| Informacao | Paciente | Medico |
|---|---|---|
| Dados geneticos interpretados pela IA | ✅ | ✅ |
| Trechos do relatorio (fontes) | ✅ | ✅ |
| Agendamento de reavaliacao (com botao) | ✅ | ✅ (informativo) |
| Metadados administrativos (protocolo, CRM, CRBM) | ❌ | ✅ |
| Exames complementares sugeridos com codigo TUSS | ❌ | ✅ |
| Historico de anotacoes clinicas | ❌ | ✅ |

**Justificativa**: Metadados administrativos e sugestoes de exames complementares sao informacoes de trabalho do profissional de saude. Exibi-las ao paciente pode causar confusao, automedicacao ou ansiedade desnecessaria.

---

## 3. Guardrails Tecnicos

### 3.1 System Prompt (controle de comportamento)

Localizado em `src/llm/prompts.py`. O System Prompt define:

- Persona: assistente virtual da Dasa Genomica
- Linguagem: portugues simples (6ª serie), explicacao de todo jargao
- Tom: acolhedor, empatico, nunca alarmista
- Limites: nao e medico, nao da diagnosticos, nao prescreve
- Fundamentacao: exclusivamente no contexto do relatorio
- Disclaimer: obrigatorio em toda resposta

### 3.2 Validacao pos-geracao (validate_response)

Localizado em `src/llm/prompts.py:validate_response()`. Apos cada geracao, verifica:

1. **Presenca do disclaimer** — palavras-chave "nao um diagnostico" e "consulte sempre um profissional"
2. **Ausencia de termos alarmistas** — "seu diagnostico", "voce esta com", "voce sofre de", "voce desenvolvera", "perigoso", "preocupante", "alarmante", "urgente", "emergencia"
3. **Comprimento minimo** — resposta deve ter pelo menos 50 caracteres

Resultados sao exibidos na interface como "Alertas de qualidade" quando ha violacoes.

### 3.3 RAG Template (anti-alucinacao)

Localizado em `src/llm/prompts.py:RAG_TEMPLATE`. O template de prompt instrui o LLM a:

- Responder com base **EXCLUSIVAMENTE** no contexto fornecido
- Se o contexto nao contiver informacao suficiente, dizer: "Esta informacao especifica nao consta no seu relatorio Genera"
- **NAO inventar** informacoes que nao estejam no contexto

---

## 4. Privacidade e Protecao de Dados

### 4.1 Armazenamento

- Relatorios sao armazenados **localmente** (ChromaDB em disco + JSONs)
- Nenhum dado e enviado para servicos externos alem do estritamente necessario para:
  - Gerar embeddings (NVIDIA API)
  - Gerar respostas (NVIDIA NIM / OpenRouter API)
- Os textos enviados para APIs sao trechos anonimizados do relatorio

### 4.2 Dados enviados para APIs externas

| Servico | Dados enviados | Proposito |
|---|---|---|
| NVIDIA NeMo Embeddings | Trechos de texto do relatorio (sem identificacao do paciente) | Gerar vetores de embedding |
| NVIDIA NIM / OpenRouter | Contexto do relatorio + pergunta do usuario | Gerar resposta fundamentada |

### 4.3 Recomendacoes para producao

- Criptografia em repouso (AES-256) para ChromaDB e JSONs
- Anonimizacao completa pre-API (remover nome, ID, metadados)
- Politica de retencao: dados excluidos apos X dias da ultima consulta
- Log de acesso auditoria para conformidade LGPD
- Termo de consentimento explicito do paciente

---

## 5. Disclaimers

### 5.1 Disclaimer obrigatorio (toda resposta)

> Esta e uma interpretacao do seu relatorio Genera, nao um diagnostico medico.  
> Consulte sempre um profissional de saude para orientacoes personalizadas.  
> Para duvidas medicas, o Nucleo de Assessoria Medica (NAM) da Dasa esta  
> disponivel para auxiliar seu medico na interpretacao dos resultados.

### 5.2 Locais de exibicao

- Ao final de **toda resposta** do chat (paciente e medico)
- Na tela de **login**
- Na aba **Ajuda**
- No **README** do repositorio
- No **chainlit.md** (tela de boas-vindas)

---

## 6. Riscos Identificados e Mitigacoes

| Risco | Probabilidade | Impacto | Mitigacao |
|---|---|---|---|
| **Alucinacao do LLM** | Media | Alto | RAG com grounding estrito + prompt "nao sei" + validacao pos-geracao |
| **Resposta alarmista** | Baixa | Alto | System Prompt proibindo + lista de termos proibidos + validacao |
| **Diagnostico inadvertido** | Baixa | Alto | System Prompt + disclaimer + validacao |
| **Vazamento de dados** | Baixa | Alto | Armazenamento local + anonimizacao pre-API |
| **Indisponibilidade da API NVIDIA** | Media | Medio | Arquitetura com fallback automatico NVIDIA → OpenRouter |
| **Resposta lenta** | Media | Baixo | Top-K configuravel + streaming (pendente) + timeout da API |
| **Falso positivo em guardrail** | Baixa | Baixo | Ajuste manual da lista FORBIDDEN_TERMS |

---

## 7. Conformidade com o Sprint 2

| Requisito | Status |
|---|---|
| Delimitacao dos limites do agente | ✅ Implementado via System Prompt + documentacao |
| Disclaimers obrigatorios | ✅ Em toda resposta + multiplos pontos da interface |
| Dados simulados | ✅ 3 perfis geneticos completos |
| Guardrails anti-diagnostico | ✅ validate_response() + FORBIDDEN_TERMS |
| Separacao paciente/medico | ✅ Metadados e exames complementares visiveis apenas ao medico |
| Rastreabilidade das respostas | ✅ Fontes exibidas com similaridade + trecho do relatorio |

---

## 8. Contato

**Nucleo de Assessoria Medica (NAM) — Dasa**  
Email: namgenomica@dasa.com.br  
WhatsApp: (11) 4020-2446  
Horario: Seg-Sex 8h as 20h, Sab 8h as 12h

---

**FIAP — Enterprise Challenge — Sprint 2 — Maio 2026**
