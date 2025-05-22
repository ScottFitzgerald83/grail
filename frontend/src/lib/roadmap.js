export const roadmapMarkdown = `
| Priority | Task                                         | Domain | File                                      |
|----------|----------------------------------------------|--------|-------------------------------------------|
| 🚩 P0     | Model execution wiring                       | BE     | backend/engine/remote.py                  |
| 🚩 P0     | Config routing + translation                 | BE     | backend/config/settings.py                |
| 🚩 P0     | Return fallback vs. primary model info       | BE     | backend/engine/remote.py                  |
| 🚩 P0     | Chat pipeline (send/edit/delete)             | FE     | frontend/routes/chat/+page.svelte         |
| ⚠️ P1     | API key validation logic                     | BE     | backend/lib/secrets.py                    |
| ⚠️ P1     | Show warning if OpenAI key is missing        | FE     | frontend/routes/chat/+page.svelte         |
| ⚠️ P1     | Streaming support for public models          | BE     | backend/engine/remote.py                  |
| ⚠️ P1     | Token/cost display for streamed output       | FE     | frontend/routes/chat/+page.svelte         |
| ⚠️ P1     | Token preview before submission              | FE     | frontend/routes/chat/+page.svelte         |
| ⚠️ P1     | Model fallback routing                       | BE     | backend/engine/remote.py                  |
| ⚠️ P1     | Cost/token tracking in memory save           | BE     | backend/engine/memory.py                  |
| ⚠️ P1     | Structured session file I/O                  | BE     | backend/engine/memory.py                  |
| ⚠️ P1     | Roadmap filtering, table view                | FE     | frontend/routes/roadmap/+page.svelte      |
| 🍀 P2     | Model pricing table (per-token cost)         | FE     | frontend/config/pricing.js                |
| 🍀 P2     | Prompt evaluation integration                | FE     | frontend/routes/compare/+page.svelte      |
| 🍀 P2     | Model fallback status indicator              | FE     | frontend/routes/compare/+page.svelte      |
| 🍀 P2     | Tokenizer validation endpoint                | BE     | backend/token.py                          |
| 🍀 P2     | Glossary search bar                          | FE     | frontend/routes/glossary/+page.svelte     |
| 🍀 P2     | Prompt truncation UI control                 | FE     | frontend/routes/tuning/+page.svelte       |
| 🍀 P2     | Tuning config export formatting              | FE     | frontend/routes/tuning/+page.svelte       |
| 🍀 P2     | API key test button (live validation)        | FE     | frontend/routes/tuning/+page.svelte       |
| 🍀 P2     | Persist OpenAI key (opt-in)                  | FE     | frontend/routes/tuning/+page.svelte       |
| 🍀 P2     | Training tab layout + config YAML preview    | FE     | frontend/routes/training/+page.svelte     |
| 🍀 P2     | Dataset import (CSV/JSON/Chat)               | FE     | frontend/routes/training/+page.svelte     |
| 🍀 P2     | Launch trainer via CLI or Colab              | FE     | frontend/routes/training/+page.svelte     |
| 🍬 P3     | Shareable compare URL preview                | FE     | frontend/routes/compare/+page.svelte      |
| 🍬 P3     | Toast after copy/export                      | FE     | frontend/routes/compare/+page.svelte      |
| 🍬 P3     | Output diff highlight                        | FE     | frontend/routes/compare/+page.svelte      |
| 🍬 P3     | Visual layout toggle                         | FE     | frontend/routes/compare/+page.svelte      |
| 🍬 P3     | Model feature badges                         | FE     | frontend/routes/compare/+page.svelte      |
| 🍬 P3     | Per-API key usage logging                    | BE     | backend/log.py                            |
`;