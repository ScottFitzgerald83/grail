<script>
    import '../app.css';
</script>

<nav class="top-nav">
  <a href="/chat">Chat</a>
  <a href="/compare">Compare</a>
  <a href="/glossary">Glossary</a>
  <a href="/roadmap">Roadmap</a>
  <a href="/tuning">Tuning</a>
</nav>

<slot />

<style>
  .top-nav {
    display: flex;
    gap: 1rem;
    padding: 1rem;
    background-color: #0e1117;
    color: white;
  }

  .top-nav a {
    color: white;
    text-decoration: none;
    font-weight: 500;
  }

  .top-nav a:hover {
    text-decoration: underline;
  }
</style>