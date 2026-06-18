from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

reader = PdfReader("documentos/regulamentos.pdf")

texto = ""

for pagina in reader.pages:
    texto += pagina.extract_text()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_text(texto)

print("Quantidade de chunks:", len(chunks))
print("\nPrimeiro chunk:\n")
print(chunks[0])