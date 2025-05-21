<script>
    import {onMount} from 'svelte';

    let darkMode = false;

    onMount(() => {
        darkMode = localStorage.getItem("theme") === "dark";
        document.body.classList.toggle("dark", darkMode);
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
            resultA = data[0].result_a;
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
        const blob = new Blob([
            format === 'json'
                ? JSON.stringify({prompt, configA, configB, resultA, resultB}, null, 2)
                : `### Prompt:\n${prompt}\n\n### Config A (${resultA.model}):\n${resultA.output}\n\n### Config B (${resultB.model}):\n${resultB.output}`
        ], {type: format === 'json' ? 'application/json' : 'text/markdown'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `compare_result.${format}`;
        a.click();
        URL.revokeObjectURL(url);
    }
</script>
<div style="text-align: right; margin-bottom: 0.5rem;">
    <button on:click={toggleDarkMode}>
        {darkMode ? '☀️ Light Mode' : '🌙 Dark Mode'}
    </button>
</div>
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
    </div>
</div>

{#if resultA && resultB}
    <p class="summary-box">
        {resultA.model} was {resultA.latency_ms < resultB.latency_ms ? 'faster' : 'slower'} and
        used {resultA.tokens < resultB.tokens ? 'fewer' : 'more'} tokens than {resultB.model}.
    </p>
{/if}

{#if resultA && resultB}
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
        </div>
    </div>
{/if}

{#if resultA && resultB}
    <div style="margin-top: 2rem;">
        <button on:click={runComparison}>🔁 Retry Comparison</button>
        <button on:click={() => exportResults('json')}>📤 Export JSON</button>
        <button on:click={() => exportResults('md')}>📝 Export Markdown</button>
    </div>
{/if}

{#if resultA && resultB}
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
