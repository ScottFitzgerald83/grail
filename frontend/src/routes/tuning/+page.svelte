<h1>🎛️ Model Tuning</h1>

<div class="preset-buttons">
    {#each Object.keys(presets) as preset}
        <button on:click={() => applyPreset(preset)}>{preset}</button>
    {/each}
</div>

<div class="param-grid">
  {#each parameters as param}
    <div class="param-tile" title={param.eli5}>
      <div class="param-header">
        <strong>{param.label}</strong>
        <span class="help-icon-wrapper">
          <span class="help-icon">❓</span>
          <div class="tooltip-card">{param.eli5}</div>
        </span>
      </div>
      <p class="param-category">{paramCategory(param.key)}</p>
      <p style="font-size: 0.9rem; margin-bottom: 0.5rem;">{param.definition}</p>
      <div class="param-control">
        <label>
          <span class="param-label">{param.label}</span>
          <span class="param-value">
            {#if param.type === 'slider'}
              {config[param.key].toFixed(2)} ({fuzzyLabel(param, config[param.key])})
            {:else if param.type === 'number'}
              {config[param.key]}
            {:else}
              {config[param.key]}
            {/if}
          </span>
        </label>
        {#if param.type === 'slider'}
          <div class="slider-labels">
            <span>{param.lowLabel || 'Low'}</span>
            <span>{param.highLabel || 'High'}</span>
          </div>
          <input type="range" min={param.min} max={param.max} step={param.step}
                 bind:value={config[param.key]}
                 on:input={(e) => updateConfig(param.key, +e.target.value)}
                 style="background: {sliderGradient(param.key)}"/>
        {:else if param.type === 'number'}
          <input type="number" min={param.min} max={param.max}
                 bind:value={config[param.key]}
                 on:input={(e) => updateConfig(param.key, +e.target.value)}/>
        {:else if param.type === 'text'}
          <input type="text"
                 bind:value={config[param.key]}
                 on:input={(e) => updateConfig(param.key, e.target.value)}/>
        {:else if param.type === 'select'}
          <select bind:value={config[param.key]}
                  on:change={(e) => updateConfig(param.key, e.target.value)}>
            {#each param.options as option}
              <option value={option}>{option}</option>
            {/each}
          </select>
        {/if}
        <button class="reset-btn" on:click={() => updateConfig(param.key, getDefault(param.key))}>
          Reset
        </button>
        <p class="dynamic-desc">{fuzzyLabel(param, config[param.key])} level selected</p>
      </div>
    </div>
  {/each}
</div>

<h2 style="margin-top: 2rem;">🧠 Predicted Model Behavior</h2>
<table class="performance-table">
    <thead>
    <tr>
        <th>Metric</th>
        <th>Impact</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    {#each Object.entries(computeMetrics(config)) as [key, value]}
        <tr>
            <td>{key[0].toUpperCase() + key.slice(1)}</td>
            <td>
                <div class="bar-bg">
                    <div class="bar-fill" style="width: {barWidth(value)}; background: {barColor(key, value)}"></div>
                </div>
            </td>
            <td>
                {#if key === 'creativity'}Too low = boring output; too high = chaotic, off-topic, or hallucinated
                    content.
                {/if}
                {#if key === 'coherence'}Too low = disjointed or nonsensical replies; higher values improve logical
                    flow.
                {/if}
                {#if key === 'repetition'}Higher values increase the chance of word or idea loops; lower is usually
                    better.
                {/if}
                {#if key === 'length'}Lower values may feel abrupt; higher values allow more explanation (at a cost).
                {/if}
                {#if key === 'latency'}Higher values mean slower response time; may frustrate users or delay feedback.
                {/if}
                {#if key === 'cost'}Higher values increase token usage and compute load; affects scalability and
                    billing.
                {/if}
            </td>
        </tr>
    {/each}
    </tbody>
</table>

<h2 style="margin-top: 2rem;">📤 Export & Import Config</h2>
<div style="margin-bottom: 1rem;">
  <button on:click={exportConfig}>Download Config</button>
  <input type="file" accept=".json" on:change={importConfig} />
</div>





<script>
    import {onMount} from 'svelte';
    import {browser} from '$app/environment';
    // Fuzzy label for slider value
    function fuzzyLabel(param, value) {
      if (param.type !== 'slider') return '';
      const levels = ['Low', 'Medium', 'High'];
      const percent = (value - param.min) / (param.max - param.min);
      if (percent <= 0.33) return levels[0];
      if (percent <= 0.66) return levels[1];
      return levels[2];
    }

    function getDefault(key) {
      return {
        temperature: 0.7,
        top_k: 50,
        top_p: 0.9,
        max_tokens: 256,
        presence_penalty: 0.0,
        frequency_penalty: 0.0,
        stop_sequence: '',
        response_style: 'Default'
      }[key];
    }

    // Color-coded slider gradient based on parameter key
    function sliderGradient(key) {
      const themes = {
        temperature: 'linear-gradient(to right, #b3e5fc, #03a9f4)',
        top_p: 'linear-gradient(to right, #e1bee7, #9c27b0)',
        top_k: 'linear-gradient(to right, #fff59d, #fbc02d)',
        presence_penalty: 'linear-gradient(to right, #c8e6c9, #4caf50)',
        frequency_penalty: 'linear-gradient(to right, #ffcdd2, #f44336)',
        max_tokens: 'linear-gradient(to right, #b0bec5, #607d8b)'
      };
      return themes[key] || 'linear-gradient(to right, #4caf50, #ffeb3b, #f44336)';
    }


    let config = {
        temperature: 0.7,
        top_k: 50,
        top_p: 0.9,
        max_tokens: 256,
        presence_penalty: 0.0,
        frequency_penalty: 0.0,
        stop_sequence: '',
        response_style: 'Default',
    };

    let savedStatus = '';

    onMount(() => {
        if (browser) {
            const saved = localStorage.getItem('grailConfig');
            if (saved) {
                config = JSON.parse(saved);
                savedStatus = '✅ Loaded saved config';
            }
        }
    });

    function reset() {
        config = {
            temperature: 0.7,
            top_k: 50,
            top_p: 0.9,
            max_tokens: 256,
            presence_penalty: 0.0,
            frequency_penalty: 0.0,
            stop_sequence: '',
            response_style: 'Default',
        };
        savedStatus = '↩️ Reset to default';
    }

    const presets = {
        Creative: {
            temperature: 1.2,
            top_k: 40,
            top_p: 1,
            presence_penalty: 1.5,
            frequency_penalty: 0.7,
            max_tokens: 256,
            response_style: 'Creative'
        },
        Concise: {
            temperature: 0.3,
            top_k: 20,
            top_p: 0.8,
            presence_penalty: 0.1,
            frequency_penalty: 0.2,
            max_tokens: 100,
            response_style: 'Concise'
        },
        Balanced: {
            temperature: 0.7,
            top_k: 50,
            top_p: 0.9,
            presence_penalty: 0.5,
            frequency_penalty: 0.5,
            max_tokens: 128,
            response_style: 'Default'
        }
    };

    function applyPreset(name) {
        config = {...config, ...presets[name]};
        localStorage.setItem('grailConfig', JSON.stringify(config));
        savedStatus = `🎛️ ${name} preset loaded`;
    }

    const parameters = [
        {
            key: 'temperature',
            label: 'Temperature',
            definition: 'Controls output randomness. Lower = more deterministic, Higher = more creative.',
            eli5: 'Controls randomness. Lower values produce safe, predictable answers. Higher values increase creativity but risk hallucination or off-topic responses.',
            type: 'slider',
            min: 0,
            max: 1.5,
            step: 0.05,
            lowLabel: 'Calm 🧘',
            highLabel: 'Wild 🌪'
        },
        {
            key: 'top_k',
            label: 'How many top choices to consider?',
            definition: 'Restricts sampling to top K tokens. Lower = less randomness.',
            eli5: 'Limits token selection to the top K most likely options. Smaller values force the model to stay focused. Larger values let it roam, but may lose coherence.',
            type: 'number',
            min: 0,
            max: 100,
            step: 1
        },
        {
            key: 'top_p',
            label: 'Top-P',
            definition: 'Limits sampling to top P probability mass. Lower = less variation.',
            eli5: 'Limits selection to a dynamic group of tokens that collectively reach P probability. Lower values reduce variety. Higher values allow more diverse phrasing.',
            type: 'slider',
            min: 0,
            max: 1,
            step: 0.01,
            lowLabel: 'Tight 🎯',
            highLabel: 'Expressive 🎉'
        },
        {
            key: 'max_tokens',
            label: 'How long should responses be?',
            definition: 'Maximum number of tokens to generate.',
            eli5: 'Sets a cap on response length. Short responses are punchy but may lack depth. Long responses offer more detail but take more time and tokens.',
            type: 'number',
            min: 16,
            max: 2048,
            step: 1
        },
        {
            key: 'presence_penalty',
            label: 'How much should it avoid repeating ideas?',
            definition: 'Encourages introducing new topics and discourages repetition.',
            eli5: 'Discourages the model from repeating the same ideas. Higher values increase topic variety. Lower values make it more likely to stay on the same subject.',
            type: 'slider',
            min: 0,
            max: 2,
            step: 0.1,
            lowLabel: 'Repeat ♻️',
            highLabel: 'New Ideas 💡'
        },
        {
            key: 'frequency_penalty',
            label: 'How much should it avoid repeating words?',
            definition: 'Reduces likelihood of repeating the same tokens.',
            eli5: 'Reduces word repetition. Higher values make phrasing more varied. Lower values may repeat or stutter if the model gets stuck.',
            type: 'slider',
            min: 0,
            max: 2,
            step: 0.1,
            lowLabel: 'Repetitive 🔁',
            highLabel: 'Varied 🆕'
        },
        {
            key: 'stop_sequence',
            label: 'Stop when this text appears',
            definition: 'Ends generation when the model outputs this string.',
            eli5: 'Defines where the model should stop. Useful to prevent it from rambling or continuing too far past a logical stopping point.',
            type: 'text'
        },
        {
            key: 'response_style',
            label: 'Response Style',
            definition: 'Controls the overall tone or formatting of the output.',
            eli5: 'Applies a general tone or formatting style. Useful for controlling personality or structure in the reply.',
            type: 'select',
            options: ['Default', 'Creative', 'Concise']
        }
    ];

    function updateConfig(key, value) {
        config[key] = value;
        localStorage.setItem('grailConfig', JSON.stringify(config));
        savedStatus = '💾 Config saved';
    }

    function score(x) {
        return Math.min(5, Math.max(1, Math.round(x)));
    }

    function computeMetrics(config) {
        if (!browser) return {};
        return {
            creativity: score(config.temperature * 2 + config.top_p * 2 - config.top_k / 100),
            coherence: score(5 - config.temperature * 2 + config.top_k / 20),
            repetition: score(3 - config.top_p * 2),
            length: score(config.max_tokens / 512),
            latency: score(config.max_tokens / 400),
            cost: score((config.max_tokens * 0.001 + config.temperature) / 2)
        };
    }

    function barWidth(value) {
        return `${(value / 5) * 100}%`;
    }

    function barColor(metric, value) {
        const riskyHigh = ['repetition', 'latency', 'cost']; // higher is worse
        const score = riskyHigh.includes(metric) ? 6 - value : value;

        if (score <= 2) return '#f44336'; // red
        if (score === 3) return '#ffeb3b'; // yellow
        return '#4caf50'; // green
    }

    function exportConfig() {
      const blob = new Blob([JSON.stringify(config, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'grail-config.json';
      a.click();
      URL.revokeObjectURL(url);
    }

    function importConfig(event) {
      const file = event.target.files?.[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const newConfig = JSON.parse(e.target.result);
          config = { ...config, ...newConfig };
          localStorage.setItem('grailConfig', JSON.stringify(config));
          savedStatus = '📥 Config loaded';
        } catch (err) {
          savedStatus = '❌ Invalid config file';
        }
      };
      reader.readAsText(file);
    }

    function paramCategory(key) {
      const map = {
        temperature: 'Creativity & Style',
        top_p: 'Creativity & Style',
        response_style: 'Creativity & Style',
        top_k: 'Repetition & Diversity',
        presence_penalty: 'Repetition & Diversity',
        frequency_penalty: 'Repetition & Diversity',
        max_tokens: 'Length & Structure',
        stop_sequence: 'Length & Structure'
      };
      return map[key] || '';
    }

</script>

<style>
    .param-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .help-icon-wrapper {
      position: relative;
      display: inline-block;
    }

    .help-icon {
      font-size: 0.9rem;
      cursor: help;
      color: #666;
    }

    .tooltip-card {
      position: absolute;
      top: 100%;
      left: 0;
      transform: translateY(0.5rem);
      background: white;
      border: 1px solid #ccc;
      border-radius: 8px;
      padding: 0.75rem;
      font-size: 0.8rem;
      line-height: 1.3;
      width: 240px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.2s ease;
      z-index: 999;
    }

    .help-icon-wrapper:hover .tooltip-card {
      opacity: 1;
      pointer-events: auto;
    }

    .reset-btn {
      margin-top: 0.5rem;
      font-size: 0.75rem;
      background: transparent;
      border: none;
      color: #007acc;
      cursor: pointer;
      padding: 0;
    }

    .reset-btn:hover {
      text-decoration: underline;
    }

    .dynamic-desc {
      font-size: 0.8rem;
      color: #555;
      margin-top: 0.25rem;
    }
    .preset-buttons {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .preset-buttons button {
        padding: 0.5rem 1rem;
        background: #efefef;
        border: 1px solid #ccc;
        border-radius: 6px;
        cursor: pointer;
        transition: background 0.2s ease;
    }

    .preset-buttons button:hover {
        background: #ddd;
    }

    .slider-labels {
        display: flex;
        justify-content: space-between;
        font-size: 0.8rem;
        color: #555;
        margin-bottom: 0.25rem;
    }

    .param-control input[type="range"] {
        width: 100%;
        appearance: none;
        height: 6px;
        border-radius: 4px;
        /* background is set inline for color-coding */
    }

    .param-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-top: 1.5rem;
    }

    @media (max-width: 1000px) {
        .param-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    @media (max-width: 600px) {
        .param-grid {
            grid-template-columns: 1fr;
        }
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

    .param-control {
        margin: 1rem 0;
    }

    .param-control input[type="number"] {
        width: 100%;
        padding: 0.4rem;
        font-size: 0.9rem;
        border-radius: 4px;
        border: 1px solid #ccc;
        margin-top: 0.25rem;
    }

    .param-control input[type="text"] {
        width: 100%;
        padding: 0.4rem;
        font-size: 0.9rem;
        border-radius: 4px;
        border: 1px solid #ccc;
        margin-top: 0.25rem;
    }

    .param-control select {
        width: 100%;
        padding: 0.4rem;
        font-size: 0.9rem;
        border-radius: 4px;
        border: 1px solid #ccc;
        margin-top: 0.25rem;
        background: white;
    }

    .param-label {
        display: inline-block;
        font-weight: 600;
        font-size: 0.9rem;
    }

    .param-value {
        float: right;
        font-size: 0.85rem;
        color: #444;
    }

    .performance-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1rem;
        font-size: 0.9rem;
    }

    .performance-table th, .performance-table td {
        border: 1px solid #ccc;
        padding: 0.5rem;
    }

    .performance-table th {
        background: #f0f0f0;
        text-align: left;
    }

    .performance-table td:nth-child(2) {
        font-family: system-ui, sans-serif;
        font-size: 1.1rem;
    }

    .bar-bg {
        height: 12px;
        width: 100%;
        background: #eee;
        border-radius: 4px;
        overflow: hidden;
    }

    .bar-fill {
        height: 100%;
        background: #4caf50;
        transition: width 0.2s ease;
    }

    .eli5-list {
        margin-top: 1rem;
        font-size: 0.9rem;
        line-height: 1.4;
        padding-left: 1.25rem;
    }

    .eli5-list li {
        margin-bottom: 0.5rem;
    }

    .eli5-list li {
        margin-bottom: 0.5rem;
    }

    .section-title {
        margin-top: 2rem;
        font-size: 1.1rem;
        font-weight: 600;
    }

.param-category {
  font-size: 0.75rem;
  color: #888;
  font-style: italic;
  margin-top: -0.25rem;
  margin-bottom: 0.25rem;
}


</style>

