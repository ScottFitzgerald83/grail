<script>
    import { afterUpdate, onMount } from 'svelte';
    import { marked } from 'marked';
    import { browser } from '$app/environment';

    let messages = [];
    let input = '';
    let sending = false;

    // Persona banner state
    let activePersona = '';
    let systemPrompt = '';

    let recognition, recognizing = false;
    let supportsSpeech = typeof window !== 'undefined' && ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window);

    if (supportsSpeech && typeof window !== 'undefined') {
        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SR();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.onresult = (e) => {
            input += e.results[0][0].transcript + ' ';
        };
    }

    function startVoice() {
        if (recognition && !recognizing) {
            recognizing = true;
            recognition.start();
        }
    }

    function formatTimestampForDisplay(ts) {
        const date = new Date(ts);
        if (isNaN(date)) return '';
        const minutes = Math.floor((Date.now() - date) / 60000);
        return minutes < 1 ? 'just now' : `${minutes}m ago`;
    }

    onMount(() => {
        const config = JSON.parse(localStorage.getItem("grailConfig") || "{}");
        activePersona = config.persona || '';
        systemPrompt = config.system_prompt || '';

        const savedY = localStorage.getItem('chatScroll');
        if (savedY && chatWindow) chatWindow.scrollTop = parseInt(savedY);

        if (!localStorage.getItem("theme")) {
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            localStorage.setItem("theme", prefersDark ? "dark" : "light");
            document.body.classList.toggle("dark", prefersDark);
        }
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
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const url = `/memory/${model}?format=${format}`;
        const a = document.createElement('a');
        a.href = url;
        a.download = `chat_${model}_${timestamp}.${format === 'json' ? 'json' : 'txt'}`;
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
    <div class="messages" bind:this={chatWindow} on:scroll={() => {
        localStorage.setItem('chatScroll', chatWindow.scrollTop);
    }}>
        {#each messages as m (m.id)}
            <div class="message-row {m.role}">
                <span class="avatar">{m.role === 'user' ? '🙋' : '🧠'}</span>
                {#if m.role === 'user' && editingId !== m.id}
                    <div
                        class="message-bubble"
                        on:contextmenu|preventDefault={() => {
                            const confirmed = confirm('Edit this message? Click OK to edit, Cancel to delete.');
                            if (confirmed) startEdit(m);
                            else deleteMessage(m.id);
                        }}
                        title="{m.role.toUpperCase()} • {m.timestamp}"
                    >
                        <div class="content">
                            {@html marked.parse(m.content || '')}
                        </div>
                        <div class="timestamp" title={m.timestamp}>
                            {formatTimestampForDisplay(m.timestamp)}
                        </div>

                    </div>
                {:else}
                    <div class="message-bubble" title="{m.role.toUpperCase()} • {m.timestamp}">
                        <div class="content">
                            {#if editingId === m.id}
                                <textarea bind:value={editedInput} rows="2" style="width: 100%; font-size: 0.9rem;"></textarea>
                                <div style="margin-top: 0.25rem;">
                                    <button on:click={() => applyEdit(m.id)} style="margin-right: 0.5rem;">Save</button>
                                    <button on:click={cancelEdit}>Cancel</button>
                                </div>
                            {:else}
                                {@html marked.parse(m.content || '')}
                            {/if}
                        </div>
                        <div class="timestamp" title={m.timestamp}>
                            {formatTimestampForDisplay(m.timestamp)}
                        </div>

                    </div>
                {/if}
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
        {#if supportsSpeech}
          <button on:click={startVoice} title="Voice Input 🎙️">🎙️</button>
        {/if}
    </form>
</div>
