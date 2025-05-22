export const roadmapMarkdown = `
| Priority | Task                                      | Domain | File                                      |
|----------|-------------------------------------------|--------|-------------------------------------------|
| ⚠️ P1     | Max token cap enforcement per model       | BE     | backend/engine/model.py                   |
| ⚠️ P1     | Return final stats from streamed outputs  | BE     | backend/main.py                           |
| ⚠️ P1     | Return fallback vs. primary model info    | BE     | backend/engine/remote.py                  |
| 🍀 P2     | Model pricing table (per-token cost)      | FE     | frontend/config/pricing.js                |
| 🍀 P2     | Prompt evaluation integration             | BE+FE  | backend/eval/metrics.py + compare/+page.svelte |
| 🍀 P2     | Model fallback status indicator           | FE     | frontend/routes/compare/+page.svelte      |
| 🍀 P2     | Training tab layout + config YAML preview | FE     | frontend/routes/training/+page.svelte     |
| 🍀 P2     | Dataset import (CSV/JSON/Chat)            | FE     | frontend/routes/training/+page.svelte     |
| 🍀 P2     | Launch trainer via CLI or Colab           | FE     | frontend/routes/training/+page.svelte     |
| 🍀 P2     | Tokenizer validation endpoint             | BE     | backend/main.py or new backend/token.py   |
| 🍀 P2     | API key test button (live validation)     | FE     | frontend/routes/tuning/+page.svelte       |
| 🍀 P2     | Persist OpenAI key (opt-in)               | FE     | frontend/routes/tuning/+page.svelte       |
| 🍬 P3     | Shareable compare URL preview             | FE     | frontend/routes/compare/+page.svelte      |
| 🍬 P3     | Glossary search bar                       | FE     | frontend/routes/glossary/+page.svelte     |
| 🍬 P3     | Toast after copy/export                   | FE     | frontend/routes/compare/+page.svelte      |
| 🕒 P4     | Per-API key usage logging                 | BE     | backend/utils/log.py                      |
`;