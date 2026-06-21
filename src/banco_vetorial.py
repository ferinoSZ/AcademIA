import json
from pathlib import Path

import numpy as np

from embeddings import gerar_embeddings
from ingestao import carregar_chunks

BASE_DIR = Path(__file__).resolve().parent.parent

PASTA_DADOS = BASE_DIR / "dados"
ARQUIVO_CHUNKS = PASTA_DADOS / "chunks.json"
ARQUIVO_EMBEDDINGS = PASTA_DADOS / "embeddings.npy"

ARQUIVO_PDF = BASE_DIR / "documentos" / "regulamentos.pdf"


def banco_esta_atualizado():
    if not ARQUIVO_PDF.exists():
        raise FileNotFoundError(f"PDF não encontrado: {ARQUIVO_PDF}")

    if not ARQUIVO_CHUNKS.exists() or not ARQUIVO_EMBEDDINGS.exists():
        return False

    data_banco = min(
        ARQUIVO_CHUNKS.stat().st_mtime,
        ARQUIVO_EMBEDDINGS.stat().st_mtime
    )

    return data_banco >= ARQUIVO_PDF.stat().st_mtime


def salvar_banco(chunks, vetores_chunks):
    PASTA_DADOS.mkdir(exist_ok=True)

    with ARQUIVO_CHUNKS.open("w", encoding="utf-8") as arquivo:
        json.dump(
            chunks,
            arquivo,
            ensure_ascii=False,
            indent=2
        )

    np.save(
        ARQUIVO_EMBEDDINGS,
        vetores_chunks
    )


def carregar_banco():
    with ARQUIVO_CHUNKS.open("r", encoding="utf-8") as arquivo:
        chunks = json.load(arquivo)

    vetores_chunks = np.load(ARQUIVO_EMBEDDINGS)

    return chunks, vetores_chunks


def carregar_ou_criar_banco():
    if banco_esta_atualizado():
        return carregar_banco()

    chunks = carregar_chunks(ARQUIVO_PDF)
    vetores_chunks = gerar_embeddings(chunks)

    salvar_banco(
        chunks,
        vetores_chunks
    )

    return chunks, vetores_chunks