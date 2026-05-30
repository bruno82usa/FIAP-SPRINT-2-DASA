import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import json

from src.config import TOP_K_CHUNKS, LLM_TEMPERATURE
from src.data.generator import generate_reports, load_report, list_reports, list_patients, get_patient_by_id
from src.vector_store.chroma_store import ChromaStore
from src.llm.client import LLMClient
from src.rag.pipeline import RAGPipeline
from src.llm.prompts import DISCLAIMER

st.set_page_config(page_title="Genera IA — Assistente Genetico", page_icon="🧬", layout="wide")

# ── Session state ───────────────────────────────────────────────
if "pipeline" not in st.session_state:
    st.session_state.pipeline = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "role" not in st.session_state:
    st.session_state.role = None
if "report_id" not in st.session_state:
    st.session_state.report_id = None
if "tab" not in st.session_state:
    st.session_state.tab = "login"
if "schedule_confirmed" not in st.session_state:
    st.session_state.schedule_confirmed = False
if "doctor_patient_id" not in st.session_state:
    st.session_state.doctor_patient_id = None
if "doctor_reports" not in st.session_state:
    st.session_state.doctor_reports = []
if "doctor_messages" not in st.session_state:
    st.session_state.doctor_messages = []


def init_pipeline():
    store = ChromaStore()
    llm = LLMClient()
    st.session_state.pipeline = RAGPipeline(store, llm)


def ensure_pipeline():
    if st.session_state.pipeline is None:
        with st.spinner("Inicializando motor de IA..."):
            init_pipeline()
        generate_reports()
        for rid in list_reports():
            report = load_report(rid)
            if report:
                st.session_state.pipeline.ingest_report(report)


def risk_emoji(risk_label):
    if "aumentado" in risk_label: return "🔴"
    if "levemente" in risk_label: return "🟡"
    return "🔵"


# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/dna-helix.png", width=64)
    st.title("🧬 Genera IA")
    st.caption("Dasa Genomica")
    st.caption("Medicina do Futuro, Todos os Dias")
    st.divider()

    if st.session_state.role:
        role_label = "Paciente" if st.session_state.role == "patient" else "Medico(a)"
        st.write(f"Perfil: **{role_label}**")
        if st.button("Trocar de perfil"):
            st.session_state.role = None
            st.session_state.tab = "login"
            st.session_state.report_id = None
            st.session_state.messages = []
            st.rerun()

    st.divider()
    st.caption("FIAP — Sprint 2 — Dasa")


# ═════════════════════════════════════════════════════════════════
# LOGIN
# ═════════════════════════════════════════════════════════════════
if st.session_state.role is None:
    st.title("🧬 Genera IA")
    st.caption("Dasa Genomica — Medicina preventiva, preditiva e personalizada")
    st.markdown("### Selecione seu perfil:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧬 Sou Paciente\n\nConsultar meus relatorios geneticos", use_container_width=True):
            ensure_pipeline()
            st.session_state.role = "patient"
            st.session_state.tab = "reports"
            st.rerun()
    with col2:
        if st.button("👩‍⚕️ Sou Medico(a)\n\nPortal profissional", use_container_width=True):
            ensure_pipeline()
            st.session_state.role = "doctor"
            st.session_state.tab = "patients"
            st.rerun()

    st.divider()
    st.markdown("""### 👋 Bem-vindo(a) ao Genera IA
O assistente virtual da **Dasa Genomica** ajuda voce a entender seu relatorio genetico.

A Dasa Genomica reune GeneOne + Chromosome + Genia + Insitus para oferecer
um cuidado **preventivo, preditivo, personalizado e por toda a vida**.
""")
    st.warning(DISCLAIMER)
    st.stop()


# ═════════════════════════════════════════════════════════════════
# PATIENT
# ═════════════════════════════════════════════════════════════════
if st.session_state.role == "patient":
    st.title("🧬 Genera IA")
    st.caption("Dasa Genomica — Medicina preventiva, preditiva, personalizada e por toda a vida.")

    tab_names = ["📋 Relatorios", "💬 Chat", "📅 Agendamento", "ℹ️ Ajuda"]
    tab_keys  = ["reports", "chat", "agendamento", "ajuda"]
    tab_index = tab_keys.index(st.session_state.tab) if st.session_state.tab in tab_keys else 0

    selected = st.radio("nav", tab_names, index=tab_index, horizontal=True, label_visibility="collapsed")
    selected_key = tab_keys[tab_names.index(selected)]
    if selected_key != st.session_state.tab:
        st.session_state.tab = selected_key
        st.rerun()

    # ── 📋 Relatorios ──
    if selected_key == "reports":
        report_ids = list_reports()
        if not report_ids:
            st.warning("Nenhum relatorio encontrado. Gerando dados...")
            if st.button("Gerar relatorios demo"):
                ensure_pipeline()
                st.rerun()
        else:
            st.caption(f"{len(report_ids)} relatorio(s) encontrado(s). Selecione um para conversar ou agendar.")

            for rid in sorted(report_ids):
                report = load_report(rid)
                if not report:
                    continue
                date = report["exam_metadata"]["exam_date"]
                exam_type = report["exam_metadata"]["exam_type"]
                patient_name = report["patient_name"]
                next_date = report.get("suggested_next_exam", {}).get("date", "")

                max_risk, risk_label = 0, "risco tipico"
                for item in report["sections"].get("predisposicao_doencas", {}).get("data", []):
                    s = item.get("risk_score", 0)
                    if s > max_risk:
                        max_risk, risk_label = s, item.get("risk_level", "risco tipico")

                with st.container(border=True):
                    st.markdown(f"### {risk_emoji(risk_label)} {date}")
                    st.markdown(f"**{exam_type}**")
                    st.caption(f"Paciente: {patient_name} | Predisposicao: {risk_label}")
                    if next_date:
                        st.caption(f"Proxima reavaliacao sugerida: {next_date}")

                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("💬 Conversar", key=f"chat_{rid}", use_container_width=True):
                            st.session_state.report_id = rid
                            st.session_state.messages = []
                            st.session_state.tab = "chat"
                            st.rerun()
                    with c2:
                        if st.button("📅 Agendar", key=f"sched_{rid}", use_container_width=True):
                            st.session_state.report_id = rid
                            st.session_state.tab = "agendamento"
                            st.rerun()

    # ── 💬 Chat ──
    elif selected_key == "chat":
        report_id = st.session_state.report_id
        if not report_id:
            st.info("Selecione um relatorio na aba 📋 Relatorios para conversar.")
            if st.button("Ir para Relatorios"):
                st.session_state.tab = "reports"
                st.rerun()
        else:
            report = load_report(report_id)
            if report:
                st.caption(f"Relatorio de **{report['exam_metadata']['exam_date']}** — Paciente: **{report['patient_name']}**")

            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
                    if msg.get("sources"):
                        with st.expander("Fontes consultadas no relatorio"):
                            for src in msg["sources"]:
                                st.caption(f"{src['section']} — {src['similarity']}%")
                                st.text(src["content"])

            prompt = st.chat_input("Digite sua pergunta sobre o relatorio...")
            if prompt:
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    with st.spinner("Analisando relatorio..."):
                        result = st.session_state.pipeline.query(
                            question=prompt, report_id=report_id, k=TOP_K_CHUNKS
                        )
                    st.markdown(result["answer"])

                    if result.get("guardrail_issues"):
                        for i in result["guardrail_issues"]:
                            st.warning(i)

                    sources = result.get("sources", [])
                    if sources:
                        with st.expander("Fontes consultadas no relatorio"):
                            for src in sources:
                                st.caption(f"{src['section']} — relevancia: {src['similarity']}%")
                                st.text(src["content"])

                    if report and report.get("suggested_next_exam", {}).get("date"):
                        nex = report["suggested_next_exam"]
                        st.info(f"Proxima reavaliacao sugerida: **{nex['date']}** — {nex['reason']}")
                        if st.button("Agendar esta reavaliacao", key="sched_chat"):
                            st.session_state.tab = "agendamento"
                            st.rerun()

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result.get("sources", []),
                })
                st.rerun()

        st.warning(DISCLAIMER)

    # ── 📅 Agendamento ──
    elif selected_key == "agendamento":
        report_id = st.session_state.report_id
        if not report_id:
            st.info("Selecione um relatorio na aba 📋 Relatorios para agendar.")
            if st.button("Ir para Relatorios"):
                st.session_state.tab = "reports"
                st.rerun()
        else:
            report = load_report(report_id)
            if report:
                nex = report.get("suggested_next_exam", {})
                date = nex.get("date", "Nao definida")
                reason = nex.get("reason", "")
                name = report["patient_name"]

                st.markdown(f"## 📅 Agendamento de Reavaliacao")
                st.markdown(f"**Paciente:** {name}")
                st.markdown(f"**Data sugerida:** {date}")
                st.markdown(f"**Motivo:** {reason}")

                if not st.session_state.schedule_confirmed:
                    c1, c2, c3 = st.columns([1, 1, 2])
                    with c1:
                        if st.button("✅ Confirmar", type="primary", use_container_width=True):
                            st.session_state.schedule_confirmed = True
                            st.rerun()
                    with c2:
                        if st.button("❌ Cancelar", use_container_width=True):
                            st.info("Tudo bem! Voce pode agendar quando quiser.")
                else:
                    st.success(f"#### ✅ Agendamento Confirmado!\n\nPaciente: **{name}**\n\nData: **{date}**\n\nLocal: Unidade Dasa de sua preferencia\n\nVoce recebera um lembrete proximo a data. Consulte seus resultados na plataforma **Nav Dasa**.")
                    if st.button("Voltar"):
                        st.session_state.schedule_confirmed = False
                        st.rerun()
            else:
                st.warning("Relatorio nao encontrado.")

    # ── ℹ️ Ajuda ──
    elif selected_key == "ajuda":
        st.markdown("""
        ## ℹ️ Ajuda — Genera IA

        ### O que e a Genera IA?
        Assistente virtual da **Dasa Genomica** que ajuda voce a entender seu relatorio genetico com linguagem simples e acessivel.

        ### Como usar
        **1. 📋 Relatorios** — veja seus exames e escolha um para consultar
        **2. 💬 Chat** — faca perguntas sobre seus resultados
        **3. 📅 Agendamento** — marque sua proxima reavaliacao genetica

        ### O que perguntar
        - Qual e minha ancestralidade?
        - Tenho predisposicao genetica para alguma doenca?
        - Como meu organismo processa medicamentos?
        - Sou portador(a) de alguma condicao genetica?
        - Tracos de bem-estar (lactose, cafeina, exercicios)

        ### Contato
        **NAM — Nucleo de Assessoria Medica da Dasa**
        Email: namgenomica@dasa.com.br | WhatsApp: (11) 4020-2446
        Seg-Sex 8h as 20h, Sab 8h as 12h
        """)
        st.warning(DISCLAIMER)


# ═════════════════════════════════════════════════════════════════
# DOCTOR
# ═════════════════════════════════════════════════════════════════
if st.session_state.role == "doctor":
    st.title("🧬 Genera IA — Portal Medico")
    st.caption("Dasa Genomica — Nucleo de Assessoria Medica")

    tab_names = ["👥 Pacientes", "🧬 Prontuario", "🔬 Exames Comp.", "💬 Chat IA"]
    tab_keys  = ["patients", "prontuario", "exames", "chat"]
    tab_index = tab_keys.index(st.session_state.tab) if st.session_state.tab in tab_keys else 0

    selected = st.radio("nav", tab_names, index=tab_index, horizontal=True, label_visibility="collapsed")
    selected_key = tab_keys[tab_names.index(selected)]
    if selected_key != st.session_state.tab:
        st.session_state.tab = selected_key
        st.rerun()

    # ── 👥 Pacientes ──
    if selected_key == "patients":
        patients = list_patients()
        if not patients:
            st.warning("Nenhum paciente cadastrado.")
        else:
            st.caption(f"{len(patients)} paciente(s) encontrado(s).")
            for p in patients:
                with st.container(border=True):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.markdown(f"### {p['patient_name']}")
                        st.caption(f"ID: {p['patient_id']} | Ultimo exame: {p.get('last_exam', '-')}")
                    with c2:
                        if st.button("📋 Abrir", key=f"doc_{p['patient_id']}", use_container_width=True):
                            st.session_state.doctor_patient_id = p["patient_id"]
                            st.session_state.doctor_reports = p.get("reports", [])
                            st.session_state.doctor_messages = []
                            st.session_state.tab = "prontuario"
                            st.rerun()

    # ── 🧬 Prontuario ──
    elif selected_key == "prontuario":
        pid = st.session_state.get("doctor_patient_id")
        if not pid:
            st.info("Selecione um paciente na aba 👥 Pacientes.")
            if st.button("Ir para Pacientes"):
                st.session_state.tab = "patients"
                st.rerun()
        else:
            patient = get_patient_by_id(pid)
            if patient:
                st.subheader(f"Prontuario — {patient['patient_name']}")
                st.caption(f"ID: {patient['patient_id']} | Nascimento: {patient.get('birth_date', '-')}")
                st.divider()

                reports_ids = st.session_state.get("doctor_reports", [])
                for rid in reports_ids:
                    report = load_report(rid)
                    if not report:
                        continue
                    meta = report["exam_metadata"]
                    with st.container(border=True):
                        st.markdown(f"### {meta['exam_type']}")
                        st.caption(f"Data: {meta['exam_date']}")
                        st.caption(f"Protocolo: {meta['protocol_number']}")
                        st.caption(f"Unidade: {meta['collection_location']}")
                        st.caption(f"Laboratorio: {meta['laboratory_name']} — {meta['laboratory_unit']}")
                        st.caption(f"Medico responsavel: {meta['responsible_physician']}")
                        st.caption(f"Responsavel tecnico: {meta['technical_responsible']}")

                        nex = report.get("suggested_next_exam", {})
                        if nex.get("date"):
                            st.info(f"Proxima reavaliacao: **{nex['date']}** — {nex['reason']}")

                st.session_state.report_id = reports_ids[0] if reports_ids else None

    # ── 🔬 Exames Comp. ──
    elif selected_key == "exames":
        pid = st.session_state.get("doctor_patient_id")
        if not pid:
            st.info("Selecione um paciente na aba 👥 Pacientes.")
            if st.button("Ir para Pacientes"):
                st.session_state.tab = "patients"
                st.rerun()
        else:
            patient = get_patient_by_id(pid)
            if patient:
                st.subheader(f"Exames Complementares — {patient['patient_name']}")
                reports_ids = st.session_state.get("doctor_reports", [])
                for rid in reports_ids:
                    report = load_report(rid)
                    if not report:
                        continue
                    comp = report.get("complementary_exams", [])
                    if not comp:
                        st.caption(f"Nenhum exame complementar sugerido para {rid}")
                        continue
                    for e in comp:
                        urgent_label = " ⚠️ ATENCAO" if e.get("urgent") else ""
                        with st.container(border=True):
                            st.markdown(f"**{e['name']}**{urgent_label}")
                            st.caption(f"Codigo TUSS: {e['code']}")
                            st.caption(f"Motivo: {e['reason']}")
                            st.caption(f"Frequencia: {e['frequency']}")

    # ── 💬 Chat IA ──
    elif selected_key == "chat":
        pid = st.session_state.get("doctor_patient_id")
        if not pid:
            st.info("Selecione um paciente na aba 👥 Pacientes para conversar.")
            if st.button("Ir para Pacientes"):
                st.session_state.tab = "patients"
                st.rerun()
        else:
            patient = get_patient_by_id(pid)
            if patient:
                st.caption(f"💬 Chat IA — Paciente: **{patient['patient_name']}**")

            reports_ids = st.session_state.get("doctor_reports", [])
            report_id = st.session_state.get("report_id") or (reports_ids[0] if reports_ids else None)

            for msg in st.session_state.get("doctor_messages", []):
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            prompt = st.chat_input("Digite sua pergunta sobre os dados geneticos do paciente...")
            if prompt:
                st.session_state.doctor_messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    with st.spinner("Consultando IA..."):
                        result = st.session_state.pipeline.query(
                            question=prompt, report_id=report_id, k=TOP_K_CHUNKS
                        )
                    st.markdown(result["answer"])

                    if result.get("guardrail_issues"):
                        for i in result["guardrail_issues"]:
                            st.warning(i)

                    sources = result.get("sources", [])
                    if sources:
                        with st.expander("Fontes consultadas"):
                            for src in sources:
                                st.caption(f"{src['section']} — {src['similarity']}%")
                                st.text(src["content"])

                    if report_id:
                        report = load_report(report_id)
                        if report:
                            meta = report["exam_metadata"]
                            st.caption(f"Fonte: {meta['protocol_number']} | {meta['laboratory_name']} / {meta['laboratory_unit']} | {meta['responsible_physician']}")

                st.session_state.doctor_messages.append({"role": "assistant", "content": result["answer"]})
                st.rerun()
