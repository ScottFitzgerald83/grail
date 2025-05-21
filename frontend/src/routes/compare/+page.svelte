<script>
  let prompt = '';
  let configA = { public_model_name: 'gpt-4' };
  let configB = { public_model_name: 'ollama:llama2' };
  let resultA = null;
  let resultB = null;
  let loading = false;

  async function runComparison() {
    loading = true;
    const response = await fetch('/compare', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
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
</script>

<h1>🔁 Compare</h1>

<div style="margin-bottom: 1rem;">
  <textarea bind:value={prompt} rows="3" placeholder="Enter a prompt to test" style="width: 100%; padding: 0.75rem; font-size: 1rem;"></textarea>
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
    <div class="result-card">
      <h4>{resultA.model}</h4>
      <p><strong>Latency:</strong> {resultA.latency_ms} ms</p>
      <p><strong>Tokens:</strong> {resultA.tokens}</p>
      <pre>{resultA.output}</pre>
    </div>
    <div class="result-card">
      <h4>{resultB.model}</h4>
      <p><strong>Latency:</strong> {resultB.latency_ms} ms</p>
      <p><strong>Tokens:</strong> {resultB.tokens}</p>
      <pre>{resultB.output}</pre>
    </div>
  </div>
{/if}

<style>
  .config-panels {
    display: flex;
    gap: 2rem;
    margin-bottom: 1rem;
  }
  .config-card {
    flex: 1;
    background: #f9fafc;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #ddd;
  }
  .compare-output {
    display: flex;
    gap: 2rem;
    margin-top: 2rem;
  }
  .result-card {
    flex: 1;
    background: #fff;
    border: 1px solid #ccc;
    padding: 1rem;
    border-radius: 8px;
  }
  pre {
    white-space: pre-wrap;
    background: #f6f8fa;
    padding: 0.75rem;
    border-radius: 6px;
    font-size: 0.9rem;
  }
</style>