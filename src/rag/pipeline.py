import logging
from typing import List, Optional

from src.embeddings.embedder import embed_query
from src.vector_store.chroma_store import ChromaStore
from src.llm.client import LLMClient
from src.llm.prompts import (
    RAG_TEMPLATE,
    SYSTEM_PROMPT,
    DISCLAIMER,
    validate_response,
    format_context,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGPipeline:
    def __init__(self, store: ChromaStore, llm: LLMClient):
        self.store = store
        self.llm = llm

    def ingest_report(self, report: dict) -> int:
        return self.store.index_report(report)

    def query(
        self,
        question: str,
        report_id: Optional[str] = None,
        k: int = 5,
    ) -> dict:
        """
        Full RAG query: retrieve relevant chunks, build prompt, generate answer.
        """
        # Step 1: Retrieve relevant chunks
        chunks = self.store.search(query=question, k=k, report_id=report_id)

        if not chunks:
            return {
                "answer": (
                    "Não encontrei informacoes relevantes no relatorio para responder "
                    "a sua pergunta. Sugiro verificar se o relatorio foi carregado "
                    "corretamente ou reformular a questao.\n\n" + DISCLAIMER
                ),
                "sources": [],
                "model_used": "none",
                "guardrail_issues": [],
            }

        # Step 2: Format context
        context = format_context(chunks)

        # Step 3: Build prompt
        prompt = RAG_TEMPLATE.format(context=context, question=question)

        # Step 4: Generate
        result = self.llm.generate(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT,
        )

        # Step 5: Validate
        guardrail = validate_response(result["content"])

        # Step 6: Format sources
        sources = []
        for chunk in chunks:
            sources.append({
                "section": chunk.get("metadata", {}).get("title", "Relatorio"),
                "content": chunk.get("text", "")[:300] + ("..." if len(chunk.get("text", "")) > 300 else ""),
                "similarity": round(chunk.get("similarity", 0) * 100, 1),
            })

        return {
            "answer": result["content"],
            "sources": sources,
            "model_used": result["model_used"],
            "guardrail_issues": guardrail["issues"],
        }

    def list_indexed_reports(self) -> List[str]:
        return self.store.list_reports()

    def get_report_chunk_count(self, report_id: Optional[str] = None) -> int:
        return self.store.count_chunks(report_id)
