# 📚 AcademIA – Assistente Inteligente de Documentos Acadêmicos

O **AcademIA** é um sistema de perguntas e respostas baseado em documentos PDF. O usuário pode enviar regulamentos, editais, matrizes curriculares e outros documentos acadêmicos, realizando perguntas em linguagem natural e recebendo respostas fundamentadas no conteúdo dos arquivos enviados.

---

## 🚀 Funcionalidades

- 📄 Upload de documentos PDF;
- 🧠 Extração automática do texto;
- 🔎 Geração de embeddings para busca semântica;
- 📚 Busca vetorial por similaridade;
- 💬 Perguntas em linguagem natural;
- 🤖 Respostas baseadas exclusivamente nos documentos enviados;
- 🎨 Interface web moderna e intuitiva;
- 📌 Exibição da fonte utilizada na resposta.

---


# 🛠 Tecnologias Utilizadas

## Front-end

- HTML5
- CSS3
- JavaScript

## Back-end

- Python
- FastAPI
- Uvicorn

## Inteligência Artificial

- Sentence Transformers
- Embeddings
- Busca Vetorial
- Similaridade do Cosseno

## Bibliotecas

- PyPDF2
- NumPy
- Scikit-Learn
- Transformers

---

# 📂 Estrutura do Projeto

```text
AcademIA/
│
├── iniciar.py
├── requirements.txt
│
├── src/
│   ├── api.py
│   ├── banco_vetorial.py
│   ├── busca.py
│   ├── embeddings.py
│   ├── ingestao.py
│   ├── resposta.py
│   ├── reranking.py
│   ├── validacao.py
│   ├── utilitarios.py
│   ├── frontend/
│         ├── index.html
│         ├── style.css
│         └── img/
└── README.md
```

---

# ⚙️ Instalação

Clone o repositório:

```bash
git clone https://github.com/ferinoSZ/AcademIA.git
```

Entre na pasta:

```bash
cd AcademIA
```

Crie um ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual:

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

# ▶ Executando o Projeto

Inicie o servidor:

```bash
python iniciar.py
```

Abra no navegador:

```text
vai dar erro na página, porém espere um momento até iniciar a aplicação
```

---

# 💡 Como Utilizar

1. Faça upload de um documento PDF;
2. Aguarde o processamento do arquivo;
3. Digite uma pergunta em linguagem natural;
4. O sistema localizará os trechos mais relevantes;
5. A IA gerará uma resposta baseada no conteúdo do documento.

---

# 🔎 Fluxo RAG

```text
PDF
 ↓
Extração do texto
 ↓
Chunking
 ↓
Embeddings
 ↓
Banco Vetorial
 ↓
Pergunta do usuário
 ↓
Embedding da pergunta
 ↓
Busca por Similaridade
 ↓
Reranking
 ↓
Validação
 ↓
Resposta
```

---

# 📸 Interface

### Principais recursos

- Upload de PDFs;
- Respostas fundamentadas nos documentos.

---

# 👨‍💻 Desenvolvedores

### Wesley Ferino de Carvalho
### Renan Queiroz Chavez
### Eduardo Rank
### Kauan Rogaleski

- 📧 Email: weslleycontas09@gmail.com
- 💼 LinkedIn: https://www.linkedin.com/in/wesley-ferino-190a83309
- 🐙 GitHub: https://github.com/ferinoSZ

---

# 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos e educacionais.

---

⭐ Caso tenha gostado do projeto, deixe uma estrela no repositório.
