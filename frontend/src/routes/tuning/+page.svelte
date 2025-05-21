<h1>🎛️ Model Tuning</h1>

<div class="param-grid">
  {#each parameters as param}
    <div class="param-tile {selectedParam && selectedParam.key === param.key ? 'active' : ''}" on:click={() => openPanel(param.key)}>
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
      eli5: 'Think of this like how wild or calm your story is. Low means very calm and predictable, high means wild and surprising.',
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
      eli5: 'Imagine choosing from only the top few options instead of all. Lower means fewer choices, making answers more predictable.',
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
      eli5: 'Think of this as picking words from a basket until you reach a certain chance. Lower means fewer words, so answers are simpler.',
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
      eli5: 'This is like setting a word limit for the answer. Lower means short answers, higher means longer ones.',
      lowEffect: 'Shorter, punchy replies',
      highEffect: 'Longer, detailed completions',
      type: 'number',
      min: 16,
      max: 2048
    }
  ];

  function openPanel(key) {
    if (selectedParam && selectedParam.key === key) {
      selectedParam = null;
    } else {
      selectedParam = parameters.find(p => p.key === key);
    }
  }

  function updateConfig(key, value) {
    config[key] = value;
    localStorage.setItem('grailConfig', JSON.stringify(config));
    savedStatus = '💾 Config saved';
  }
</script>

{#if selectedParam}
  <div class="param-drawer">
    <button class="drawer-toggle" on:click={() => selectedParam = null}>▶</button>
    <h2>{selectedParam.label}</h2>
    <p>{selectedParam.definition}</p>
    <p><em>{selectedParam.eli5}</em></p>
    <div style="margin: 1rem 0;">
      {#if selectedParam.type === 'slider'}
        <input
          type="range"
          min={selectedParam.min}
          max={selectedParam.max}
          step={selectedParam.step}
          bind:value={config[selectedParam.key]}
          on:input={(e) => updateConfig(selectedParam.key, +e.target.value)} />
      {:else}
        <input
          type="number"
          min={selectedParam.min}
          max={selectedParam.max}
          bind:value={config[selectedParam.key]}
          on:input={(e) => updateConfig(selectedParam.key, +e.target.value)} />
      {/if}
    </div>
    <p><strong>Low:</strong> {selectedParam.lowEffect}</p>
    <p><strong>High:</strong> {selectedParam.highEffect}</p>
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

  .param-tile.active {
    border-color: #007acc;
    background: #d0e7ff;
  }

  .param-drawer {
    position: fixed;
    top: 0;
    right: 360px;
    width: 320px;
    height: 100vh;
    padding: 2rem;
    background: white;
    border-left: 1px solid #ddd;
    box-shadow: -2px 0 8px rgba(0,0,0,0.1);
    overflow-y: auto;
    z-index: 100;
  }

  .drawer-toggle {
    position: absolute;
    left: -1.75rem;
    top: 1rem;
    background: #fff;
    border: 1px solid #ccc;
    border-radius: 4px;
    cursor: pointer;
    padding: 0.25rem 0.5rem;
    transform: rotate(180deg);
  }
</style>