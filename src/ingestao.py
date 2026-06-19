from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def carregar_chunks():
    reader = PdfReader("documentos/regulamentos.pdf")
    texto = ""

    for pagina in reader.pages:
        texto += pagina.extract_text()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=675,
        chunk_overlap=100
    )

    chunks = splitter.split_text(texto)
    
    return chunks