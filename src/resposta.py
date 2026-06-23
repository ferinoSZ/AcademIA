# ... existing code ...
def gerar_resposta(
        melhor,
        chunks):

    indice = melhor["indice"]

    # Pegamos APENAS esse pedaço exato, sem juntar com o resto do grupo
    chunk_encontrado = chunks[indice]

    return {
        "titulo": chunk_encontrado["titulo"],
        "pagina": chunk_encontrado["pagina"],
        "texto": chunk_encontrado["texto"]
    }