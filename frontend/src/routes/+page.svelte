<script>
    import { onMount, afterUpdate } from 'svelte';
    let messages = [];
    let input = '';
    let chatWindow;

    async function sendMessage() {
        if (!input.trim()) return;
        const userMsg = { role: 'user', content: input };
        messages = [...messages, userMsg];


        const response = await fetch('/infer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: input })
        });

        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Response data:', data);
        const replyMsg = { role: 'assistant', content: data.output };
        messages = [...messages, replyMsg];
        input = '';
        setTimeout(() => chatWindow.scrollTop = chatWindow.scrollHeight, 0);
    }

    onMount(() => {
        setTimeout(() => chatWindow.scrollTop = chatWindow.scrollHeight, 0);
    });

    afterUpdate(() => {
        if (chatWindow) {
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
    });
</script>

<style>
    .chat-container {
        display: flex;
        flex-direction: column;
        height: 100vh;
    }
    .messages {
        flex: 1;
        overflow-y: auto;
        padding: 1rem;
    }
    .message {
        max-width: 75%;
        margin-bottom: 1rem;
        padding: 0.75rem 1rem;
        border-radius: 1rem;
        word-wrap: break-word;
    }
    .user {
        align-self: flex-end;
        background-color: #0d6efd;
        color: white;
    }
    .assistant {
        align-self: flex-start;
        background-color: #e9ecef;
        color: #212529;
    }
    .input-bar {
        display: flex;
        padding: 1rem;
        border-top: 1px solid #ccc;
        background-color: #f9f9f9;
    }
    .input-bar input {
        flex: 1;
        padding: 0.75rem;
        margin-right: 0.5rem;
    }
    .input-bar button {
        padding: 0.75rem 1rem;
    }
</style>

<div class="chat-container">
    <div class="messages" bind:this={chatWindow}>
        {#each messages as message}
            <div class="message {message.role}">
                {message.content}
            </div>
        {/each}
    </div>
    <form on:submit|preventDefault={sendMessage} class="input-bar">
        <input
                type="text"
                bind:value={input}
                placeholder="Type your message..."
        />
        <button type="submit">📤</button>
    </form>
</div>