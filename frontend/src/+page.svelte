<script>
    import { onMount } from 'svelte';
    import { browser } from '$app/environment';
    import { marked } from 'marked';

    let layoutMode = 'side-by-side';
    let prompt = '';
    let configA = { public_model_name: 'gpt-4' };
    let configB = { public_model_name: 'ollama:llama2' };
    let resultA = null;
    let resultB = null;
    let loading = false;

    function renderMarkdown(html) {
        return marked.parse(html || '');
    }

    function runComparison() {
        loading = true;
        // Simulated async load...
        loading = false;
    }

    onMount(() => {
        if (location.hash) {
            try {
                const parsed = JSON.parse(atob(location.hash.slice(1)));
                prompt = parsed.prompt;
                configA = parsed.configA;
                configB = parsed.configB;
                runComparison();
            } catch {}
        }
    });
</script>

<style src="/src/app.css"></style>

<div class="page-container">
  <div class="card-block">
    <label class="field-label">Output Layout</label>
    <select bind:value={layoutMode}>
      <option value="side-by-side">🧩 Side-by-side</option>
      <option value="stacked">📚 Stacked</option>
    </select>
  </div>

  {#if resultA && resultB}
    <div class="card-block {layoutMode === 'stacked' ? 'output-stacked' : 'compare-output'}">
      <div class="output-block">
        <h4>🧠 {resultA.model}</h4>
        <button class="copy-btn" on:click={() => navigator.clipboard.writeText(resultA.output)}>📋 Copy</button>
        {@html renderMarkdown(resultA.output)}
      </div>
      <div class="output-block">
        <h4>🧠 {resultB.model}</h4>
        <button class="copy-btn" on:click={() => navigator.clipboard.writeText(resultB.output)}>📋 Copy</button>
        {@html renderMarkdown(resultB.output)}
      </div>
    </div>
  {/if}
</div>
