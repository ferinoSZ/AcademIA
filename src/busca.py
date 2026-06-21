from src.embeddings import gerar_embedding_pergunta
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def buscar(pergunta, vetores_chunks, quantidade=10):
    vetor_pergunta = gerar_embedding_pergunta(
        pergunta
    )
    similaridades = cosine_similarity(
        vetor_pergunta,
        vetores_chunks
    )
    indices = np.argsort(
        similaridades[0]
    )[-quantidade:][::-1]

    return indices