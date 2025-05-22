<script>
  import { onMount } from 'svelte';

  let darkMode = false;

  onMount(() => {
    darkMode = localStorage.getItem('theme') === 'dark';
    document.body.classList.toggle('dark', darkMode);
  });

  function toggleDarkMode() {
    darkMode = !darkMode;
    localStorage.setItem('theme', darkMode ? 'dark' : 'light');
    document.body.classList.toggle('dark', darkMode);
  }
</script>
<nav class="top-nav">
  <a href="/chat">Chat</a>
  <a href="/compare">Compare</a>
  <a href="/tuning">Tuning</a>
  <a href="/glossary">Glossary</a>
  <a href="/roadmap">Roadmap</a>
  <a href="/training">Training</a>
  <button on:click={toggleDarkMode} class="theme-toggle">
    {darkMode ? '☀️' : '🌙'}
  </button>
</nav>
<slot />
