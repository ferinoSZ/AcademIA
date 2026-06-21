const fileInput = document.getElementById('fileInput');
const attachButton = document.getElementById('attachButton');
const dropzone = document.getElementById('dropzone');
const uploadList = document.getElementById('uploadList');
const conversationPanel = document.getElementById('conversationPanel');
const questionInput = document.getElementById('questionInput');
const sendButton = document.getElementById('sendButton');
const suggestionButtons = document.querySelectorAll('.suggestion');

const files = [];

// URL DO SEU BACK-END PYTHON
const BASE_URL = "http://localhost:8000";

function formatSize(bytes) {
    if (!bytes) return '0 KB';
    const units = ['B', 'KB', 'MB', 'GB'];
    let value = bytes;
    let index = 0;
    while (value >= 1024 && index < units.length - 1) {
        value /= 1024;
        index += 1;
    }
    return `${value.toFixed(value >= 10 || index === 0 ? 0 : 1)} ${units[index]}`;
}

function renderFiles() {
    uploadList.innerHTML = '';

    if (!files.length) {
        return;
    }

    files.forEach((file) => {
        const item = document.createElement('div');
        item.className = 'upload-item';
        item.innerHTML = `
            <div class="upload-meta">
                <strong title="${file.name}">${file.name}</strong>
                <span>${formatSize(file.size)} · PDF carregado</span>
            </div>
            <div class="chip" id="status-${file.name.replace(/[^a-zA-Z0-9]/g, '')}">Enviando...</div>
        `;
        uploadList.appendChild(item);
    });
}

function addConversationItem(role, text) {
    conversationPanel.classList.add('is-visible');
    const item = document.createElement('div');
    item.className = `conversation-item ${role}`;
    item.textContent = text;
    conversationPanel.appendChild(item);
    conversationPanel.scrollTop = conversationPanel.scrollHeight;
    return item; // Retornamos o elemento para podermos alterá-lo depois (ex: tirar o "Pensando...")
}

// ---------------------------------------------------------
// INTEGRAÇÃO 1: FUNÇÃO PARA ENVIAR O PDF PARA O BACK-END
// ---------------------------------------------------------
async function uploadFileToBackend(file) {
    const formData = new FormData();
    formData.append("file", file);

    const statusChip = document.getElementById(`status-${file.name.replace(/[^a-zA-Z0-9]/g, '')}`);

    try {
        const response = await fetch(`${BASE_URL}/api/upload`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        if(statusChip) statusChip.textContent = "PDF processado com sucesso";
        console.log(data.mensagem);
    } catch (error) {
        console.error("Erro no upload:", error);
        if(statusChip) {
            statusChip.textContent = "Erro no envio";
            statusChip.style.backgroundColor = "#ffcccc"; // Feedback visual de erro
        }
    }
}

function addFiles(selectedFiles) {
    const pdfFiles = Array.from(selectedFiles).filter((file) => file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf'));
    if (!pdfFiles.length) {
        dropzone.textContent = 'Somente arquivos PDF são aceitos.';
        return;
    }

    pdfFiles.forEach((file) => {
        if (!files.some((existing) => existing.name === file.name && existing.size === file.size)) {
            files.push(file);
            renderFiles(); // Renderiza na tela primeiro
            uploadFileToBackend(file); // Dispara o envio para o Python em segundo plano
        }
    });

    dropzone.textContent = files.length > 1 ? `${files.length} PDFs prontos para consulta.` : `${files[0].name} pronto para consulta.`;
}

attachButton.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', (event) => {
    addFiles(event.target.files);
    fileInput.value = '';
});

['dragenter', 'dragover'].forEach((eventName) => {
    dropzone.addEventListener(eventName, (event) => {
        event.preventDefault();
        event.stopPropagation();
        dropzone.classList.add('dragover');
    });
});

['dragleave', 'drop'].forEach((eventName) => {
    dropzone.addEventListener(eventName, (event) => {
        event.preventDefault();
        event.stopPropagation();
        dropzone.classList.remove('dragover');
    });
});

dropzone.addEventListener('drop', (event) => {
    addFiles(event.dataTransfer.files);
});

suggestionButtons.forEach((button) => {
    button.addEventListener('click', () => {
        questionInput.value = button.dataset.question || button.textContent.trim();
        questionInput.focus();
        questionInput.dispatchEvent(new Event('input'));
    });
});

function autosize() {
    questionInput.style.height = 'auto';
    questionInput.style.height = `${Math.min(questionInput.scrollHeight, 120)}px`;
}

questionInput.addEventListener('input', () => {
    autosize();
    sendButton.disabled = !questionInput.value.trim();
});

questionInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendButton.click();
    }
});

// ---------------------------------------------------------
// INTEGRAÇÃO 2: ENVIAR A PERGUNTA E RECEBER A RESPOSTA RAG
// ---------------------------------------------------------
sendButton.addEventListener('click', async () => {
    const perguntaTexto = questionInput.value.trim();
    if (!perguntaTexto) return;

    // 1. Adiciona a pergunta do usuário na tela
    addConversationItem('user', perguntaTexto);
    
    // 2. Limpa o input
    questionInput.value = '';
    autosize();
    sendButton.disabled = true;

    // 3. Adiciona o balão temporário do assistente (indicador de carregamento)
    const respostaNode = addConversationItem('assistant', 'Consultando os regulamentos...');

    // 4. Faz a requisição real para o Python
    try {
        const response = await fetch(`${BASE_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ pergunta: perguntaTexto })
        });

        const data = await response.json();
        
        // 5. Substitui o texto temporário pela resposta real do LLM
        respostaNode.textContent = data.resposta;

    } catch (error) {
        console.error("Erro na consulta:", error);
        respostaNode.textContent = "Erro de conexão. Verifique se o servidor Python está rodando.";
    }
});

autosize();
sendButton.disabled = true;