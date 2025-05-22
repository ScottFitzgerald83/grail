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

    function startVoice() {
        if (!supportsSpeech || !recognition) return;
        if (recognizing) {
            recognition.stop();
            recognizing = false;
        } else {
            recognition.start();
            recognizing = true;
        }
    }

    if (browser && supportsSpeech) {
        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SR();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.onresult = (e) => {
            input += e.results[0][0].transcript + ' ';
            recognizing = false;
        };
        recognition.onend = () => {
            recognizing = false;
        };
    }

    let sessionId = browser ? localStorage.getItem('grailSessionId') : null;
    if (!sessionId) sessionId = Date.now().toString();
    let historySessions = [];

    let isOnline = navigator.onLine;
    let offlineQueue = [];

    if (browser) {
      window.addEventListener('online', () => {
        isOnline = true;
        processOfflineQueue();
      });
      window.addEventListener('offline', () => {
        isOnline = false;
      });
    }

    async function processOfflineQueue() {
      for (const queued of offlineQueue) {
        input = queued;
        await sendMessage();
      }
      offlineQueue = [];
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

        const stored = localStorage.getItem('grailHistory');
        if (stored) {
            historySessions = JSON.parse(stored);
        }

        const savedSession = localStorage.getItem(`session_${sessionId}`);
        if (savedSession) {
            messages = JSON.parse(savedSession);
        }
    });

    $: {
        localStorage.setItem(`session_${sessionId}`, JSON.stringify(messages));
    }

    function newChat() {
        if (confirm("Start a new chat?")) {
            sessionId = Date.now().toString();
            messages = [];
            localStorage.setItem('grailSessionId', sessionId);
        }
    }

    function loadChat(id) {
        const saved = localStorage.getItem(`session_${id}`);
        if (saved) {
            messages = JSON.parse(saved);
            sessionId = id;
            localStorage.setItem('grailSessionId', sessionId);
        }
    }

    let chatWindow;
    let showScrollButton = false;

    // Message editing/deletion/export state
    let editingId = null;
    let editedInput = '';

    let toastMessage = '';
    let previousMessages = [];

    // Context menu state
    let showContextMenu = false;
    let contextTarget = null;
    let contextPosition = { x: 0, y: 0 };

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
        closeContextMenu();
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
            previousMessages = [...messages];
            messages = messages.map(m =>
                m.id === id
                    ? { ...m, content: editedInput }
                    : m
            );
            cancelEdit();
            toastMessage = 'Edit successful. Undo?';
            setTimeout(() => toastMessage = '', 3000);
        }
    }

    async function deleteMessage(id) {
        previousMessages = [...messages];
        const config = JSON.parse(localStorage.getItem("grailConfig") || "{}");
        const res = await fetch(`/memory/${config.public_model_name || 'local'}/${id}`, {
            method: 'DELETE'
        });
        const result = await res.json();
        if (result.status === 'deleted') {
            messages = messages.filter(m => m.id !== id);
            toastMessage = 'Delete successful. Undo?';
            setTimeout(() => toastMessage = '', 3000);
        }
        closeContextMenu();
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

    function formatTimestampForDisplay(ts) {
        const date = new Date(ts);
        if (isNaN(date)) return '';
        const minutes = Math.floor((Date.now() - date) / 60000);
        return minutes < 1 ? 'just now' : `${minutes}m ago`;
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

        if (!navigator.onLine) {
          offlineQueue.push(input);
          input = '';
          alert('You are offline. Message saved and will send when back online.');
          return;
        }

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
        // Patch 1: Warn if OpenAI key missing before /infer
        if (config.use_public_model === 'true' && !localStorage.getItem('grailOpenAIKey')) {
            alert('⚠️ OpenAI API key is missing. Please enter it in the Tuning tab.');
            sending = false;
            return;
        }
        const payload = { prompt: input, message_id: assistantMessage.id, ...config };
        payload.openai_api_key = localStorage.getItem('grailOpenAIKey');

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
                // Patch 3: Token/cost display for streamed output
                let tokenEstimate = Math.ceil(data.output.length * 1.25);
                console.log(`[GRAIL] Streamed estimate: ~${tokenEstimate} tokens`);
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

    function retryMessage(failedId) {
        const failed = messages.find(m => m.id === failedId && m.role === 'assistant');
        const previous = messages.findLast(m => m.timestamp && m.timestamp < failed.timestamp && m.role === 'user');
        if (!previous) return;
        input = previous.content;
        sendMessage();
    }

    function openContextMenu(event, message) {
      event.preventDefault();
      contextTarget = message;
      showContextMenu = true;
      contextPosition = { x: event.clientX, y: event.clientY };
    }

    function closeContextMenu() {
      showContextMenu = false;
    }

    function handleUndo() {
      messages = [...previousMessages];
      toastMessage = 'Undo successful';
      setTimeout(() => toastMessage = '', 3000);
    }
</script>
<style src="/src/app.css"></style>
<div class="chat-container">
    {#if activePersona !== 'none' || systemPrompt}
      <div class="persona-banner">
        <strong>Active System Prompt:</strong>
        <div class="prompt-content system-box">
          {systemPrompt || personaDescription(activePersona)}
        </div>
      </div>
    {/if}

    {#if messages.length === 0}
      <div class="empty-state">
        <h2>Welcome to GRAIL Chat</h2>
        <p>Ask a question, explore ideas, or test your prompt configurations.</p>
      </div>
    {/if}

    {#if browser}
      {#await Promise.resolve(JSON.parse(localStorage.getItem("grailConfig") || "{}")) then config}
        {#if config?.public_model_name}
          <div class="model-badge">
            Using: <strong>{config.public_model_name}</strong>
          </div>
        {/if}
      {/await}
    {/if}

    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0 1rem;">
        <div>
            {#if browser}
              <select on:change={(e) => loadChat(e.target.value)}>
                  <option value="">Load previous chat...</option>
                  {#each Object.keys(localStorage)
                    .filter(k => k.startsWith('session_'))
                    .sort()
                    .reverse() as key}
                    <option value={key}>{new Date(+key.slice(8)).toLocaleString()}</option>
                  {/each}
              </select>
            {/if}
        </div>
        <div>
            <button class="mini" on:click={newChat}>🆕 New Chat</button>
        </div>
    </div>

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
                        on:contextmenu={(e) => openContextMenu(e, m)}
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
                        {#if m.role === 'assistant'}
                            <div class="token-estimate">≈ {Math.ceil((m.content || '').split(' ').length * 1.25)} tokens</div>
                            {#if m.content.startsWith("⚠️")}
                                <button class="mini" on:click={() => retryMessage(m.id)}>🔁 Retry</button>
                            {/if}
                        {/if}
                    </div>
                {/if}
            </div>
        {/each}

        {#if messages.length && messages[messages.length - 1].streaming}
            <div class="message-row assistant">
                <span class="avatar">🧠</span>
                <div class="message-bubble">
                    <div class="content typing-indicator">
                        <span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="blinking-cursor">▋</span>
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

    {#if showContextMenu}
      <div class="context-menu" style="top: {contextPosition.y}px; left: {contextPosition.x}px;">
        <button on:click={() => { startEdit(contextTarget); closeContextMenu(); }}>✏️ Edit</button>
        <button on:click={() => { deleteMessage(contextTarget.id); closeContextMenu(); }}>🗑️ Delete</button>
        <button on:click={closeContextMenu}>Cancel</button>
      </div>
    {/if}

    {#if toastMessage}
      <div class="toast" on:click={handleUndo}>{toastMessage}</div>
    {/if}

    {#if input}
      <div class="token-preview">
        Estimated input tokens: ~{Math.ceil(input.trim().split(/\s+/).length * 1.25)}
      </div>
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
                } else if (e.key === 'Escape') {
                    cancelEdit();
                } else if (e.key === 'ArrowUp' && !input && !editingId) {
                    const last = [...messages].reverse().find(m => m.role === 'user');
                    if (last) startEdit(last);
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
