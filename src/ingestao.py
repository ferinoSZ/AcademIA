from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# identifica se a linha é um título, ou seja, se ela está em caixa alta e tem no máximo 8 palavras
def eh_titulo(linha):
    # aqui ele vai remover os espaços em branco no início e no final da linha
    linha = linha.strip()
    # se a linha estiver vazia, ou seja, se não tiver nenhum caractere, ela não é um título
    if not linha:
        return False
    # se a linha for composta apenas por números, ela não é um título
    if linha.isdigit():
        return False
    # aqui ele vai verificar se a linha está em caixa alta e tem no máximo 8 palavras, se for verdade, ela é um título
    return (
        linha.isupper()
        and len(linha.split()) <= 8
    )
# identifica se a linha é um subtitulo, ou seja, se ela não está em caixa alta, tem no máximo 4 palavras e não termina com ponto final
def eh_subtitulo(linha):
    # aqui ele vai remover os espaços em branco no início e no final da linha
    linha = linha.strip()
    # se a linha estiver vazia, ou seja, se não tiver nenhum caractere, ela não é um subtítulo
    return (
        not linha.isupper()
        and len(linha.split()) <= 4
        and not linha.endswith(".")
    )
# aqui ele vai carregar o PDF
def carregar_chunks(caminho_pdf="documentos/regulamentos.pdf"):
    reader = PdfReader(caminho_pdf)
    # aqui ele vai dividir o texto em chunks
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
    # vai percorrer todas as páginas do PDF, usando a função enumerate para ter o número da página e o conteúdo da página
    for numero_pagina, pagina in enumerate(reader.pages):
        # extrai o texto da página atual
        texto_pagina = pagina.extract_text()
        # ignora páginas sem textos
        if not texto_pagina:
            continue
        #divide os textos da página em linhas, usando o \n como separador
        linhas = texto_pagina.split("\n")
        # percorre linha por linha da página
        for linha in linhas:
            # remove os espaços em branco no início e no final da linha
            linha = linha.strip()
            # ignora linhas vazias
            if not linha:
                continue
            # ignora número das páginas
            if linha.isdigit():
                continue
            # verifica se a linha é um título, usando a função eh_titulo
            if eh_titulo(linha):
                # se existe texto acumulado, divide em chunks e armazena
                if texto_atual:
                    # divide chunks em subchunks menores
                    subchunks = splitter.split_text(
                        texto_atual.strip()
                    )
                    # percorre os subchunks 
                    for ordem, subchunk in enumerate(subchunks):
                        # armazena chunk com suas informações de contexto
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
    # salva o último grupo de texto do documento 
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