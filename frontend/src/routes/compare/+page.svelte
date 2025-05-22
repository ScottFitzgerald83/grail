<script>
  import { roadmapMarkdown } from '$lib/roadmap.js';
  import { onMount } from 'svelte';
  import { marked } from 'marked';

  let htmlContent;

  onMount(() => {
    if (htmlContent) {
      htmlContent.innerHTML = marked.parse(roadmapMarkdown);
    }
  });
</script>

<style src="/src/app.css"></style>

<h1>🗺️ Roadmap</h1>

<div class="roadmap-table" bind:this={htmlContent}></div>