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