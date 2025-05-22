export const roadmapMarkdown = `
| Priority | Description                               | Filename                              |
|----------|-------------------------------------------|---------------------------------------|
| ⚠️ P1    | Prompt evaluation metrics + feedback loop | backend/eval.py, frontend/compare     |
| ⚠️ P1    | Session management + export               | backend/session.py, frontend/logs     |
| 🍀 P2    | Prompt truncation UI + controls           | frontend/routes/tuning/+page.svelte   |
| 🍀 P2    | API key live test + persistence           | frontend/routes/tuning/+page.svelte   |
| 🍀 P2    | Model fallback indicator                  | frontend/routes/compare/+page.svelte  |
| 🍀 P2    | Prompt diff + evaluation highlight        | frontend/routes/compare/+page.svelte  |
| 🍀 P2    | Training tab + config YAML preview        | frontend/routes/training/+page.svelte |
| 🍀 P2    | Dataset import (CSV/JSON/Chat)            | frontend/routes/training/+page.svelte |
| 🍀 P2    | Launch trainer via CLI or Colab           | frontend/routes/training/+page.svelte |
| 🍬 P3    | Visual layout toggle (stacked vs side)    | frontend/routes/compare/+page.svelte  |
| 🍬 P3    | Shareable compare URL + export toast      | frontend/routes/compare/+page.svelte  |
| 🍬 P3    | Model feature badges                      | frontend/routes/compare/+page.svelte  |
| 🧪 P2    | User training lab scaffold (UI + files)   | frontend/routes/lab, backend/train.py |
| 🧪 P3    | CLI wizard to generate fine-tune configs  | cli/tune_wizard.py                    |
| 🧪 P3    | Local training job runner (Python)        | backend/train_runner.py               |
| 💅 P3    | Theme + visual polish pass                | frontend/app.css                      |
| 💅 P3    | Responsive layout for mobile              | frontend/routes/*                     |
`;