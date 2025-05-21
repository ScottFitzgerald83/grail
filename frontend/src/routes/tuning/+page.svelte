<h1>🎛️ Model Tuning</h1>
<p>Controls for model architecture and generation settings will live here.</p>

<script>
    let config = {
        temperature: 0.7,
        top_k: 50,
        top_p: 0.9,
        max_tokens: 256
    };

    function save() {
        localStorage.setItem('grailConfig', JSON.stringify(config));
    }

    function reset() {
        config = {
            temperature: 0.7,
            top_k: 50,
            top_p: 0.9,
            max_tokens: 256
        };
    }
</script>

<h1>🎛️ Tuning</h1>

<form on:submit|preventDefault={save}>
    <label>Temperature: <input type="range" min="0" max="1.5" step="0.05" bind:value={config.temperature} /></label>
    <label>Top-K: <input type="number" min="0" max="100" bind:value={config.top_k} /></label>
    <label>Top-P: <input type="range" min="0" max="1" step="0.01" bind:value={config.top_p} /></label>
    <label>Max Tokens: <input type="number" min="16" max="2048" bind:value={config.max_tokens} /></label>

    <button type="submit">💾 Save Config</button>
    <button type="button" on:click={reset}>↩️ Reset</button>
</form>