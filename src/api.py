import os
import shutil

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from banco_vetorial import (
    carregar_ou_criar_banco,
    ARQUIVO_PDF,
    ARQUIVO_CHUNKS,
    ARQUIVO_EMBEDDINGS
)

from busca import buscar
from reranking import rerank
from validacao import validar_resultado
from resposta import gerar_resposta


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Pergunta(BaseModel):
    pergunta: str


@app.post("/api/upload")
async def upload_pdf(
        file: UploadFile = File(...)
):

    ARQUIVO_PDF.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
            ARQUIVO_PDF,
            "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    if ARQUIVO_CHUNKS.exists():
        os.remove(ARQUIVO_CHUNKS)

    if ARQUIVO_EMBEDDINGS.exists():
        os.remove(ARQUIVO_EMBEDDINGS)

    carregar_ou_criar_banco()

    return {
        "mensagem": "PDF processado com sucesso."
    }


@app.post("/api/chat")
async def chat(
        dados: Pergunta
):

    pergunta = dados.pergunta

    chunks, vetores_chunks = (
        carregar_ou_criar_banco()
    )

    indices = buscar(
        pergunta,
        vetores_chunks
    )

    resultados = rerank(
        pergunta,
        indices,
        chunks
    )

    melhor, motivo = validar_resultado(
        resultados,
        chunks,
        pergunta
    )

    if melhor is None:

        return {
            "resposta":
            (
                "Não encontrei informações suficientes "
                "no documento.\n"
                f"Motivo: {motivo}"
            )
        }

    resposta = gerar_resposta(
        melhor,
        chunks
    )

    resposta_final = (
        f"Título: {resposta['titulo']}\n"
        f"Página: {resposta['pagina']}\n\n"
        f"{resposta['texto']}"
    )

    return {
        "resposta": resposta_final
    }