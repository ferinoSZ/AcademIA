from sentence_transformers import SentenceTransformer
import sentence_transformers

modelo = sentence_transformers.SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

def gerar_embeddings(chunks):

    vetores_chunks = modelo.encode(chunks)

    return vetores_chunks

def gerar_embedding_pergunta(pergunta):
    return modelo.encode([pergunta])