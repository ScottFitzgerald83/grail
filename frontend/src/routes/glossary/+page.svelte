<script>
    import { glossaryMarkdown } from '$lib/glossary.js';
    import { onMount } from 'svelte';
    import { marked } from 'marked';

    let htmlContent;
    let search = '';
    let filteredMarkdown = '';

    onMount(() => {
        filteredMarkdown = glossaryMarkdown;
        if (htmlContent) {
            htmlContent.innerHTML = marked.parse(filteredMarkdown);
        }
    });

    $: {
        const lines = glossaryMarkdown.split('\n');
        const header = lines.slice(0, 2); // header + separator
        const body = lines.slice(2);

        const filteredRows = body.filter(line => {
            const parts = line.split('|').map(s => s.trim());
            return parts.length > 1 && (parts[0] + parts[1]).toLowerCase().includes(search.toLowerCase());
        });

        const filtered = [...header, ...filteredRows].join('\n');

        if (htmlContent) {
            htmlContent.innerHTML = marked.parse(filtered);
        }
    }
</script>

<style src="/src/app.css"></style>
<h1>📘 Glossary</h1>

<input
    type="text"
    bind:value={search}
    placeholder="🔍 Search terms..."
    class="search-bar"
/>

<div class="glossary-table" bind:this={htmlContent}></div>
