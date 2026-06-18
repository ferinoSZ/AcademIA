from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

pergunta = "Como funciona o estacionamento para alunos?"

reader = PdfReader("documentos/regulamentos.pdf")
texto = ""

paginas = []

for numero, pagina in enumerate(reader.pages):
    texto_pagina = pagina.extract_text()

    paginas.append({
        "texto": texto_pagina,
        "pagina": numero + 1
    })

modelo = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=675,
    chunk_overlap=100
)

texto_completo = ""

for pagina in paginas:
    texto_completo += (
        f"\n[Pagina {pagina['pagina']}]\n"
        + pagina["texto"]
    )

chunks = splitter.split_text(texto_completo)
vetores_chunks = modelo.encode(chunks)

vetor_pergunta = modelo.encode([pergunta])

similaridades = cosine_similarity(
    vetor_pergunta,
    vetores_chunks
)

indice_melhor = np.argmax(similaridades)
indices = np.argsort(similaridades[0])[-3:]

print(f"\nPergunta:")
print(pergunta)

print("\nResultados Encontrados:")

for posicao, indice in enumerate(reversed(indices), start=1):

    print(f"\n[{posicao}]")

    print(
        f"Score: {similaridades[0][indice]:.4f}"
    )

    print(chunks[indice][:500])

    print("\n" + "-" * 50)

melhor_indice = indices[-1]

print("\n" + "=" * 50)
print("RESPOSTA PRINCIPAL")
print("=" * 50)

print(chunks[melhor_indice])

print(
    f"\nScore: {similaridades[0][melhor_indice]:.4f}"
)
