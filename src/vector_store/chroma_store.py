import os
import json
import hashlib
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings

from src.config import CHROMA_PERSIST_DIR, TOP_K_CHUNKS
from src.embeddings.embedder import embed_texts, embed_query


class ChromaStore:
    def __init__(self, persist_dir: str = None):
        if persist_dir is None:
            persist_dir = CHROMA_PERSIST_DIR
        self.persist_dir = persist_dir
        os.makedirs(persist_dir, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False),
        )
        self.collection_name = "genera_reports"
        self._ensure_collection()

    def _ensure_collection(self):
        try:
            self.collection = self.client.get_collection(self.collection_name)
        except Exception:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"},
            )

    def _make_chunks(self, report: dict) -> List[dict]:
        """
        Split a report JSON into chunks — one per section item or major subsection.
        Each chunk is a dict with text and metadata for traceability.
        """
        chunks = []
        report_id = report["report_id"]
        patient = report.get("patient_name", "")

        for section_key, section in report["sections"].items():
            section_title = section.get("title", section_key)

            # Add section description as chunk
            if section.get("description"):
                chunks.append({
                    "text": f"[{section_title}] {section['description']}",
                    "metadata": {
                        "report_id": report_id,
                        "patient": patient,
                        "section": section_key,
                        "subsection": "descricao",
                        "title": section_title,
                    }
                })

            # Add ancestralidade as one text block
            if section_key == "ancestralidade" and "data" in section:
                ancestry_parts = []
                for ancestry, info in section["data"].items():
                    regions = ", ".join(info.get("regioes", []))
                    ancestry_parts.append(f"{ancestry}: {info['percentage']}% (regioes: {regions})")
                text = "Composicao Ancestral: " + " | ".join(ancestry_parts)
                if section.get("interpretation"):
                    text += f"\nInterpretacao: {section['interpretation']}"
                chunks.append({
                    "text": text,
                    "metadata": {
                        "report_id": report_id,
                        "patient": patient,
                        "section": section_key,
                        "subsection": "dados",
                        "title": section_title,
                    }
                })

            # Add each data item as a chunk (for lists)
            elif "data" in section and isinstance(section["data"], list):
                for idx, item in enumerate(section["data"]):
                    condition = item.get("condition") or item.get("trait") or item.get("drug") or item.get("condition", "")
                    gene = item.get("gene", "")
                    variant = item.get("variant", "")
                    status = item.get("status", "")
                    risk = item.get("risk_level", "")
                    result = item.get("result", "")
                    details = item.get("details", "")
                    prevalence = item.get("prevalence_general", "")
                    estimated = item.get("your_estimated_risk", "")
                    regions_str = item.get("regions", "")

                    # Build structured text
                    parts = [f"[{section_title}] {condition}"]
                    if gene:
                        parts.append(f"Gene(s): {gene}")
                    if variant:
                        parts.append(f"Variante(s): {variant}")
                    if risk:
                        parts.append(f"Nivel de risco: {risk}")
                    if result:
                        parts.append(f"Resultado: {result}")
                    if status:
                        parts.append(f"Status: {status}")
                    if prevalence:
                        parts.append(f"Prevalencia na populacao: {prevalence}")
                    if estimated:
                        parts.append(f"Risco estimado: {estimated}")
                    if details:
                        parts.append(f"Detalhes: {details}")
                    if regions_str:
                        parts.append(f"Regioes: {regions_str}")

                    chunk_text = "\n".join(parts)

                    chunks.append({
                        "text": chunk_text,
                        "metadata": {
                            "report_id": report_id,
                            "patient": patient,
                            "section": section_key,
                            "subsection": condition or item.get("condition", ""),
                            "title": section_title,
                            "chunk_index": idx,
                        }
                    })

        return chunks

    def index_report(self, report: dict) -> int:
        """
        Index a report by chunking it, generating embeddings, and storing in Chroma.
        Returns number of chunks indexed.
        """
        report_id = report["report_id"]

        # Remove existing chunks for this report
        try:
            existing = self.collection.get(where={"report_id": report_id})
            if existing and existing["ids"]:
                self.collection.delete(ids=existing["ids"])
        except Exception:
            pass

        chunks = self._make_chunks(report)
        if not chunks:
            return 0

        texts = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]

        # Generate unique IDs
        ids = []
        for i, c in enumerate(chunks):
            hash_input = f"{report_id}_{c['metadata']['section']}_{c['metadata']['subsection']}_{i}"
            ids.append(hashlib.md5(hash_input.encode()).hexdigest())

        # Generate embeddings in batches of 50
        all_embeddings = []
        batch_size = 50
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_embeddings = embed_texts(batch_texts)
            all_embeddings.extend(batch_embeddings)

        # Insert into Chroma
        self.collection.add(
            ids=ids,
            embeddings=all_embeddings,
            documents=texts,
            metadatas=metadatas,
        )

        return len(chunks)

    def search(self, query: str, k: int = None, report_id: Optional[str] = None) -> List[dict]:
        """
        Search for relevant chunks given a query.
        Returns list of dicts with text, metadata, and distance.
        """
        if k is None:
            k = TOP_K_CHUNKS

        query_embedding = embed_query(query)

        where_filter = None
        if report_id:
            where_filter = {"report_id": report_id}

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )

        formatted = []
        if results and results["ids"] and results["ids"][0]:
            for i in range(len(results["ids"][0])):
                formatted.append({
                    "text": results["documents"][0][i] if results["documents"] else "",
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": float(results["distances"][0][i]) if results["distances"] else 0.0,
                    "similarity": 1.0 - float(results["distances"][0][i]) if results["distances"] else 0.0,
                })

        return formatted

    def delete_report(self, report_id: str):
        try:
            existing = self.collection.get(where={"report_id": report_id})
            if existing and existing["ids"]:
                self.collection.delete(ids=existing["ids"])
        except Exception:
            pass

    def list_reports(self) -> List[str]:
        try:
            results = self.collection.get(include=["metadatas"])
            if not results or not results["metadatas"]:
                return []
            report_ids = set()
            for meta in results["metadatas"]:
                if meta and "report_id" in meta:
                    report_ids.add(meta["report_id"])
            return sorted(report_ids)
        except Exception:
            return []

    def count_chunks(self, report_id: Optional[str] = None) -> int:
        try:
            if report_id:
                results = self.collection.get(where={"report_id": report_id})
            else:
                results = self.collection.get()
            if results and results["ids"]:
                return len(results["ids"])
            return 0
        except Exception:
            return 0
