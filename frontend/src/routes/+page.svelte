<script>
    import { goto } from '$app/navigation';
</script>

<h1>Welcome to GRAIL</h1>
<p>This is your AI research assistant. Choose a section below:</p>

<nav>
    <button on:click={() => goto('/chat')}>💬 Chat</button>
    <button on:click={() => goto('/compare')}>🔁 Compare</button>
    <button on:click={() => goto('/glossary')}>📘 Glossary</button>
    <button on:click={() => goto('/roadmap')}>🗺️ Roadmap</button>
    <button on:click={() => goto('/tuning')}>🎛️ Tuning</button>
</nav>