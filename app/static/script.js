document.addEventListener('DOMContentLoaded', function() {
    const chatLog = document.getElementById('chat-log');
    const questionInput = document.getElementById('question');
    const sendBtn = document.getElementById('send-btn');
    const uploadForm = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');
    const uploadMessage = document.getElementById('upload-message');

    // Режим (передан из шаблона)
    const mode = window.MODE || 'rag';

    function addMessage(text, sender) {
        const msg = document.createElement('div');
        msg.className = sender;
        msg.textContent = text;
        chatLog.appendChild(msg);
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    // Отправка вопроса
    sendBtn.addEventListener('click', async function() {
        const question = questionInput.value.trim();
        if (!question) return;
        addMessage(question, 'user');
        questionInput.value = '';
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question, mode })
            });
            const data = await response.json();
            if (response.ok) {
                addMessage(data.answer, 'agent');
            } else {
                addMessage('Ошибка: ' + data.detail, 'agent');
            }
        } catch (error) {
            addMessage('Ошибка сети: ' + error.message, 'agent');
        }
    });

    questionInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendBtn.click();
    });

    // Загрузка файла (только если есть форма)
    if (uploadForm) {
        uploadForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const file = fileInput.files[0];
            if (!file) {
                uploadMessage.textContent = 'Пожалуйста, выберите файл.';
                uploadMessage.style.color = 'red';
                return;
            }
            const formData = new FormData();
            formData.append('file', file);
            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                if (response.ok) {
                    uploadMessage.textContent = data.message + ` (добавлено чанков: ${data.chunks_added})`;
                    uploadMessage.style.color = 'green';
                } else {
                    uploadMessage.textContent = 'Ошибка: ' + data.detail;
                    uploadMessage.style.color = 'red';
                }
            } catch (error) {
                uploadMessage.textContent = 'Ошибка сети: ' + error.message;
                uploadMessage.style.color = 'red';
            }
            fileInput.value = '';
        });
    }
});