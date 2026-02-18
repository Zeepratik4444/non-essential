document.addEventListener('DOMContentLoaded', () => {
    const taskInput = document.getElementById('task-input');
    const sendBtn = document.getElementById('send-btn');
    const chatHistory = document.getElementById('chat-history');
    const loader = document.getElementById('loading-overlay');
    const timerDisplay = document.getElementById('loader-timer');
    const skillsList = document.getElementById('skills-list');
    const clearBtn = document.getElementById('clear-console');

    let startTime = 0;
    let timerInterval = null;

    // --- Core Functions ---

    function updateTimer() {
        const elapsed = (Date.now() - startTime) / 1000;
        timerDisplay.textContent = `${elapsed.toFixed(1)}s`;
    }

    async function executeTask(description) {
        if (!description.trim()) return;

        // UI State: Loading
        addMessage('user', description);
        taskInput.value = '';
        taskInput.style.height = 'auto';

        loader.classList.remove('hidden');
        startTime = Date.now();
        timerInterval = setInterval(updateTimer, 100);

        try {
            const response = await fetch('/api/v1/run', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task_description: description })
            });

            const data = await response.json();

            if (data.success) {
                addMessage('agent', data.result);
            } else {
                addMessage('system', `❌ Error: ${data.message}`, 'error');
            }
        } catch (error) {
            addMessage('system', `❌ Connection failed: ${error.message}`, 'error');
        } finally {
            clearInterval(timerInterval);
            loader.classList.add('hidden');
        }
    }

    function addMessage(role, content, type = '') {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role} ${type}`;

        const inner = document.createElement('div');
        inner.className = `message-content markdown-body`;

        if (role === 'agent') {
            inner.innerHTML = marked.parse(content);
        } else {
            inner.textContent = content;
        }

        msgDiv.appendChild(inner);
        chatHistory.appendChild(msgDiv);

        // Scroll to bottom
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    // --- Dynamic Skills discovery (Mock implementation for now, could be an endpoint) ---
    function populateSkills() {
        const skills = ['Financial Analysis', 'Legal Review', 'HR Recruitment', 'Customer Support', 'Frontend Dev', 'API Dev', 'Database Design'];
        skillsList.innerHTML = '';
        skills.forEach(skill => {
            const div = document.createElement('div');
            div.className = 'skill-tag';
            div.textContent = skill;
            div.onclick = () => {
                taskInput.value = `Load ${skill} and help me with...`;
                taskInput.focus();
            };
            skillsList.appendChild(div);
        });
    }

    // --- Event Listeners ---

    sendBtn.onclick = () => executeTask(taskInput.value);

    taskInput.onkeydown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            executeTask(taskInput.value);
        }
    };

    // Auto-resize textarea
    taskInput.oninput = () => {
        taskInput.style.height = 'auto';
        taskInput.style.height = (taskInput.scrollHeight) + 'px';
    };

    clearBtn.onclick = () => {
        chatHistory.innerHTML = '';
        addMessage('system', 'History cleared.');
    };

    // Quick prompts
    document.querySelectorAll('.btn-quick').forEach(btn => {
        btn.onclick = () => executeTask(btn.dataset.prompt);
    });

    populateSkills();
});
