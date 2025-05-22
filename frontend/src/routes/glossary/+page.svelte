<script>
    import { glossaryMarkdown } from '$lib/glossary.js';
    import { onMount } from 'svelte';
    import { marked } from 'marked';

    let htmlContent;

    onMount(() => {
        if (htmlContent) {
            htmlContent.innerHTML = marked.parse(glossaryMarkdown);
        }
    });
</script>

<h1>📘 Glossary</h1>

<div class="glossary-table" bind:this={htmlContent}></div>

<style>
  .glossary-table table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1.5rem;
    font-size: 0.95rem;
    table-layout: fixed;
  }

  .glossary-table th,
  .glossary-table td {
    border: 1px solid #ccc;
    padding: 0.75rem;
    text-align: left;
    vertical-align: top;
    word-wrap: break-word;
  }

  .glossary-table th {
    background-color: #f4f6f8;
    font-weight: 600;
    font-size: 1rem;
  }

  .glossary-table tr:nth-child(even) {
    background-color: #f9f9f9;
  }

  .glossary-table tr:hover {
    background-color: #eef3f8;
  }

  .glossary-table {
    overflow-x: auto;
  }

  :global(.glossary-table table) {
      width: 100%;
      border-collapse: collapse;
      margin-top: 1.5rem;
      font-size: 0.95rem;
      table-layout: fixed;
  }

  :global(.glossary-table th),
  :global(.glossary-table td) {
      border: 1px solid #ccc;
      padding: 0.75rem;
      text-align: left;
      vertical-align: top;
      word-wrap: break-word;
  }

  :global(.glossary-table th) {
      background-color: #f4f6f8;
      font-weight: 600;
      font-size: 1rem;
  }

  :global(.glossary-table tr:nth-child(even)) {
      background-color: #f9f9f9;
  }

  :global(.glossary-table tr:hover) {
      background-color: #eef3f8;
  }
</style>