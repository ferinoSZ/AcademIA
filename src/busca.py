from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from embeddings import gerar_embedding_pergunta

def buscar(pergunta, chunks, vetores_chunks,):

    vetor_pergunta = gerar_embedding_pergunta(pergunta)

    similaridades = cosine_similarity(
        vetor_pergunta, 
        vetores_chunks
    )

    indices = np.argsort(
        similaridades[0]
    )[-3:]

    return indices, similaridades