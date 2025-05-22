<script>
    import {onMount} from 'svelte';
    import { browser } from '$app/environment';

    let darkMode = false;
    let condensedView = false;
    let scrollY = 0;

    onMount(() => {
        darkMode = localStorage.getItem("theme") === "dark";
        document.body.classList.toggle("dark", darkMode);
        if (browser) {
            const savedY = localStorage.getItem('compareScroll');
            if (savedY) window.scrollTo(0, parseInt(savedY));
        }
    });

    function toggleDarkMode() {
        darkMode = !darkMode;
        localStorage.setItem("theme", darkMode ? "dark" : "light");
        document.body.classList.toggle("dark", darkMode);
    }

    import {fade} from 'svelte/transition';
    import {marked} from 'marked';
    import DOMPurify from 'dompurify';

    let prompt = '';
    let configA = {public_model_name: 'gpt-4'};
    let configB = {public_model_name: 'ollama:llama2'};
    let resultA = null;
    let resultB = null;
    let loading = false;

    function renderMarkdown(html) {
        return DOMPurify.sanitize(marked.parse(html || ''));
    }

    async function runComparison() {
        loading = true;
        const prompts = prompt.split('\n').filter(p => p.trim());
        if (prompts.length === 1) {
            const response = await fetch('/compare', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    prompt,
                    config_a: configA,
                    config_b: configB
                })
            });
            const data = await response.json();
            resultA = data.result_a;
            resultB = data.result_b;
        } else {
            const response = await fetch('/compare/batch', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompts, config_a: configA, config_b: configB})
            });
            const data = await response.json();
            resultA = data;
            resultB = data[0].result_b;
        }
        loading = false;
    }

    function getDiffTable(configA, configB) {
        const keys = new Set([...Object.keys(configA), ...Object.keys(configB)]);
        return Array.from(keys)
            .filter(key => configA[key] !== configB[key])
            .sort()
            .map(key => ({key, a: configA[key], b: configB[key]}));
    }

    function exportResults(format = 'json') {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const name = `${resultA?.model || 'modelA'}_vs_${resultB?.model || 'modelB'}`;
        const blob = new Blob([
            format === 'json'
                ? JSON.stringify({ prompt, configA, configB, resultA, resultB }, null, 2)
                : `# Prompt:\n${prompt}\n\n## ${resultA.model}:\n${resultA.output}\n\n## ${resultB.model}:\n${resultB.output}`
        ], { type: format === 'json' ? 'application/json' : 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `compare_${name}_${timestamp}.${format === 'json' ? 'json' : 'md'}`;
        a.click();
        URL.revokeObjectURL(url);
    }

    function exportResultsCSV() {
      if (!Array.isArray(resultA)) return;
      const header = ['Prompt', 'Model A', 'Output A', 'Latency A', 'Tokens A', 'Model B', 'Output B', 'Latency B', 'Tokens B'];
      const rows = resultA.map((row, i) => [
        row.prompt, row.result_a.model, row.result_a.output, row.result_a.latency_ms, row.result_a.tokens,
        row.result_b.model, row.result_b.output, row.result_b.latency_ms, row.result_b.tokens
      ]);
      const csv = [header, ...rows].map(r => r.map(c => `"${(c || '').toString().replace(/"/g, '""')}"`).join(',')).join('\n');
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'compare_batch_export.csv';
      a.click();
      URL.revokeObjectURL(url);
    }

    function exportBatchMarkdown() {
        if (!Array.isArray(resultA)) return;
        const parts = resultA.map(row => {
            return `## Prompt
${row.prompt}

### ${row.result_a.model}
${row.result_a.output}

### ${row.result_b.model}
${row.result_b.output}`;
        });
        const blob = new Blob([parts.join('\n\n---\n\n')], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'compare_batch_export.md';
        a.click();
        URL.revokeObjectURL(url);
    }
<svelte:window on:scroll={() => {
    if (browser) localStorage.setItem('compareScroll', window.scrollY);
}} />
</script>
<div style="text-align: right; margin-bottom: 0.5rem;">
    <button on:click={toggleDarkMode}>
        {darkMode ? '☀️ Light Mode' : '🌙 Dark Mode'}
    </button>
</div>

<label style="margin-right: 1rem;">
  <input type="checkbox" bind:checked={condensedView} />
  Condensed View
</label>

<h1>🔁 Compare</h1>

<div style="margin-bottom: 1rem;">
    <textarea bind:value={prompt} rows="4" placeholder="Enter one or more prompts, separated by line breaks"></textarea>
    <button on:click={runComparison} disabled={loading} style="margin-top: 0.5rem;">
        {loading ? 'Comparing...' : 'Run Comparison'}
    </button>
</div>

<div class="config-panels">
    <div class="config-card">
        <h3>Config A</h3>
        <label>Model A:
            <select bind:value={configA.public_model_name}>
                <option value="gpt-4">GPT-4</option>
                <option value="gpt-3.5">GPT-3.5</option>
                <option value="ollama:llama2">Ollama: LLaMA 2</option>
                <option value="ollama:mistral">Ollama: Mistral</option>
                <option value="mixtral">Mixtral</option>
            </select>
        </label>
        {#if resultA?.config?.system_prompt}
          <div class="system-prompt-preview">
            <strong>System Prompt:</strong>
            <pre>{resultA.config.system_prompt}</pre>
          </div>
        {/if}
    </div>
    <div class="config-card">
        <h3>Config B</h3>
        <label>Model B:
            <select bind:value={configB.public_model_name}>
                <option value="gpt-4">GPT-4</option>
                <option value="gpt-3.5">GPT-3.5</option>
                <option value="ollama:llama2">Ollama: LLaMA 2</option>
                <option value="ollama:mistral">Ollama: Mistral</option>
                <option value="mixtral">Mixtral</option>
            </select>
        </label>
        {#if resultB?.config?.system_prompt}
          <div class="system-prompt-preview">
            <strong>System Prompt:</strong>
            <pre>{resultB.config.system_prompt}</pre>
          </div>
        {/if}
    </div>
</div>

{#if resultA && resultB && !condensedView}
    <p class="summary-box">
        {resultA.model} was {resultA.latency_ms < resultB.latency_ms ? 'faster' : 'slower'} and
        used {resultA.tokens < resultB.tokens ? 'fewer' : 'more'} tokens than {resultB.model}.
    </p>
{/if}

{#if resultA && resultB && !condensedView}
    <div class="compare-output">
        <div class="result-card" transition:fade>
            <h4>{resultA.model}</h4>
            <div class="metric-bar"><span>Latency</span>
                <div class="bar">
                    <div class="fill" style="width: {resultA.latency_ms / 10}%"></div>
                </div>
            </div>
            <div class="metric-bar"><span>Tokens</span>
                <div class="bar">
                    <div class="fill" style="width: {resultA.tokens / 2}%"></div>
                </div>
            </div>
            {@html `<div class="markdown-output">${renderMarkdown(resultA.output)}</div>`}
            {#if resultA?.config?.system_prompt}
              <div class="system-prompt-preview">
                <strong>System Prompt:</strong>
                <pre>{resultA.config.system_prompt}</pre>
              </div>
            {/if}
        </div>
        <div class="result-card" transition:fade>
            <h4>{resultB.model}</h4>
            <div class="metric-bar"><span>Latency</span>
                <div class="bar">
                    <div class="fill" style="width: {resultB.latency_ms / 10}%"></div>
                </div>
            </div>
            <div class="metric-bar"><span>Tokens</span>
                <div class="bar">
                    <div class="fill" style="width: {resultB.tokens / 2}%"></div>
                </div>
            </div>
            {@html `<div class="markdown-output">${renderMarkdown(resultB.output)}</div>`}
            {#if resultB?.config?.system_prompt}
              <div class="system-prompt-preview">
                <strong>System Prompt:</strong>
                <pre>{resultB.config.system_prompt}</pre>
              </div>
            {/if}
        </div>
    </div>
{/if}

{#if resultA && resultB}
    <div style="margin-top: 2rem;">
        <button on:click={runComparison}>🔁 Retry Comparison</button>
        <button on:click={() => exportResults('json')}>📤 Export JSON</button>
        <button on:click={() => exportResults('md')}>📝 Export Markdown</button>
        {#if Array.isArray(resultA)}
          <button on:click={exportResultsCSV}>📊 Export Batch CSV</button>
          <button on:click={exportBatchMarkdown}>📘 Export Batch Markdown</button>
        {/if}
    </div>
{/if}

{#if resultA && resultB && !condensedView}
    <h2 style="margin-top: 2rem;">🔍 Config Differences</h2>
    <table class="diff-table">
        <thead>
        <tr>
            <th>Parameter</th>
            <th>Config A</th>
            <th>Config B</th>
        </tr>
        </thead>
        <tbody>
        {#each getDiffTable(resultA.config, resultB.config) as row}
            <tr>
                <td>{row.key}</td>
                <td>{row.a}</td>
                <td>{row.b}</td>
            </tr>
        {/each}
        </tbody>
    </table>
{/if}
