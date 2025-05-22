<script>
    import {onMount} from 'svelte';
    import {browser} from '$app/environment';
    import {fade} from 'svelte/transition';
    import {marked} from 'marked';

    import DOMPurify from 'dompurify';
    import hljs from 'highlight.js';
    import 'highlight.js/styles/github.css';

    marked.setOptions({
      highlight: function (code, lang) {
        const valid = hljs.getLanguage(lang) ? lang : 'plaintext';
        return hljs.highlight(code, { language: valid }).value;
      }
    });

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
    // Preset support
    let comparePresets = [];
    let presetName = '';
    let selectedPreset = '';
    let layoutMode = 'side-by-side';

    onMount(() => {
        // Theme preference auto-detect
        if (!localStorage.getItem("theme")) {
          const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
          localStorage.setItem("theme", prefersDark ? "dark" : "light");
          document.body.classList.toggle("dark", prefersDark);
        }
        darkMode = localStorage.getItem("theme") === "dark";
        document.body.classList.toggle("dark", darkMode);
        if (browser) {
            // Persistent compare history export: restore lastComparePrompt
            const lastPrompt = localStorage.getItem('lastComparePrompt');
            if (lastPrompt) prompt = lastPrompt;

            const savedY = localStorage.getItem('compareScroll');
            if (savedY) requestAnimationFrame(() => window.scrollTo(0, parseInt(savedY)));

            const stored = localStorage.getItem('compareHistory');
            if (stored) history = JSON.parse(stored);

            // Load comparePresets from localStorage
            const presetStore = localStorage.getItem('comparePresets');
            if (presetStore) comparePresets = JSON.parse(presetStore);

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

    function saveComparePreset() {
        if (!presetName.trim()) return;
        comparePresets.push({
            name: presetName.trim(),
            prompt,
            configA,
            configB
        });
        localStorage.setItem('comparePresets', JSON.stringify(comparePresets));
        presetName = '';
    }

    function loadComparePreset() {
        const found = comparePresets.find(p => p.name === selectedPreset);
        if (found) {
            prompt = found.prompt;
            configA = found.configA;
            configB = found.configB;
        }
    }

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
            if (!response.ok) {
                resultA = null;
                resultB = null;
                alert("Comparison failed. Please try again.");
                loading = false;
                return;
            }
            const data = await response.json();
            resultA = data.result_a;
            resultB = data.result_b;
        } else {
            const response = await fetch('/compare/batch', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompts, config_a: configA, config_b: configB})
            });
            if (!response.ok) {
                resultA = null;
                resultB = null;
                alert("Comparison failed. Please try again.");
                loading = false;
                return;
            }
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

        // Persistent compare history export: save lastComparePrompt
        if (browser) {
            localStorage.setItem('lastComparePrompt', prompt);
            setTimeout(() => localStorage.setItem('compareScroll', window.scrollY), 100);
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
        const keys = new Set([...Object.keys(configA || {}), ...Object.keys(configB || {})]);
        return Array.from(keys)
            .filter(key => showAllDiff || (configA && configB && configA[key] !== configB[key]))
            .sort()
            .map(key => ({key, a: configA ? configA[key] : undefined, b: configB ? configB[key] : undefined}));
    }

    function exportResults(format = 'json') {
        const safeA = resultA && resultA.model ? resultA : { model: 'modelA', output: '' };
        const safeB = resultB && resultB.model ? resultB : { model: 'modelB', output: '' };

        const name = resultA?.filename || `${safeA.model}_vs_${safeB.model}_${Date.now()}`;
        const blob = new Blob([
            format === 'json'
                ? JSON.stringify({prompt, configA, configB, resultA: safeA, resultB: safeB}, null, 2)
                : `# Prompt:\n${prompt}\n\n## ${safeA.model}:\n${safeA.output}\n\n## ${safeB.model}:\n${safeB.output}`
        ], {type: format === 'json' ? 'application/json' : 'text/markdown'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `compare_${name}.${format === 'json' ? 'json' : 'md'}`;
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

    function highlightDiff(a, b) {
      if (!a || !b) return a;
      const aWords = a.split(/\s+/);
      const bWords = new Set(b.split(/\s+/));
      return aWords.map(word =>
              bWords.has(word) ? word : `<span class="diff-miss">${word}</span>`
      ).join(' ');
    }


</script>
<style src="/src/app.css"></style>

<div class="page-container">
  {#if history.length > 0}
    <div class="card-block">
      <label class="field-label">Load Previous Prompt</label>
      <select on:change={(e) => {
        const item = history.find(h => h.timestamp.toString() === e.target.value);
        if (item) {
          prompt = item.prompt;
          configA = item.configA;
          configB = item.configB;
        }
      }}>
        <option value="">-- select --</option>
        {#each history as h}
          <option value={h.timestamp}>{new Date(h.timestamp).toLocaleString()} | {h.summary}</option>
        {/each}
      </select>
    </div>
  {/if}

  <div class="card-block">
    <label class="field-label">Prompt</label>
    <div class="preset-buttons">
      <button on:click={() => prompt = 'Explain quantum computing to a child.'}>Explain like I&apos;m five</button>
      <button on:click={() => prompt = 'Write a poem about the sea.'}>Generate poetry</button>
      <button on:click={() => prompt = 'Translate: "I love you" into Japanese.'}>Translation test</button>
    </div>
    <textarea bind:value={prompt} rows="4" class="full-input" placeholder="Enter one or more prompts, separated by line breaks"></textarea>
  </div>

  <div class="card-block">
    <input type="text" bind:value={presetName} placeholder="Save compare preset as..." />
    <button on:click={saveComparePreset}>💾 Save Compare Preset</button>
  </div>

  {#if comparePresets.length > 0}
    <div class="card-block">
      <select bind:value={selectedPreset}>
        <option value="">Load compare preset...</option>
        {#each comparePresets as p}
          <option value={p.name}>{p.name}</option>
        {/each}
      </select>
      <button on:click={loadComparePreset} disabled={!selectedPreset}>📥 Load Preset</button>
    </div>
  {/if}

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

  {#if resultA && resultB}
    <div class="card-block">
      <h3 class="section-title">📊 Metrics</h3>
      <table class="metrics-table">
        <thead>
          <tr>
            <th>Metric</th>
            <th>{resultA.model}</th>
            <th>{resultB.model}</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Latency (ms)</td><td>{resultA.latency_ms}</td><td>{resultB.latency_ms}</td></tr>
          <tr><td>Tokens</td><td>{resultA.tokens}</td><td>{resultB.tokens}</td></tr>
          <tr><td>Cost</td><td>{estimateCost(resultA.model, resultA.tokens)}</td><td>{estimateCost(resultB.model, resultB.tokens)}</td></tr>
        </tbody>
      </table>
    </div>

    <div class="card-block">
      <label>
        <input type="checkbox" bind:checked={showAllDiff} />
        Show full config
      </label>
      <table class="diff-table" style="margin-top: 1rem;">
        <thead>
          <tr>
            <th>Parameter</th>
            <th>Config A</th>
            <th>Config B</th>
          </tr>
        </thead>
        <tbody>
          {#each getDiffTable(resultA?.config, resultB?.config) as row}
            <tr title={row.key}>
              <td>
                <span class="param-label-tooltip" title={row.key}>
                  {row.key}
                </span>
              </td>
              <td>{row.a}</td>
              <td>{row.b}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}

  <div class="card-block">
    <label class="field-label">Output Layout</label>
    <select bind:value={layoutMode}>
      <option value="side-by-side">🧩 Side-by-side</option>
      <option value="stacked">📚 Stacked</option>
    </select>
  </div>

  {#if resultA && resultB && !Array.isArray(resultA)}
    <div class="card-block {layoutMode === 'stacked' ? 'output-stacked' : 'compare-output'}">
      <div class="output-block">
        <h4>🧠 {resultA.model}</h4>
        <button class="copy-btn" on:click={() => navigator.clipboard.writeText(resultA.output)}>📋 Copy</button>
        {@html highlightDiff(resultA.output, resultB.output)}
      </div>
      <div class="output-block">
        <h4>🧠 {resultB.model}</h4>
        <button class="copy-btn" on:click={() => navigator.clipboard.writeText(resultB.output)}>📋 Copy</button>
        {@html highlightDiff(resultB.output, resultA.output)}
      </div>
    </div>
  {/if}

  <div class="card-block controls-row spaced">
    <button class="mini" on:click={() => exportResults('json')}>📤 Export JSON</button>
    <button class="mini" on:click={() => exportResults('md')}>📝 Export Markdown</button>
    <button class="mini" on:click={exportResultsCSV}>📊 Export CSV</button>
    <button class="mini" on:click={exportBatchMarkdown}>📘 Export Batch Markdown</button>
    <button class="mini" on:click={encodeCompareURL}>🔗 Copy Shareable Link</button>
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

  {#if resultA && resultB}
    <div class="summary-box">
      <p class="tldr-summary">TL;DR: {getTldrSummary(resultA, resultB)}</p>
      <button class="primary-button" on:click={runComparison}>🔁 Retry Last Comparison</button>
    </div>
  {/if}

  {#if Array.isArray(resultA)}
    <div class="card-block">
      <h3 class="section-title">📜 Batch Prompt Results</h3>
      <table class="metrics-table">
        <thead>
          <tr>
            <th>Prompt</th>
            <th>{resultA[0].result_a.model}</th>
            <th>{resultA[0].result_b.model}</th>
          </tr>
        </thead>
        <tbody>
          {#each resultA as row}
            <tr>
              <td>{row.prompt}</td>
              <td>
                <details>
                  <summary>{row.result_a.output.slice(0, 60)}...</summary>
                  {@html renderMarkdown(row.result_a.output)}
                </details>
                <small>{row.result_a.tokens} tokens · {row.result_a.latency_ms} ms</small>
              </td>
              <td>
                <details>
                  <summary>{row.result_b.output.slice(0, 60)}...</summary>
                  {@html renderMarkdown(row.result_b.output)}
                </details>
                <small>{row.result_b.tokens} tokens · {row.result_b.latency_ms} ms</small>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}

  {#if !loading && (!resultA || !resultB)}
    <div class="empty-message">
      <p>👋 Enter a prompt and click <strong>Run Comparison</strong> to see results.</p>
    </div>
  {/if}
</div>
