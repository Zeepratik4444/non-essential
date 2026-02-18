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
    let currentThreadId = null;

    // --- Core Functions ---

    function updateTimer() {
        const elapsed = (Date.now() - startTime) / 1000;
        timerDisplay.textContent = `${elapsed.toFixed(1)}s`;
    }

    async function executeTask(description) {
        if (!description.trim()) return;

        // UI State: User Message
        addMessage('user', description);
        taskInput.value = '';
        taskInput.style.height = 'auto';

        // UI State: Agent Thinking
        const thinkingMsg = showThinking();
        startTime = Date.now();

        try {
            const response = await fetch('/api/v1/run', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    task_description: description,
                    thread_id: currentThreadId
                })
            });

            const data = await response.json();

            // Remove Thinking Animation
            thinkingMsg.remove();

            if (data.success) {
                currentThreadId = data.thread_id;
                addMessage('agent', data.result);
            } else {
                addMessage('system', `❌ Error: ${data.message}`, 'error');
            }
        } catch (error) {
            thinkingMsg.remove();
            addMessage('system', `❌ Connection failed: ${error.message}`, 'error');
        }
    }

    function showThinking() {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message agent';
        msgDiv.innerHTML = `
            <div class="message-content thinking-bubble">
                <span class="thinking-text">Skills Operator is thinking</span>
                <div class="dot-pulse">
                    <span></span><span></span><span></span>
                </div>
            </div>
        `;
        chatHistory.appendChild(msgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
        return msgDiv;
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

    async function populateSkills() {
        try {
            const response = await fetch('/api/v1/skills');
            const data = await response.json();
            const skills = data.skills || [];

            skillsList.innerHTML = '';
            skills.forEach(skill => {
                const div = document.createElement('div');
                div.className = 'skill-tag';
                // Clean up name for display (e.g. "frontend-development" -> "Frontend Development")
                const displayName = skill.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
                div.textContent = displayName;
                div.onclick = () => {
                    taskInput.value = `Load ${skill} and help me with...`;
                    taskInput.focus();
                };
                skillsList.appendChild(div);
            });
        } catch (error) {
            console.error('Failed to fetch skills:', error);
            skillsList.innerHTML = '<p style="font-size: 0.75rem; color: var(--error-red); padding: 12px;">Failed to load skills.</p>';
        }
    }

    // --- Skill Creation Modal ---
    const addSkillBtn = document.getElementById('add-skill-btn');
    const modal = document.getElementById('skill-modal');
    const closeBtn = document.getElementById('close-modal');
    const cancelBtn = document.getElementById('cancel-skill');
    const skillForm = document.getElementById('skill-form');

    addSkillBtn.onclick = (e) => {
        e.preventDefault();
        modal.classList.remove('hidden');
    };

    const closeModal = () => modal.classList.add('hidden');
    closeBtn.onclick = closeModal;
    cancelBtn.onclick = closeModal;

    skillForm.onsubmit = async (e) => {
        e.preventDefault();
        const name = document.getElementById('new-skill-name').value;
        const content = document.getElementById('new-skill-content').value;

        try {
            const response = await fetch('/api/v1/skills', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, content })
            });

            const data = await response.json();
            if (data.success) {
                addMessage('system', `✅ ${data.message}`);
                closeModal();
                skillForm.reset();
                populateSkills(); // Refresh sidebar
            } else {
                alert(`Error: ${data.message || 'Failed to create skill'}`);
            }
        } catch (error) {
            alert(`Connection failed: ${error.message}`);
        }
    };

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
        currentThreadId = null;
        addMessage('system', 'History cleared.');
    };

    // Quick prompts
    document.querySelectorAll('.btn-quick').forEach(btn => {
        btn.onclick = () => executeTask(btn.dataset.prompt);
    });

    populateSkills();
});
