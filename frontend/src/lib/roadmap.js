export const roadmapMarkdown = `
| Priority | Description                               | Filename                              |
|----------|-------------------------------------------|---------------------------------------|
| 🚩 P0    | Config routing + translation              | backend/config/settings.py            |
| ⚠️ P1    | Cost/token tracking in memory save        | backend/engine/memory.py              |
| ⚠️ P1    | Structured session file I/O               | backend/engine/memory.py              |
| ⚠️ P1    | API key validation logic                  | backend/lib/secrets.py                |
| ⚠️ P1    | Request logging framework                 | backend/log.py                        |
| ⚠️ P1    | Per-API key usage logging                 | backend/log.py                        |
| 🍀 P2    | Tokenizer validation endpoint             | backend/main.py                       |
| 🍀 P2    | Prompt evaluation scoring                 | backend/eval/metrics.py               |
| 🍀 P2    | Prompt evaluation integration             | frontend/routes/compare/+page.svelte  |
| 🍀 P2    | Model fallback status indicator           | frontend/routes/compare/+page.svelte  |
| 🍀 P2    | Prompt truncation UI control              | frontend/routes/tuning/+page.svelte   |
| 🍀 P2    | Tuning config export formatting           | frontend/routes/tuning/+page.svelte   |
| 🍀 P2    | API key test button (live validation)     | frontend/routes/tuning/+page.svelte   |
| 🍀 P2    | Persist OpenAI key (opt-in)               | frontend/routes/tuning/+page.svelte   |
| 🍀 P2    | Training tab layout + config YAML preview | frontend/routes/training/+page.svelte |
| 🍀 P2    | Dataset import (CSV/JSON/Chat)            | frontend/routes/training/+page.svelte |
| 🍀 P2    | Launch trainer via CLI or Colab           | frontend/routes/training/+page.svelte |
| 🍬 P3    | Shareable compare URL preview             | frontend/routes/compare/+page.svelte  |
| 🍬 P3    | Toast after copy/export                   | frontend/routes/compare/+page.svelte  |
| 🍬 P3    | Output diff highlight                     | frontend/routes/compare/+page.svelte  |
| 🍬 P3    | Visual layout toggle                      | frontend/routes/compare/+page.svelte  |
| 🍬 P3    | Model feature badges                      | frontend/routes/compare/+page.svelte  |

`;