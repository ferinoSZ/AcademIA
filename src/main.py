import uvicorn

from banco_vetorial import carregar_ou_criar_banco
from busca import buscar
from reranking import rerank
from validacao import validar_resultado
from resposta import gerar_resposta


chunks, vetores_chunks = carregar_ou_criar_banco()

indices = buscar(
    pergunta,
    vetores_chunks
)

resultados = rerank(
    pergunta,
    indices,
    chunks
)

melhor, motivo = validar_resultado(
    resultados,
    chunks,
    pergunta
)

if melhor is None:

    print()
    print("Não encontrei informações suficientes.")
    print(f"Motivo: {motivo}")
    exit()

resposta = gerar_resposta(
    melhor,
    chunks
)

print()
print(
    f"Título: {resposta['titulo']}"
)

print(
    f"Página: {resposta['pagina']}"
)

print()

print(
    resposta["texto"]
)

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )