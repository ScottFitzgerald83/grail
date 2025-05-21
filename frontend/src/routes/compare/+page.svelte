<script>
    import {fade} from 'svelte/transition';

    let prompt = '';
    let configA = {public_model_name: 'gpt-4'};
    let configB = {public_model_name: 'ollama:llama2'};
    let resultA = null;
    let resultB = null;
    let loading = false;

    async function runComparison() {
        loading = true;
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
        loading = false;
    }

    function getDiffTable(configA, configB) {
        const keys = new Set([...Object.keys(configA), ...Object.keys(configB)]);
        return Array.from(keys)
            .filter(key => configA[key] !== configB[key])
            .sort()
            .map(key => ({key, a: configA[key], b: configB[key]}));
    }
</script>

<h1>🔁 Compare</h1>

<div style="margin-bottom: 1rem;">
    <textarea bind:value={prompt} rows="3" placeholder="Enter a prompt to test"></textarea>
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
            <pre>{resultA.output}</pre>
            <details>
                <summary>🔍 Config A Diff</summary>
                <pre>{JSON.stringify(resultA.config, null, 2)}</pre>
            </details>
            {#if Object.keys(resultA.config).length > 0}
            <table class="diff-table" style="margin-top: 1rem;">
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
            <pre>{resultB.output}</pre>
            <details>
                <summary>🔍 Config B Diff</summary>
                <pre>{JSON.stringify(resultB.config, null, 2)}</pre>
            </details>
            {#if Object.keys(resultB.config).length > 0}
            <table class="diff-table" style="margin-top: 1rem;">
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
        </div>
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

<style>
    h1 {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #2a3b4c;
    }

    textarea {
        width: 100%;
        padding: 0.75rem;
        font-size: 1rem;
        border: 1px solid #ccc;
        border-radius: 8px;
        resize: vertical;
        background: #fff;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
    }

    button {
        background: #007acc;
        color: white;
        border: none;
        padding: 0.6rem 1.25rem;
        border-radius: 6px;
        cursor: pointer;
        font-size: 0.95rem;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }

    button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    button:hover:not(:disabled) {
        background: #005fa3;
    }

    .config-panels {
        display: flex;
        gap: 2rem;
        margin-bottom: 2rem;
    }

    .config-card {
        flex: 1;
        background: #ffffff;
        padding: 1rem 1.25rem;
        border-radius: 12px;
        border: 1px solid #dde4ea;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
    }

    .config-card h3 {
        margin-bottom: 0.5rem;
        font-size: 1rem;
        font-weight: 500;
        color: #2a3b4c;
    }

    .config-card label {
        display: block;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }

    select {
        width: 100%;
        padding: 0.45rem;
        border: 1px solid #ccc;
        border-radius: 6px;
        font-size: 0.9rem;
    }

    .compare-output {
        display: flex;
        gap: 2rem;
        margin-top: 2rem;
    }

    .result-card {
        flex: 1;
        background: #ffffff;
        border: 1px solid #ccc;
        padding: 1rem 1.25rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        display: flex;
        flex-direction: column;
    }

    .result-card h4 {
        font-size: 1rem;
        margin-bottom: 0.5rem;
        color: #2a3b4c;
    }

    .result-card p {
        font-size: 0.85rem;
        margin: 0.2rem 0;
    }

    pre {
        white-space: pre-wrap;
        background: #f6f8fa;
        padding: 0.75rem;
        border-radius: 6px;
        font-size: 0.9rem;
        line-height: 1.4;
        margin-top: 0.75rem;
        flex-grow: 1;
        overflow: auto;
    }

    .metric-bar {
        font-size: 0.75rem;
        margin: 0.4rem 0;
    }

    .metric-bar span {
        display: inline-block;
        margin-bottom: 0.15rem;
        color: #333;
    }

    .bar {
        height: 10px;
        background: #e0e0e0;
        border-radius: 5px;
        overflow: hidden;
        box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.6);
    }

    .fill {
        height: 100%;
        background: #007acc;
        transition: width 0.5s ease-in-out;
        border-radius: 5px 0 0 5px;
        box-shadow: 0 0 6px #007accaa;
    }

    details {
        margin-top: 1rem;
        font-size: 0.85rem;
        color: #444;
    }

    details summary {
        cursor: pointer;
        font-weight: 600;
        user-select: none;
    }

    .diff-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1rem;
        font-size: 0.9rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
        overflow: hidden;
    }

    .diff-table th,
    .diff-table td {
        border: 1px solid #ddd;
        padding: 0.5rem 0.75rem;
        text-align: left;
        background: #fff;
    }

    .diff-table th {
        background: #f3f4f6;
        font-weight: 600;
        color: #2a3b4c;
    }

    .diff-table tr:nth-child(even) td {
        background: #fafbfc;
    }

</style>
