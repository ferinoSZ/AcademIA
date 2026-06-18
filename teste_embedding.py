from sentence_transformers import SentenceTransformer

modelo = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

frases = [
    "Qual o prazo para trancar matrícula?",
    "Até quando posso cancelar minha matrícula?",
    "Como fazer estágio obrigatório?"
]

vetores = modelo.encode(frases)

print(vetores.shape)

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

modelo = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

frases = [
    "Qual o prazo para trancar matrícula?",
    "Até quando posso cancelar minha matrícula?",
    "Como fazer estágio obrigatório?"
]

vetores = modelo.encode(frases)

print(
    cosine_similarity(
        [vetores[0]],
        [vetores[1]]
    )
)

print(
    cosine_similarity(
        [vetores[0]],
        [vetores[2]]
    )
)