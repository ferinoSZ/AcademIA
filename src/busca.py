from embeddings import gerar_embedding_pergunta
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def buscar(pergunta, vetores_chunks):
    # variavel para armazenar o vetor da pergunta
    vetor_pergunta = gerar_embedding_pergunta(
        pergunta
    )
    # aqui ele vai calcular a similaridade entre o vetor da pergunta e os vetores dos chunks
    similaridades = cosine_similarity(
        vetor_pergunta,
        vetores_chunks
    )
    # aqui ele vai pegar os indices dos 10 chunks mais similares a pergunta
    indices = np.argsort(
        similaridades[0]
    )[-10:]

    return indices


def buscar_no_banco_vetorial(vetor_pergunta, colecao, num_resultados=10):
    """
    Busca no banco vetorial usando Chroma.
    
    Args:
        vetor_pergunta: Embedding da pergunta (numpy array)
        colecao: Coleção Chroma
        num_resultados: Número de resultados a retornar
    
    Returns:
        Array de índices dos chunks mais similares
    """
    # Converte vetor para lista se necessário
    if hasattr(vetor_pergunta, 'tolist'):
        vetor_lista = vetor_pergunta[0].tolist() if len(vetor_pergunta.shape) > 1 else vetor_pergunta.tolist()
    else:
        vetor_lista = vetor_pergunta
    
    # Busca no banco
    resultados = colecao.query(
        query_embeddings=[vetor_lista],
        n_results=num_resultados,
        include=["distances", "embeddings", "metadatas", "documents"]
    )
    
    # Extrai índices (converte IDs para números)
    indices = np.array([int(id_) for id_ in resultados["ids"][0]])
    
    return indices