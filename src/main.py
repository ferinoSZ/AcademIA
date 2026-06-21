from banco_vetorial import carregar_ou_criar_banco
from busca import buscar
from reranking import rerank

LIMIAR_SCORE = 1.0
LIMIAR_COBERTURA = 0.35
LIMIAR_MARGEM = 0.30

PALAVRAS_IGNORADAS = {
    "como", "funciona", "qual", "quais", "sobre",
    "para", "com", "que", "uma", "um",
    "dos", "das", "do", "da", "de",
    "os", "as", "ao", "aos", "em", "por",
}


def pegar_palavras_importantes(texto):
    texto_limpo = ""

    for caractere in texto.lower():
        if caractere.isalnum():
            texto_limpo += caractere
        else:
            texto_limpo += " "

    return {
        palavra
        for palavra in texto_limpo.split()
        if len(palavra) >= 3 and palavra not in PALAVRAS_IGNORADAS
    }


def calcular_cobertura(pergunta, chunk):
    palavras_pergunta = pegar_palavras_importantes(pergunta)

    if not palavras_pergunta:
        return 0

    texto_chunk = chunk["titulo"] + " " + chunk["texto"]
    palavras_chunk = pegar_palavras_importantes(texto_chunk)
    encontradas = palavras_pergunta.intersection(palavras_chunk)

    return len(encontradas) / len(palavras_pergunta)

# aqui é aonde coloco a pergunta, por enquanto é assim, mas logo vou colcoa input
pergunta = "como funciona o achados e perdidos?"

# carrega o banco vetorial simples
# se nao existir, ele le o PDF, gera os embeddings e salva em dados/
chunks, vetores_chunks = carregar_ou_criar_banco()

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
motivo_recusa = "nenhum trecho candidato foi encontrado"

if resultados:
    melhor_candidato = resultados[0]
    segundo_candidato = resultados[1] if len(resultados) > 1 else None
    indice_candidato = melhor_candidato["indice"]
    cobertura = calcular_cobertura(
        pergunta,
        chunks[indice_candidato]
    )

    melhor_candidato["cobertura"] = cobertura

    if melhor_candidato["score"] < LIMIAR_SCORE:
        motivo_recusa = "o score do melhor trecho ficou baixo"
    elif cobertura < LIMIAR_COBERTURA:
        motivo_recusa = "o trecho nao tem palavras suficientes da pergunta"
    elif (
        segundo_candidato
        and melhor_candidato["score"] - segundo_candidato["score"] < LIMIAR_MARGEM
    ):
        motivo_recusa = "existem trechos parecidos demais, entao ficou ambiguo"
    else:
        melhor = melhor_candidato

# se melhor for None, ou seja, se não tiver encontrado nenhuma resposta  para a pergunta
#pode mexer aqui, você vai ter que mexer aqui eu acho (Renan)
if melhor is None:

    print()
    print("Não encontrei informações suficientes.")
    print(f"Motivo: {motivo_recusa}.")
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

print(
    f"Confiança: score={melhor['score']:.2f} | cobertura={melhor['cobertura']:.0%}"
)

print()

print(texto)