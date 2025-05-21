<h1>🎛️ Model Tuning</h1>
<p>Controls for model architecture and generation settings will live here.</p>

<script>
  import { onMount } from 'svelte';

  let config = {
    temperature: 0.7,
    top_k: 50,
    top_p: 0.9,
    max_tokens: 256
  };

  let savedStatus = '';

  onMount(() => {
    const saved = localStorage.getItem('grailConfig');
    if (saved) {
      config = JSON.parse(saved);
      savedStatus = '✅ Loaded saved config';
    }
  });

  function save() {
    localStorage.setItem('grailConfig', JSON.stringify(config));
    savedStatus = '💾 Config saved';
  }

  function reset() {
    config = {
      temperature: 0.7,
      top_k: 50,
      top_p: 0.9,
      max_tokens: 256
    };
    savedStatus = '↩️ Reset to default';
  }
</script>

<h1>🎛️ Tuning</h1>

<h2>🧪 Sampling Parameters</h2>
<form on:submit|preventDefault={save}>
  <label>
    Temperature: {config.temperature}
    <input type="range" min="0" max="1.5" step="0.05" bind:value={config.temperature} />
  </label>

  <label>
    Top-P: {config.top_p}
    <input type="range" min="0" max="1" step="0.01" bind:value={config.top_p} />
  </label>

  <label>
    Top-K:
    <input type="number" min="0" max="100" bind:value={config.top_k} />
  </label>

  <h2>📏 Output Controls</h2>
  <label>
    Max Tokens:
    <input type="number" min="16" max="2048" bind:value={config.max_tokens} />
  </label>

  <div style="margin-top: 1rem;">
    <button type="submit">💾 Save Config</button>
    <button type="button" on:click={reset}>↩️ Reset</button>
    <p>{savedStatus}</p>
  </div>
</form>