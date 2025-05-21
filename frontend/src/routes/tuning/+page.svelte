<h1>🎛️ Model Tuning</h1>


<div class="dashboard-container">
    <div class="param-grid">
        {#each [...parameters]
            .filter(p =>
                !['Advanced', 'Output Format', 'Tool Use'].includes(paramCategory(p.key))
            )
            .sort((a, b) => {
                const ca = paramCategory(a.key);
                const cb = paramCategory(b.key);
                return ca === cb ? a.key.localeCompare(b.key) : ca.localeCompare(cb);
            }) as param}
            {#if param.key === 'use_public_model'}
                <div class="param-tile" data-category={paramCategory(param.key)}>
                    <div class="param-header">
                        <strong>{param.key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</strong>
                        <span class="help-icon-wrapper">
                            <span class="help-icon">❓</span>
                            <div class="tooltip-card">{param.eli5}</div>
                        </span>
                    </div>
                    <p class="param-category">{paramCategory(param.key)}</p>
                    <p class="param-description">{param.definition}</p>
                    <div class="param-control">
                        <select bind:value={config.use_public_model}
                                on:change={(e) => updateConfig('use_public_model', e.target.value)}>
                            <option value="false">Off</option>
                            <option value="true">On</option>
                        </select>
                        {#if config.use_public_model === 'true'}
                            <label style="margin-top: 0.75rem;">
                                <span style="font-weight: 500; font-size: 0.85rem;">Select Public Model</span>
                                <select bind:value={config.public_model_name}
                                        on:change={(e) => updateConfig('public_model_name', e.target.value)}
                                        style="margin-top: 0.25rem;">
                                    <option value="gpt-4">GPT-4</option>
                                    <option value="gpt-3.5">GPT-3.5</option>
                                    <option value="ollama:llama2">Ollama: LLaMA 2</option>
                                    <option value="ollama:mistral">Ollama: Mistral</option>
                                    <option value="mixtral">Mixtral</option>
                                </select>
                            </label>
                        {/if}
                        <button class="reset-btn" on:click={() => {
                            updateConfig('use_public_model', getDefault('use_public_model'));
                            updateConfig('public_model_name', getDefault('public_model_name'));
                        }}>
                            Reset
                        </button>
                        <p class="dynamic-desc">{config.use_public_model === 'true'
                            ? `Using ${config.public_model_name}`
                            : 'Local model active'}
                        </p>
                    </div>
                </div>
            {:else if param.key !== 'public_model_name'}
                <div class="param-tile" data-category={paramCategory(param.key)}>
                    <div class="param-header">
                        <strong>{param.key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</strong>
                        <span class="help-icon-wrapper">
                            <span class="help-icon">❓</span>
                            <div class="tooltip-card">
                                {param.eli5}
                            </div>
                        </span>
                    </div>
                    <p class="param-category">{paramCategory(param.key)}</p>
                    <p class="param-description">{param.definition}</p>
                    <div class="param-control">
                        <label>
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
            {/if}
        {/each}
    </div>

    <details style="margin-top: 2rem;">
        <summary style="cursor: pointer; font-weight: 600; font-size: 1rem;">
            ⚙️ Advanced Settings
        </summary>

        <div class="param-grid" style="margin-top: 1rem;">
            {#each [...parameters].filter(p =>
                ['Advanced', 'Output Format', 'Tool Use'].includes(paramCategory(p.key))
            ).sort((a, b) => a.key.localeCompare(b.key)) as param}
                <div class="param-tile" data-category={paramCategory(param.key)}>
                    <div class="param-header">
                        <strong>{param.key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</strong>
                        <span class="help-icon-wrapper">
              <span class="help-icon">❓</span>
              <div class="tooltip-card">
                {param.eli5}
              </div>
            </span>
                    </div>
                    <p class="param-category">{paramCategory(param.key)}</p>
                    <p class="param-description">{param.definition}</p>
                    <div class="param-control">
                        <label>
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
    </details>
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
    <input type="file" accept=".json" on:change={importConfig}/>
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
            logit_bias: '',
            sampling_seed: '',
            stop_tokens: '',
            model_name: 'gpt-4',
            system_prompt: '',
            tools_enabled: 'false',
            json_mode: 'false',
            truncate_prompt: 0,
            stream: 'false',
            use_public_model: 'false',
            public_model_name: 'gpt-4',
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
        logit_bias: '',
        sampling_seed: '',
        stop_tokens: '',
        model_name: 'gpt-4',
        system_prompt: '',
        tools_enabled: 'false',
        json_mode: 'false',
        truncate_prompt: 0,
        stream: 'false',
        use_public_model: 'false',
        public_model_name: 'gpt-4',
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
            logit_bias: '',
            sampling_seed: '',
            stop_tokens: '',
            model_name: 'gpt-4',
            system_prompt: '',
            tools_enabled: 'false',
            json_mode: 'false',
            truncate_prompt: 0,
            stream: 'false',
            use_public_model: 'false',
            public_model_name: 'gpt-4',
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
        eli5: `Controls how "creative" or "risky" the model is with its wording.
Lower values make answers steady and predictable.
Higher values increase variety but may lead to off-topic or wild responses.`,
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
        eli5: `Controls how many of the model's top word choices it considers at each step.
Small values make it stick to the most likely next words.
Larger values allow more options, increasing randomness and diversity.`,
        type: 'number',
        min: 0,
        max: 100,
        step: 1
      },
      {
        key: 'top_p',
        label: 'Top-P',
        definition: 'Limits sampling to top P probability mass. Lower = less variation.',
        eli5: `Selects tokens based on cumulative probability mass.
Lower values make output more focused.
Higher values allow the model to consider more diverse options.`,
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
        eli5: `This sets how long the reply can be.
Shorter values limit verbosity.
Longer values allow more detail, but may be slower or cost more.`,
        type: 'number',
        min: 16,
        max: 2048,
        step: 1
      },
      {
        key: 'presence_penalty',
        label: 'How much should it avoid repeating ideas?',
        definition: 'Encourages introducing new topics and discourages repetition.',
        eli5: `Discourages talking about the same topics repeatedly.
Higher values push novelty.
Lower values let the model stay focused on one topic.`,
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
        eli5: `Discourages repeating exact words.
Helps avoid stuttering or loops.
Higher values produce more diverse phrasing.`,
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
        eli5: `This tells the model to stop replying when it sees a certain phrase.
It helps enforce boundaries in structured outputs.`,
        type: 'text'
      },
      {
        key: 'system_prompt',
        label: 'System Prompt',
        definition: 'Custom instruction given before any user input.',
        eli5: `This sets the tone and behavior of the assistant.
It's like a backstage cue for the model to act a certain way.`,
        type: 'text'
      },
      {
        key: 'truncate_prompt',
        label: 'Prompt Truncation Limit',
        definition: 'If the prompt exceeds this many tokens, truncate older messages.',
        eli5: `Helps manage long chat history by dropping old messages.
Keeps token count under control.`,
        type: 'number',
        min: 0,
        max: 8192,
        step: 1
      },
      {
        key: 'use_public_model',
        label: 'Use Public Model?',
        definition: 'Enable this to override local settings with a public model like GPT-4.',
        eli5: `Turn this on to test your prompt with a known hosted model.
Leave it off to use your local configuration.`,
        type: 'select',
        options: ['false', 'true']
      },
      {
        key: 'public_model_name',
        label: 'Select Public Model',
        definition: 'Choose the public model to use when enabled.',
        eli5: `Pick a specific model like GPT-4 or Mistral to run your prompt on.
Useful for benchmarking or testing responses.`,
        type: 'select',
        options: ['gpt-4', 'gpt-3.5', 'ollama:llama2', 'ollama:mistral', 'mixtral']
      },
      {
        key: 'tools_enabled',
        label: 'Enable Tools',
        definition: 'Allow access to tools, functions, or APIs during generation.',
        eli5: `Lets the model call tools like calculators or plugins if available.
Useful for extending its capabilities beyond text generation.`,
        type: 'select',
        options: ['false', 'true']
      },
      {
        key: 'json_mode',
        label: 'Force JSON',
        definition: 'Model must return a valid JSON object.',
        eli5: `Instructs the model to respond only with JSON-formatted output.
Best for structured applications.`,
        type: 'select',
        options: ['false', 'true']
      },
      {
        key: 'stream',
        label: 'Stream Response',
        definition: 'Send back results as the model writes them.',
        eli5: `Streams the output live so users can see it as it generates.
Feels more responsive and interactive.`,
        type: 'select',
        options: ['false', 'true']
      },
      {
        key: 'logit_bias',
        label: 'Logit Bias',
        definition: 'Overrides probability of specific tokens.',
        eli5: `Advanced control that lets you nudge the model to avoid or prefer specific words.
Requires token-level knowledge.`,
        type: 'text'
      },
      {
        key: 'sampling_seed',
        label: 'Sampling Seed',
        definition: 'Fixes randomness for consistent output.',
        eli5: `Using a fixed seed makes responses repeatable.
Great for testing or debugging.`,
        type: 'number',
        min: 0,
        max: 999999,
        step: 1
      },
      {
        key: 'stop_tokens',
        label: 'Stop Tokens',
        definition: 'Stops generation when one of these strings appears.',
        eli5: `Lets you define multiple phrases that cut off generation.
Useful for strict response limits.`,
        type: 'text'
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
        const blob = new Blob([JSON.stringify(config, null, 2)], {type: 'application/json'});
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
                config = {...config, ...newConfig};
                localStorage.setItem('grailConfig', JSON.stringify(config));
                savedStatus = '📥 Config loaded';
            } catch (err) {
                savedStatus = '❌ Invalid config file';
            }
        };
        reader.readAsText(file);
    }

    // Returns a category label for each parameter key
    function paramCategory(key) {
        const map = {
            // Creativity & Style
            temperature: 'Creativity & Style',
            top_p: 'Creativity & Style',
            model_name: 'Creativity & Style',

            // Repetition & Diversity
            top_k: 'Repetition & Diversity',
            presence_penalty: 'Repetition & Diversity',
            frequency_penalty: 'Repetition & Diversity',

            // Length & Structure
            max_tokens: 'Length & Structure',
            stop_sequence: 'Length & Structure',
            truncate_prompt: 'Length & Structure',

            // Prompt Control
            system_prompt: 'Prompt Control',

            // Tool Use
            tools_enabled: 'Tool Use',

            // Advanced
            logit_bias: 'Advanced',
            sampling_seed: 'Advanced',
            stop_tokens: 'Advanced',

            // Output Format
            json_mode: 'Output Format',
            stream: 'Output Format'
        };
        return map[key] || 'General';
    }

</script>

<style>
    body {
        background: #f4f7fb;
    }

    .dashboard-container {
        background: #eef3f9;
        min-height: 100vh;
        padding-bottom: 2rem;
    }

    h1 {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #2a3b4c;
    }

    .param-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.25rem;
    }

    .param-header strong {
        font-size: 1.1rem;
        color: #2a3b4c;
        font-weight: 700;
    }

    .help-icon-wrapper {
        position: relative;
        display: inline-block;
    }

    .help-icon {
        font-size: 0.9rem;
        cursor: help;
        color: #007acc;
        transition: color 0.2s;
    }

    .help-icon-wrapper:hover .help-icon {
        color: #005c99;
    }

    .tooltip-card {
        position: absolute;
        top: 100%;
        left: 0;
        transform: translateY(0.5rem);
        width: 280px;
        background: #ffffff;
        color: #333;
        border: 1px solid #ccd5e0;
        font-size: 0.85rem;
        padding: 0.75rem 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        line-height: 1.4;
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
        transition: color 0.2s;
    }

    .reset-btn:hover {
        text-decoration: underline;
        color: #005c99;
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
        background: #ffffff;
        border: 1px solid #cfd8e3;
        border-radius: 8px;
        padding: 0.5rem 1.25rem;
        font-size: 0.9rem;
        color: #2a3b4c;
        cursor: pointer;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
        transition: all 0.2s ease;
    }

    .preset-buttons button:hover {
        background: #e8f2fc;
        border-color: #007acc;
        color: #007acc;
    }

    .slider-labels {
        display: flex;
        justify-content: space-between;
        font-size: 0.8rem;
        color: #555;
        margin-bottom: 0.4rem;
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
        background: #ffffff;
        border: 1px solid #dde4ea;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .param-tile[data-category='Creativity & Style'] {
        background: #e1f0ff;
    }

    .param-tile[data-category='Repetition & Diversity'] {
        background: #dffbe6;
    }

    .param-tile[data-category='Length & Structure'] {
        background: #fff4e5;
    }

    .param-tile[data-category='Prompt Control'] {
        background: #f5e9ff;
    }

    .param-tile[data-category='Tool Use'] {
        background: #e6f4ff;
    }

    .param-tile[data-category='Output Format'] {
        background: #fffbe6;
    }

    .param-tile[data-category='Advanced'] {
        background: #f0f1f3;
    }

    .param-tile:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.06);
        background: inherit;
    }

    .param-tile.active {
        border-color: #007acc;
        background: #e8f2fc;
    }

    .param-control {
        margin-top: 0.75rem;
        margin-bottom: 0.5rem;
    }

    .param-control input[type="range"],
    .param-control input[type="number"],
    .param-control input[type="text"],
    .param-control select {
        border-radius: 6px;
        border: 1px solid #cfd8e3;
        font-size: 0.9rem;
        padding: 0.45rem;
        transition: border-color 0.2s ease;
        width: 100%;
        margin-top: 0.25rem;
        background: #ffffff;
        box-sizing: border-box;
    }

    .param-control input:focus,
    .param-control select:focus {
        border-color: #007acc;
        outline: none;
    }

    .param-label {
        display: inline-block;
        font-weight: 600;
        font-size: 0.9rem;
    }

    .param-value {
        float: right;
        font-size: 0.8rem;
        color: #444;
        margin-left: 0.5rem;
    }

    .performance-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1rem;
        font-size: 0.9rem;
        background: #ffffff;
        border-radius: 10px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
        overflow: hidden;
    }

    .performance-table th, .performance-table td {
        border: 1px solid #dde4ea;
        padding: 0.5rem;
    }

    .performance-table th {
        background: #f4f7fb;
        text-align: left;
        color: #2a3b4c;
    }

    .performance-table td:nth-child(2) {
        font-family: system-ui, sans-serif;
        font-size: 1.1rem;
    }

    .bar-bg {
        height: 12px;
        width: 100%;
        background: #eaf0f7;
        border-radius: 4px;
        overflow: hidden;
    }

    .bar-fill {
        height: 100%;
        background: #4caf50;
        transition: width 0.2s ease;
        border-radius: 4px;
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

    .param-description {
        font-size: 0.85rem;
        color: #333;
        margin-bottom: 0.5rem;
    }
</style>

