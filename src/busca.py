from src.embeddings import gerar_embedding_pergunta
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def buscar(pergunta, vetores_chunks, quantidade=10):
    # variavel para armazenar o vetor da pergunta
    vetor_pergunta = gerar_embedding_pergunta(
        pergunta
    )
    # aqui ele vai calcular a similaridade entre o vetor da pergunta e os vetores dos chunks
    similaridades = cosine_similarity(
        vetor_pergunta,
        vetores_chunks
    )
    # aqui ele vai pegar os indices dos chunks mais similares a pergunta
    indices = np.argsort(
        similaridades[0]
    )[-quantidade:][::-1]

    return indices