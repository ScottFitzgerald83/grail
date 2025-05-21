<h1>🎛️ Model Tuning</h1>

<div class="param-grid">
  {#each parameters as param}
    <div class="param-tile" on:click={() => openPanel(param.key)}>
      <strong>{param.label}</strong>
      <p style="font-size: 0.9rem;">{config[param.key]}</p>
    </div>
  {/each}
</div>

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

  let selectedParam = null;

  const parameters = [
    {
      key: 'temperature',
      label: 'Temperature',
      definition: 'Controls output randomness. Lower = more deterministic, Higher = more creative.',
      lowEffect: 'Safe, factual completions',
      highEffect: 'Diverse, surprising completions',
      type: 'slider',
      min: 0,
      max: 1.5,
      step: 0.05
    },
    {
      key: 'top_k',
      label: 'Top-K',
      definition: 'Restricts sampling to top K tokens. Lower = less randomness.',
      lowEffect: 'Conservative, predictable output',
      highEffect: 'Expansive, less filtered output',
      type: 'number',
      min: 0,
      max: 100
    },
    {
      key: 'top_p',
      label: 'Top-P',
      definition: 'Limits sampling to top P probability mass. Lower = less variation.',
      lowEffect: 'Tight, repetitive phrasing',
      highEffect: 'Fluent, expressive variation',
      type: 'slider',
      min: 0,
      max: 1,
      step: 0.01
    },
    {
      key: 'max_tokens',
      label: 'Max Tokens',
      definition: 'Maximum number of tokens to generate.',
      lowEffect: 'Shorter, punchy replies',
      highEffect: 'Longer, detailed completions',
      type: 'number',
      min: 16,
      max: 2048
    }
  ];

  function openPanel(key) {
    selectedParam = parameters.find(p => p.key === key);
  }
</script>

{#if selectedParam}
  <div class="param-drawer">
    <h2>{selectedParam.label}</h2>
    <p>{selectedParam.definition}</p>
    <div style="margin: 1rem 0;">
      {#if selectedParam.type === 'slider'}
        <input
          type="range"
          min={selectedParam.min}
          max={selectedParam.max}
          step={selectedParam.step}
          bind:value={config[selectedParam.key]} />
      {:else}
        <input
          type="number"
          min={selectedParam.min}
          max={selectedParam.max}
          bind:value={config[selectedParam.key]} />
      {/if}
    </div>
    <p><strong>Low:</strong> {selectedParam.lowEffect}</p>
    <p><strong>High:</strong> {selectedParam.highEffect}</p>
    <div style="margin-top: 1rem;">
      <button on:click={save}>💾 Save</button>
      <button on:click={() => selectedParam = null}>✖ Close</button>
    </div>
  </div>
{/if}

<style>
  .param-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 1rem;
    margin-top: 1.5rem;
  }

  .param-tile {
    background: #f5f5f5;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .param-tile:hover {
    background: #eef2f7;
  }

  .param-drawer {
    position: fixed;
    top: 0;
    right: 0;
    width: 360px;
    height: 100vh;
    padding: 2rem;
    background: white;
    border-left: 1px solid #ddd;
    box-shadow: -2px 0 8px rgba(0,0,0,0.1);
    overflow-y: auto;
    z-index: 100;
  }
</style>