from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def eh_titulo(linha):
    linha = linha.strip()
    if not linha:
        return False
    if linha.isdigit():
        return False
    return (
        linha.isupper()
        and len(linha.split()) <= 8
    )
def eh_subtitulo(linha):
    linha = linha.strip()
    return (
        not linha.isupper()
        and len(linha.split()) <= 4
        and not linha.endswith(".")
    )
def carregar_chunks(caminho_pdf="documentos/regulamentos.pdf"):
    reader = PdfReader(caminho_pdf)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "; ",
            ", ",
            " "
        ]
    )

    chunks = []

    titulo_atual = "SEM TÍTULO"
    texto_atual = ""
    pagina_atual = 1
    id_chunk = 0
    grupo = 0
    for numero_pagina, pagina in enumerate(reader.pages):
        texto_pagina = pagina.extract_text()
        if not texto_pagina:
            continue
        linhas = texto_pagina.split("\n")
        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue
            if linha.isdigit():
                continue
            if eh_titulo(linha):
                if texto_atual:
                    subchunks = splitter.split_text(
                        texto_atual.strip()
                    )
                    for ordem, subchunk in enumerate(subchunks):
                        chunks.append({
                            "id": id_chunk,
                            "grupo": grupo,
                            "ordem": ordem,
                            "titulo": titulo_atual,
                            "texto": subchunk,
                            "pagina": pagina_atual
                        })

                        id_chunk += 1
                    grupo += 1
                titulo_atual = linha
                pagina_atual = numero_pagina + 1
                texto_atual = ""
            else:
                texto_atual += linha + "\n"
    if texto_atual:

        subchunks = splitter.split_text(
            texto_atual.strip()
        )

        for ordem, subchunk in enumerate(subchunks):

            chunks.append({
                "id": id_chunk,
                "grupo": grupo,
                "ordem": ordem,
                "titulo": titulo_atual,
                "texto": subchunk,
                "pagina": pagina_atual
            })

            id_chunk += 1

    return chunks