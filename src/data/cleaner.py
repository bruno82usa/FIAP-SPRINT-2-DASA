"""
Normalizacao e limpeza de textos geneticos para alimentacao do modelo de linguagem.
Remove ruidos, normaliza terminologia e prepara textos para chunking e embedding.
"""

import re
import unicodedata


def remove_accents(text: str) -> str:
    """Remove acentos mantendo a legibilidade (para compatibilidade)."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize_gene_names(text: str) -> str:
    """Normaliza nomes de genes para formato padrao (uppercase)."""
    # Match gene patterns like BRCA1, TCF7L2, HLA-DQ2
    pattern = r"\b([A-Z]{2,}[0-9]*[A-Z]*(?:[-/][A-Z0-9]+)*)\b"
    return re.sub(pattern, lambda m: m.group(1).upper(), text)


def normalize_variant_notation(text: str) -> str:
    """Normaliza notacao de variantes (rsID, delecoes, etc.)."""
    # Ensure rsIDs are lowercase and consistent
    text = re.sub(r"\bRS(\d+)\b", r"rs\1", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(rs\d+)\b", lambda m: m.group(1).lower(), text)
    return text


def clean_special_characters(text: str) -> str:
    """Remove caracteres nao imprimiveis e normaliza espacos."""
    # Remove non-printable characters except newlines
    text = re.sub(r"[^\S\n]+", " ", text)
    # Normalize multiple spaces
    text = re.sub(r" {2,}", " ", text)
    # Remove spaces before punctuation
    text = re.sub(r" +([.,;:!?)])", r"\1", text)
    # Remove trailing spaces per line
    text = "\n".join(line.strip() for line in text.split("\n"))
    # Remove empty lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def normalize_medical_terms(text: str) -> str:
    """Normaliza termos medicos comuns para consistencia."""
    replacements = {
        "doenca": "doenca",
        "diabetes mellitus": "diabetes mellitus",
        "cancer": "cancer",
        "hipertensao arterial": "hipertensao arterial",
        "mellitus": "mellitus",
        "falciforme": "falciforme",
        "celiaca": "celiaca",
        "celiaco": "celiaca",
    }
    for wrong, correct in replacements.items():
        text = re.sub(rf"\b{re.escape(wrong)}\b", correct, text, flags=re.IGNORECASE)
    return text


def clean_genetic_text(text: str) -> str:
    """
    Pipeline completo de limpeza de texto genetico.
    Aplica normalizacao de genes, variantes, termos medicos e caracteres.
    """
    text = normalize_gene_names(text)
    text = normalize_variant_notation(text)
    text = normalize_medical_terms(text)
    text = clean_special_characters(text)
    return text


def chunk_text_by_tokens(text: str, max_chars: int = 1000, overlap: int = 100) -> list[str]:
    """
    Divide texto em chunks com overlap para janelas deslizantes.
    Usado quando chunks precisam de contexto cruzado.
    """
    if len(text) <= max_chars:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        # Try to break at sentence boundary
        if end < len(text):
            last_period = text.rfind(".", start, end)
            if last_period > start + max_chars // 2:
                end = last_period + 1

        chunks.append(text[start:end].strip())
        start = end - overlap

    return chunks
