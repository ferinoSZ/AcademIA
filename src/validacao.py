from src.utilitarios import pegar_palavras_importantes

LIMIAR_SCORE = 0.0
LIMIAR_COBERTURA = 0.35
LIMIAR_MARGEM = 0.15


def calcular_cobertura(pergunta, chunk):

    palavras_pergunta = pegar_palavras_importantes(
        pergunta
    )

    if not palavras_pergunta:
        return 0

    texto_chunk = chunk["titulo"] + " " + chunk["texto"]

    palavras_chunk = pegar_palavras_importantes(
        texto_chunk
    )

    encontradas = palavras_pergunta.intersection(
        palavras_chunk
    )

    return len(encontradas) / len(
        palavras_pergunta
    )


def validar_resultado(
        resultados,
        chunks,
        pergunta):

    melhor = None
    motivo = "nenhum trecho encontrado"

    if resultados:

        melhor_candidato = resultados[0]

        segundo_candidato = (
            resultados[1]
            if len(resultados) > 1
            else None
        )

        indice = melhor_candidato["indice"]

        cobertura = calcular_cobertura(
            pergunta,
            chunks[indice]
        )

        melhor_candidato["cobertura"] = cobertura

        if melhor_candidato["score"] < LIMIAR_SCORE:

            motivo = "score baixo"

        elif cobertura < LIMIAR_COBERTURA:

            motivo = "baixa cobertura"

        elif (
            segundo_candidato
            and
            melhor_candidato["score"]
            - segundo_candidato["score"]
            < LIMIAR_MARGEM
        ):

            motivo = "ambiguidade"

        else:

            melhor = melhor_candidato

    return melhor, motivo