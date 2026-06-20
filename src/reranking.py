from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "BAAI/bge-reranker-base"
)
# aqui ele vai receber a pergunta, os indices dos chunks mais similares e os chunks em si
def rerank(pergunta, indices, chunks):
    # aqui ele vai criar uma lista de pares, onde cada par é composto pela pergunta e o texto do chunk correspondente ao indice
    pares = [
    (
        pergunta,
        f"{chunks[indice]['titulo']}\n\n{chunks[indice]['texto']}"
    )
    # aqui ele vai percorrer os indices dos chunks mais similares para criar os pares
    for indice in indices
    ]
    # aqui ele vai calcular os scores para cada par
    scores = reranker.predict(pares)
    # aqui essa lista é para os resultados, onde cada resultado é um dicionário com o score e o indice do chunk correspondente
    resultados = []
    # aqui ele vai percorrer os scores e os indices para criar a lista de resultados
    for score, indice in zip(scores, indices):
        # aqui ele vai adicionar o score e o indice do chunk correspondente na lista de resultados
        resultados.append({
            "score": score,
            "indice": indice
        })
    # aqui ele vai ordenar os resultados de acordo com o score, do maior para o menor
    resultados.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return resultados