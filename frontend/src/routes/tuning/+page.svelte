<h1>🎛️ Model Tuning</h1>

<div class="param-grid">
  {#each parameters as param}
    <div class="param-tile">
      <strong>{param.label}</strong>
      <p style="font-size: 0.9rem; margin-bottom: 0.5rem;">{param.definition}</p>
      <p><em style="font-size: 0.85rem;">{param.eli5}</em></p>
      <div style="margin: 0.75rem 0;">
        {#if param.type === 'slider'}
          <input
            type="range"
            min={param.min}
            max={param.max}
            step={param.step}
            bind:value={config[param.key]}
            on:input={(e) => updateConfig(param.key, +e.target.value)} />
        {:else}
          <input
            type="number"
            min={param.min}
            max={param.max}
            bind:value={config[param.key]}
            on:input={(e) => updateConfig(param.key, +e.target.value)} />
        {/if}
      </div>
      <p><strong>Low:</strong> {param.lowEffect}</p>
      <p><strong>High:</strong> {param.highEffect}</p>
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

  function updateConfig(key, value) {
    config[key] = value;
    localStorage.setItem('grailConfig', JSON.stringify(config));
    savedStatus = '💾 Config saved';
  }
</script>

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
</style>