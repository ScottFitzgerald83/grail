export const roadmapMarkdown = `
| Priority | Task                                      | Domain | File                                      |
|----------|-------------------------------------------|--------|-------------------------------------------|
| 🚩 P0     | Secure OpenAI key handling                | FE     | frontend/routes/tuning/+page.svelte       |
| 🚩 P0     | Validate presence of API key before infer | BE     | backend/main.py                           |
| ⚠️ P1     | API key setup field (OpenAI)              | FE     | frontend/routes/tuning/+page.svelte       |
| ⚠️ P1     | Prompt schema validation                  | BE     | backend/config/settings.py                |
| ⚠️ P1     | Max token cap enforcement per model       | BE     | backend/engine/model.py                   |
| ⚠️ P1     | Truncate chat history to fit context      | BE     | backend/main.py                           |
| ⚠️ P1     | Show warning if OpenAI key is missing     | FE     | frontend/routes/chat/+page.svelte         |
| ⚠️ P1     | Token/cost display for streamed output    | FE     | frontend/routes/chat/+page.svelte         |
| ⚠️ P1     | Return final stats from streamed outputs  | BE     | backend/main.py                           |
| 🍀 P2     | API key input and persistence (opt-in)    | FE     | frontend/routes/tuning/+page.svelte       |
| 🍀 P2     | Test API key button                       | FE     | frontend/routes/tuning/+page.svelte       |
| 🍀 P2     | Token preview before submission           | FE     | frontend/routes/chat/+page.svelte         |
| 🍀 P2     | Model pricing table (per-token cost)      | FE     | frontend/config/pricing.js                |
| 🍀 P2     | Prompt evaluation integration             | BE+FE  | backend/eval/metrics.py + compare/+page.svelte |
| 🍀 P2     | Model fallback status indicator           | FE     | frontend/routes/compare/+page.svelte      |
| 🍀 P2     | Training tab layout + config YAML preview | FE     | frontend/routes/training/+page.svelte     |
| 🍀 P2     | Dataset import (CSV/JSON/Chat)            | FE     | frontend/routes/training/+page.svelte     |
| 🍀 P2     | Launch trainer via CLI or Colab           | FE     | frontend/routes/training/+page.svelte     |
| 🍀 P2     | Tokenizer validation endpoint             | BE     | backend/main.py or new backend/token.py   |
| 🍬 P3     | Shareable compare URL preview             | FE     | frontend/routes/compare/+page.svelte      |
| 🍬 P3     | Config tag generation                     | FE     | frontend/routes/tuning/+page.svelte       |
| 🍬 P3     | Glossary search bar                       | FE     | frontend/routes/glossary/+page.svelte     |
| 🍬 P3     | Toast after copy/export                   | FE     | frontend/routes/compare/+page.svelte      |
`;