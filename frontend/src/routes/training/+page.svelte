<script>
  import { onMount } from 'svelte';
  import yaml from 'js-yaml';

  let dataset = null;
  let datasetPreview = '';
  let baseModel = 'mistral-7b';
  let adapterType = 'lora';
  let epochs = 3;
  let learningRate = 2e-5;
  let outputYaml = '';
  let logs = '';

  function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      datasetPreview = e.target.result.slice(0, 1000);
      dataset = e.target.result;
    };
    reader.readAsText(file);
  }

  function generateYaml() {
    const config = {
      base_model: baseModel,
      adapter: adapterType,
      epochs,
      learning_rate: learningRate,
      dataset_path: 'uploaded_dataset.json',
      output_dir: 'trained_model'
    };
    outputYaml = yaml.dump(config);
  }

  function launchTraining() {
    logs = '🚀 Training started...\n';
    setTimeout(() => {
      logs += '✅ Training completed (mock).\nModel saved to /trained_model/';
    }, 1500);
  }

  onMount(() => {
    generateYaml();
  });
</script>

<style src="/src/app.css"></style>
<h1>🧪 Model Training</h1>

<section>
  <h2>1. Upload Dataset</h2>
  <input type="file" accept=".json,.csv" on:change={handleFileUpload} />
  {#if datasetPreview}
    <p><strong>Preview:</strong></p>
    <pre style="max-height: 200px; overflow-y: auto;">{datasetPreview}</pre>
  {/if}
</section>

<section>
  <h2>2. Configure Training</h2>
  <label>Base Model:
    <select bind:value={baseModel}>
      <option value="mistral-7b">Mistral 7B</option>
      <option value="llama-2-7b">LLaMA 2 7B</option>
    </select>
  </label>

  <label>Adapter Type:
    <select bind:value={adapterType}>
      <option value="lora">LoRA</option>
      <option value="qlora">QLoRA</option>
    </select>
  </label>

  <label>Epochs:
    <input type="number" bind:value={epochs} min="1" max="50" />
  </label>

  <label>Learning Rate:
    <input type="number" step="0.00001" bind:value={learningRate} />
  </label>
</section>

<section>
  <h2>3. Preview Config</h2>
  <button on:click={generateYaml}>🔄 Refresh</button>
  <pre style="background: #f0f0f0; padding: 1rem; max-height: 300px; overflow-y: auto;">
{outputYaml}
  </pre>
</section>

<section>
  <h2>4. Launch</h2>
  <button on:click={launchTraining}>🚀 Start Training</button>
  {#if logs}
    <pre style="background: #111; color: #0f0; padding: 1rem;">{logs}</pre>
  {/if}
</section>