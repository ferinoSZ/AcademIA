from ingestao import carregar_chunks
from embeddings import gerar_embeddings
from busca import buscar

pergunta = "Quais as principais regras para o uso de celulares em sala de aula?"

chunks = carregar_chunks()

vetores_chunks = gerar_embeddings(
    chunks
)

indices, similaridades = buscar(
    pergunta, 
    chunks, 
    vetores_chunks
)


print(f"\nPergunta:")
print(pergunta)

if melhor_score < 0.7:
    print("Nenhum resultado encontrado.")
else:
    print("\nResultados encontrados:")

    for posicao, indice in enumerate(
            reversed(indices),
            start=1):
        print(f"\n[{posicao}]")

        print(
            f"Score: "
            f"{similaridades[0][indice]:.4f}"
        )

        print(chunks[indice][:500])

        print("\n" + "-" * 50)