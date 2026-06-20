from sentence_transformers import SentenceTransformer

modelo = SentenceTransformer(
    "intfloat/multilingual-e5-base"
)

def gerar_embeddings(chunks):
    #aqui vai armazenar os textos dos chunks em uma lista, para depois gerar os embeddings
    textos_embedding = []

    # vai percorrer cada chunk do documento
    for chunk in chunks:
        # vai juntar o título, subtítulo e texto do chunk em um único texto, para dar contexto ao modelo de embeddings
        partes = [
            chunk["titulo"],
            chunk.get("subtitulo", ""),
            chunk["texto"]
        ]

        # monta texto completo do chunk e adiciona um prefixo "passage"
        # para o modelo de embeddings entender que é um texto de contexto, e não uma pergunta
        texto_embedding = "passage: " + "\n".join(
            parte for parte in partes if parte
        )
        # adiciona o texto do chunk na lista de textos para gerar os embeddings mas preparado
        textos_embedding.append(texto_embedding)
    # aqui vai converter todos os textos em vetores
    return modelo.encode(textos_embedding)


def gerar_embedding_pergunta(pergunta):
    # aqui ele vai adicionar um prefixo "query" na pergunta
    return modelo.encode(
        ["query: " + pergunta]
    )