<script>
    let messages = [];
    let input = '';

    function formatTimestamp(date) {
        return date.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});
    }

    async function sendMessage() {
        if (!input.trim()) return;

        const userMessage = {
            id: Date.now() + Math.random(),
            role: 'user',
            content: input,
            timestamp: formatTimestamp(new Date()),
        };

        messages = [...messages, userMessage];

        const assistantMessage = {
            id: Date.now() + Math.random(),
            role: 'assistant',
            content: '',
            timestamp: formatTimestamp(new Date()),
            streaming: true,
        };

        messages = [...messages, assistantMessage];

        const config = JSON.parse(localStorage.getItem('grailConfig') || '{}');

        const res = await fetch('/infer', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({prompt: input, ...config})
        });
        const data = await res.json();

        // Simulate streaming character-by-character
        const fullText = data.output;
        let currentText = '';
        for (let i = 0; i < fullText.length; i++) {
            currentText += fullText[i];
            messages = messages.map(m =>
                m.id === assistantMessage.id ? {...m, content: currentText} : m
            );
            await new Promise(r => setTimeout(r, 30));
        }

        // Mark streaming as finished
        messages = messages.map(m =>
            m.id === assistantMessage.id ? {...m, streaming: false} : m
        );

        input = '';
    }
</script>

<div class="chat-container">
    <div class="messages">
        {#each messages as m (m.id)}
            <div class="message-row {m.role}">
                <span class="avatar">{m.role === 'user' ? '🙋' : '🧠'}</span>
                <div class="message-bubble">
                    <div class="content">{@html m.content}</div>
                    <div class="timestamp">{m.timestamp}</div>
                </div>
            </div>
        {/each}
    </div>

    <form on:submit|preventDefault={sendMessage}>
        <input type="text" bind:value={input}/>
        <button type="submit">Send</button>
    </form>
</div>

<style>
    .chat-container {
        display: flex;
        flex-direction: column;
        height: 100vh;
        background-color: #fdfdfd;
    }

    .messages {
        flex: 1;
        overflow-y: auto;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .message-row {
        display: flex;
        gap: 0.5rem;
        align-items: flex-start;
    }

    .message-row.user {
        flex-direction: row-reverse;
    }

    .avatar {
        font-size: 1.5rem;
        margin-top: 0.2rem;
    }

    .message-bubble {
        max-width: 75%;
        padding: 0.75rem 1rem;
        border-radius: 1rem;
        word-wrap: break-word;
        background-color: #e9ecef;
        color: #212529;
        position: relative;
    }

    .message-row.user .message-bubble {
        background-color: #0d6efd;
        color: white;
    }

    .timestamp {
        font-size: 0.7rem;
        color: #999;
        margin-top: 0.25rem;
    }

    form {
        display: flex;
        gap: 0.5rem;
        padding: 1rem;
        border-top: 1px solid #ccc;
        background-color: #f9f9f9;
    }

    input[type="text"] {
        flex: 1;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: 1px solid #ccc;
    }

    button {
        padding: 0.75rem 1rem;
        background-color: #0d6efd;
        color: white;
        border: none;
        border-radius: 0.5rem;
        cursor: pointer;
    }

    button:hover {
        background-color: #0b5ed7;
    }
</style>