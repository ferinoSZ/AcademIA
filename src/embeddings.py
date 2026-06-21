from sentence_transformers import SentenceTransformer

modelo = SentenceTransformer(
    "intfloat/multilingual-e5-base"
)

def gerar_embeddings(chunks):
    textos_embedding = []

    for chunk in chunks:
        partes = [
            chunk["titulo"],
            chunk.get("subtitulo", ""),
            chunk["texto"]
        ]

        texto_embedding = "passage: " + "\n".join(
            parte for parte in partes if parte
        )
        textos_embedding.append(texto_embedding)
    return modelo.encode(textos_embedding)


def gerar_embedding_pergunta(pergunta):
    return modelo.encode(
        ["query: " + pergunta]
    )