

<script>
let trainingFile = null;
let trainingPreview = '';
let yamlConfig = '';
let fileName = '';

function handleUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    fileName = file.name;

    const reader = new FileReader();
    reader.onload = (e) => {
        trainingPreview = e.target.result.split('\n').slice(0, 5).join('\n');
        yamlConfig = `training_file: ${file.name}\nepochs: 3\nlearning_rate: 2e-5`;
    };
    reader.readAsText(file);
}
</script>

<main>
  <h1>🧪 Training Lab</h1>

  <label>
    Upload dataset (.jsonl or .csv):
    <input type="file" accept=".jsonl,.csv" on:change={handleUpload} />
  </label>

  {#if fileName}
    <p><strong>File:</strong> {fileName}</p>
    <h3>🔍 File Preview:</h3>
    <pre>{trainingPreview}</pre>

    <h3>🛠️ Config Preview (YAML)</h3>
    <pre>{yamlConfig}</pre>
  {/if}
</main>