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
        let currentTerm = '';
        let currentBlock = '';
        let filteredBlocks = [];

        for (const line of lines) {
            if (line.startsWith('### ')) {
                if (currentTerm && currentBlock) {
                    if (currentTerm.toLowerCase().includes(search.toLowerCase())) {
                        filteredBlocks.push(currentBlock.trim());
                    }
                }
                currentTerm = line;
                currentBlock = line + '\n';
            } else {
                currentBlock += line + '\n';
            }
        }

        if (currentTerm && currentBlock) {
            if (currentTerm.toLowerCase().includes(search.toLowerCase())) {
                filteredBlocks.push(currentBlock.trim());
            }
        }

        filteredMarkdown = search.trim() ? filteredBlocks.join('\n\n') : glossaryMarkdown;
        if (htmlContent) {
            htmlContent.innerHTML = marked.parse(filteredMarkdown);
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
