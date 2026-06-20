from ingestao import carregar_chunks
from embeddings import gerar_embeddings
from busca import buscar
from reranking import rerank

# aqui é aonde coloco a pergunta, por enquanto é assim, mas logo vou colcoa input
pergunta = "como funciona o achados e perdidos?"

#carregar os chunks do pdf
chunks = carregar_chunks()

# gerar os embeddings(vetores) dos chunks
vetores_chunks = gerar_embeddings(
    chunks
)

# buscar os chunks mais relevantes para a pergunta
indices = buscar(
    pergunta,
    vetores_chunks
)

# aqui vai classificar as respostas mais de acordo com a pergunta, e depois pegar a melhor resposta
resultados = rerank(
    pergunta,
    indices,
    chunks
)


melhor = None

# esse for é para pegar o melhor resultado, ou seja, o resultado mais relevante para a pergunta, e que tenha um score maior que 0, ou seja, que tenha alguma relevância para a pergunta
for resultado in resultados:

    if resultado["score"] > 0:
        melhor = resultado
        break

# se melhor for None, ou seja, se não tiver encontrado nenhuma resposta  para a pergunta
#pode mexer aqui, você vai ter que mexer aqui eu acho (Renan)
if melhor is None:

    print()
    print("Não encontrei informações suficientes.")
    exit()

indice = melhor["indice"]

# aqui ele vai pegar o grupo do melhor resultado
grupo = chunks[indice]["grupo"]

# vai seleiconar todos os chunks do mesmo grupo, ou seja, do mesmo tópico
chunks_grupo = [
    chunk
    for chunk in chunks
    if chunk["grupo"] == grupo
]

# aqui ele vai ordenar os chunks de acordo com a ordem que aparece no PDF
chunks_grupo.sort(
    key=lambda x: x["ordem"]
)

# junta os textos dos chunks do mesmo grupo em um unico texto
texto = "\n".join(
    chunk["texto"]
    for chunk in chunks_grupo
)



print()

print(
    f"Título: {chunks[indice]['titulo']}"
)

print(
    f"Página: {chunks[indice]['pagina']}"
)

print()

print(texto)