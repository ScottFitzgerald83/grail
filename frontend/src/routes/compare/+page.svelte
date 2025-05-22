<script>
    import {onMount} from 'svelte';
    import {browser} from '$app/environment';
    import {fade} from 'svelte/transition';
    import {marked} from 'marked';
    import DOMPurify from 'dompurify';

    let darkMode = false;
    let condensedView = false;
    let scrollY = 0;
    let prompt = '';
    let configA = {public_model_name: 'gpt-4'};
    let configB = {public_model_name: 'ollama:llama2'};
    let resultA = null;
    let resultB = null;
    let loading = false;
    let showAllDiff = true;
    let history = [];

    onMount(() => {
        darkMode = localStorage.getItem("theme") === "dark";
        document.body.classList.toggle("dark", darkMode);
        if (browser) {
            const savedY = localStorage.getItem('compareScroll');
            if (savedY) requestAnimationFrame(() => window.scrollTo(0, parseInt(savedY)));

            const stored = localStorage.getItem('compareHistory');
            if (stored) history = JSON.parse(stored);

            if (location.hash) {
                try {
                    const parsed = JSON.parse(atob(location.hash.slice(1)));
                    prompt = parsed.prompt;
                    configA = parsed.configA;
                    configB = parsed.configB;
                } catch {
                }
            }
        }
    });

    function toggleDarkMode() {
        darkMode = !darkMode;
        localStorage.setItem("theme", darkMode ? "dark" : "light");
        document.body.classList.toggle("dark", darkMode);
    }

    function renderMarkdown(html) {
        return DOMPurify.sanitize(marked.parse(html || ''));
    }

    async function runComparison() {
        loading = true;
        const prompts = prompt.split("\\n").join("\n").split('\n').filter(p => p.trim());
        if (prompts.length === 1) {
            const response = await fetch('/compare', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompt, config_a: configA, config_b: configB})
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
            resultB = Array.isArray(data) && data.length > 0 ? data[0].result_b : null;
        }
        loading = false;

        if (browser && !Array.isArray(resultA)) {
            const entry = {
                timestamp: Date.now(),
                prompt,
                configA,
                configB,
                modelA: resultA.model,
                modelB: resultB.model,
                summary: getTldrSummary(resultA, resultB)
            };
            history.unshift(entry);
            localStorage.setItem('compareHistory', JSON.stringify(history.slice(0, 10)));
        }
    }

    function estimateCost(model, tokens) {
        if (!model || !tokens) return "$0.00";
        if (model.startsWith("gpt-4")) return `$${((tokens / 1000) * 0.06).toFixed(4)}`;
        if (model.startsWith("gpt-3.5")) return `$${((tokens / 1000) * 0.002).toFixed(4)}`;
        return "$0.00";
    }

    function getTldrSummary(a, b) {
        if (!a || !b) return '';
        const speed = a.latency_ms < b.latency_ms ? '🚀' : '🐢';
        const cost = estimateCost(a.model, a.tokens) > estimateCost(b.model, b.tokens) ? '💸' : '💡';
        return `${a.model} ${speed}${cost} vs ${b.model}`;
    }

    function getDiffTable(configA, configB) {
        const keys = new Set([...Object.keys(configA), ...Object.keys(configB)]);
        return Array.from(keys)
            .filter(key => showAllDiff || configA[key] !== configB[key])
            .sort()
            .map(key => ({key, a: configA[key], b: configB[key]}));
    }

    function exportResults(format = 'json') {
        const safeA = resultA && resultA.model ? resultA : { model: 'modelA', output: '' };
        const safeB = resultB && resultB.model ? resultB : { model: 'modelB', output: '' };
        const name = `${safeA.model}_vs_${safeB.model}`;
        const blob = new Blob([
            format === 'json'
                ? JSON.stringify({prompt, configA, configB, resultA: safeA, resultB: safeB}, null, 2)
                : `# Prompt:\n${prompt}\n\n## ${safeA.model}:\n${safeA.output}\n\n## ${safeB.model}:\n${safeB.output}`
        ], {type: format === 'json' ? 'application/json' : 'text/markdown'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `compare_${name}_${timestamp}.${format === 'json' ? 'json' : 'md'}`;
        a.click();
        URL.revokeObjectURL(url);
    }

    function exportResultsCSV() {
        if (!Array.isArray(resultA)) return;

        const rows = resultA.filter(row =>
          row.result_a && row.result_b
        ).map(row => [
          row.prompt,
          row.result_a.model,
          estimateCost(row.result_a.model, row.result_a.tokens),
          row.result_a.output,
          row.result_a.latency_ms,
          row.result_a.tokens,
          row.result_b.model,
          estimateCost(row.result_b.model, row.result_b.tokens),
          row.result_b.output,
          row.result_b.latency_ms,
          row.result_b.tokens
        ]);
        const header = [
            'Prompt', 'Model A', 'Cost A', 'Output A', 'Latency A', 'Tokens A',
            'Model B', 'Cost B', 'Output B', 'Latency B', 'Tokens B'
        ];
        const csv = [header, ...rows].map(r => r.map(c => `"${(c || '').toString().replace(/"/g, '""')}"`).join(',')).join('\n');
        const blob = new Blob([csv], {type: 'text/csv'});
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
            const costA = estimateCost(row.result_a.model, row.result_a.tokens);
            const costB = estimateCost(row.result_b.model, row.result_b.tokens);
            return `## Prompt
${row.prompt}

### ${row.result_a.model} (cost: ${costA})
${row.result_a.output}

### ${row.result_b.model} (cost: ${costB})
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

    function encodeCompareURL() {
        const base = typeof location !== 'undefined' ? location.origin : '';
        const encoded = btoa(JSON.stringify({prompt, configA, configB}));
        const link = `${base}/compare#${encoded}`;
        navigator.clipboard.writeText(link);
        alert("Link copied to clipboard!");
    }
</script>

<div class="page-container">
  <div class="card-block">
    <label class="field-label">Prompt</label>
    <textarea bind:value={prompt} rows="4" class="full-input" placeholder="Enter one or more prompts, separated by line breaks"></textarea>
  </div>

  <div class="card-block config-panels">
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

  <hr class="section-divider" />

  <div class="controls-row spaced">
    <div class="control-item">
      <label class="toggle-label">
        <input type="checkbox" bind:checked={condensedView} />
        Condensed View
      </label>
    </div>
    <div class="control-item">
      <button class="primary-button" on:click={runComparison} disabled={loading}>
        {loading ? 'Comparing...' : 'Run Comparison'}
      </button>
    </div>
  </div>

  {#if !loading && (!resultA || !resultB)}
    <div class="empty-message">
      <p>👋 Enter a prompt and click <strong>Run Comparison</strong> to see results.</p>
    </div>
  {/if}
</div>
