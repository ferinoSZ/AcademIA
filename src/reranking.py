from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "BAAI/bge-reranker-v2-m3"
)
def rerank(pergunta, indices, chunks):
    pares = [
    (
        pergunta,
        f"{chunks[indice]['titulo']}\n\n{chunks[indice]['texto']}"
    )
    for indice in indices
    ]
    scores = reranker.predict(pares)
    resultados = []
    for score, indice in zip(scores, indices):
        resultados.append({
            "score": score,
            "indice": indice
        })
    resultados.sort(
        key=lambda x: x["score"],
        reverse=True
    )
    return resultados