<script>
    import { afterUpdate, onMount } from 'svelte';

    let messages = [];
    let input = '';
    let sending = false;

    // Persona banner state
    let activePersona = '';
    let systemPrompt = '';

    onMount(() => {
        const config = JSON.parse(localStorage.getItem("grailConfig") || "{}");
        activePersona = config.persona || '';
        systemPrompt = config.system_prompt || '';
    });

    let chatWindow;
    let showScrollButton = false;

    // Message editing/deletion/export state
    let editingId = null;
    let editedInput = '';

    function personaDescription(key) {
        const descriptions = {
            friendly: 'You are a helpful, friendly assistant who explains things clearly and kindly.',
            creative: 'You are a poetic and imaginative assistant who speaks with flair and metaphor.',
            concise: 'You are a brief, precise assistant who avoids unnecessary elaboration.'
        };
        return descriptions[key] || '(no persona selected)';
    }

    function startEdit(message) {
        editingId = message.id;
        editedInput = message.content;
    }

    function cancelEdit() {
        editingId = null;
        editedInput = '';
    }

    async function applyEdit(id) {
        const updatedMessage = messages.find(m => m.id === id);
        if (!updatedMessage) return;
        const config = JSON.parse(localStorage.getItem("grailConfig") || "{}");
        const payload = {
            message_id: updatedMessage.id,
            new_prompt: editedInput,
            config
        };

        const res = await fetch(`/memory/${config.public_model_name || 'local'}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await res.json();
        if (result.status === 'updated') {
            messages = messages.map(m =>
                m.id === id
                    ? { ...m, content: editedInput }
                    : m
            );
            cancelEdit();
        }
    }

    async function deleteMessage(id) {
        const config = JSON.parse(localStorage.getItem("grailConfig") || "{}");
        const res = await fetch(`/memory/${config.public_model_name || 'local'}/${id}`, {
            method: 'DELETE'
        });
        const result = await res.json();
        if (result.status === 'deleted') {
            messages = messages.filter(m => m.id !== id);
        }
    }

    function exportChat(format = 'json') {
        const config = JSON.parse(localStorage.getItem("grailConfig") || "{}");
        const model = config.public_model_name || 'local';
        const url = `/memory/${model}?format=${format}`;
        const a = document.createElement('a');
        a.href = url;
        a.download = `chat_${model}.${format === 'json' ? 'json' : 'txt'}`;
        a.click();
    }

    function formatTimestamp(date) {
        return date.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});
    }

    function scrollToBottom(force = false) {
        if (!chatWindow) return;
        const nearBottom = chatWindow.scrollHeight - chatWindow.scrollTop - chatWindow.clientHeight < 120;
        if (force || nearBottom) {
            chatWindow.scrollTop = chatWindow.scrollHeight;
            showScrollButton = false;
        } else {
            showScrollButton = true;
        }
    }

    afterUpdate(() => {
        scrollToBottom();
    });

    async function sendMessage() {
        if (!input.trim() || sending) return;
        sending = true;

        const userMessage = {
            id: Date.now() + Math.random(),
            role: 'user',
            content: input,
            timestamp: formatTimestamp(new Date())
        };

        messages = [...messages, userMessage];

        const assistantMessage = {
            id: Date.now() + Math.random(),
            role: 'assistant',
            content: '',
            timestamp: formatTimestamp(new Date()),
            streaming: true
        };

        messages = [...messages, assistantMessage];

        const config = JSON.parse(localStorage.getItem("grailConfig") || "{}");
        const payload = { prompt: input, message_id: assistantMessage.id, ...config };

        try {
            const response = await fetch("/infer", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (!data.output) {
                messages = messages.map(m =>
                    m.id === assistantMessage.id ? { ...m, content: "⚠️ Assistant didn’t respond.", streaming: false } : m
                );
            } else {
                let currentText = '';
                for (let i = 0; i < data.output.length; i++) {
                    currentText += data.output[i];
                    messages = messages.map(m =>
                        m.id === assistantMessage.id ? { ...m, content: currentText } : m
                    );
                    await new Promise(r => setTimeout(r, 30));
                }

                messages = messages.map(m =>
                    m.id === assistantMessage.id ? { ...m, streaming: false } : m
                );
            }
        } catch (err) {
            messages = messages.map(m =>
                m.id === assistantMessage.id ? { ...m, content: "⚠️ Error contacting backend.", streaming: false } : m
            );
        }

        input = '';
        sending = false;
    }
</script>

<div class="chat-container">
    {#if activePersona !== 'none' || systemPrompt}
      <div class="persona-banner">
        <strong>Active System Prompt:</strong>
        <div class="prompt-content">
          {systemPrompt || personaDescription(activePersona)}
        </div>
      </div>
    {/if}
    <div style="text-align: right; padding: 0 1rem 0.5rem;">
        <button class="mini" on:click={() => exportChat('json')}>Export JSON</button>
        <button class="mini" on:click={() => exportChat('txt')}>Export Text</button>
    </div>
    <div class="messages" bind:this={chatWindow}>
        {#each messages as m (m.id)}
            <div class="message-row {m.role}">
                <span class="avatar">{m.role === 'user' ? '🙋' : '🧠'}</span>
                <div class="message-bubble" title="{m.role.toUpperCase()} • {m.timestamp}">
                    <div class="content">
                        {#if editingId === m.id}
                            <textarea bind:value={editedInput} rows="2" style="width: 100%; font-size: 0.9rem;"></textarea>
                            <div style="margin-top: 0.25rem;">
                                <button on:click={() => applyEdit(m.id)} style="margin-right: 0.5rem;">Save</button>
                                <button on:click={cancelEdit}>Cancel</button>
                            </div>
                        {:else}
                            {@html m.content}
                        {/if}
                    </div>
                    <div class="timestamp">{m.timestamp}</div>
                    {#if m.role === 'user' && editingId !== m.id}
                        <div class="controls">
                            <button class="mini" title="Edit" on:click={() => startEdit(m)}>📝</button>
                            <button class="mini" title="Delete" on:click={() => deleteMessage(m.id)}>❌</button>
                        </div>
                    {/if}
                </div>
            </div>
        {/each}

        {#if messages.length && messages[messages.length - 1].streaming}
            <div class="message-row assistant">
                <span class="avatar">🧠</span>
                <div class="message-bubble">
                    <div class="content typing-indicator">
                        <span class="dot"></span><span class="dot"></span><span class="dot"></span>
                    </div>
                </div>
            </div>
        {/if}
    </div>

    {#if showScrollButton}
        <button class="scroll-button" on:click={() => scrollToBottom(true)}>
            ⬇️ Jump to Bottom
        </button>
    {/if}

    <form on:submit|preventDefault={sendMessage}>
        <textarea
            bind:value={input}
            rows="1"
            placeholder="Type a message..."
            on:keydown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            }}
            class="chat-input-textarea"
        ></textarea>
        <button type="submit">Send</button>
    </form>
</div>

<style>
    .chat-container {
        display: flex;
        flex-direction: column;
        height: 100vh;
        background-color: #fdfdfd;
        position: relative;
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

    textarea.chat-input-textarea {
        flex: 1;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: 1px solid #ccc;
        font-size: 1rem;
        resize: none;
        line-height: 1.4;
    }

    textarea.chat-input-textarea:focus {
        outline: none;
        border-color: #0d6efd;
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

    .scroll-button {
        position: absolute;
        bottom: 5rem;
        right: 1rem;
        background: #0d6efd;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        font-size: 0.85rem;
        cursor: pointer;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }

    .scroll-button:hover {
        background: #0b5ed7;
    }

    .typing-indicator {
        display: flex;
        gap: 4px;
        height: 1rem;
        align-items: center;
        justify-content: flex-start;
    }

    .typing-indicator .dot {
        width: 6px;
        height: 6px;
        background-color: #666;
        border-radius: 50%;
        animation: blink 1.4s infinite ease-in-out both;
    }

    .typing-indicator .dot:nth-child(2) {
        animation-delay: 0.2s;
    }
    .typing-indicator .dot:nth-child(3) {
        animation-delay: 0.4s;
    }

    @keyframes blink {
        0%, 80%, 100% {
            opacity: 0;
        }
        40% {
            opacity: 1;
        }
    }
    .controls {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.25rem;
        font-size: 0.8rem;
    }

    button.mini {
        background: #eee;
        border: none;
        border-radius: 4px;
        padding: 0.25rem 0.5rem;
        font-size: 0.8rem;
        cursor: pointer;
    }

    button.mini:hover {
        background: #ddd;
    }
    .persona-banner {
        background: #f5f8ff;
        padding: 0.75rem 1rem;
        font-size: 0.85rem;
        color: #2a3b4c;
        border-bottom: 1px solid #d0dae7;
    }

    .persona-banner .prompt-content {
        margin-top: 0.25rem;
        font-style: italic;
        font-size: 0.82rem;
    }
</style>