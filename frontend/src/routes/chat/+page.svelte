<script>
    import { afterUpdate, onMount } from 'svelte';

    let messages = [];
    let input = '';
    let sending = false;

    let chatWindow;
    let showScrollButton = false;

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
    <div class="messages" bind:this={chatWindow}>
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

    {#if showScrollButton}
        <button class="scroll-button" on:click={() => scrollToBottom(true)}>
            ⬇️ Jump to Bottom
        </button>
    {/if}

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
</style>