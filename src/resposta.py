def gerar_resposta(
        melhor,
        chunks):

    indice = melhor["indice"]

    grupo = chunks[indice]["grupo"]

    chunks_grupo = [

        chunk

        for chunk in chunks

        if chunk["grupo"] == grupo

    ]

    chunks_grupo.sort(
        key=lambda x: x["ordem"]
    )

    texto = "\n".join(

        chunk["texto"]

        for chunk in chunks_grupo

    )

    return {
        "titulo": chunks[indice]["titulo"],
        "pagina": chunks[indice]["pagina"],
        "texto": texto
    }