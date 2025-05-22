export const roadmapMarkdown = `
| Priority | Task                                 | Domain | File                                  |
|----------|--------------------------------------|--------|---------------------------------------|
| 🚩 P0     | Request logging framework            | BE     | backend/utils/log.py                  |
| 🚩 P0     | Streaming support for public models  | BE     | backend/engine/remote.py              |
| 🚩 P0     | Cost/token tracking in memory save   | BE     | backend/main.py                       |
| ⚠️ P1     | Prompt schema validation             | BE     | backend/config/settings.py            |
| ⚠️ P1     | System prompt passthrough (remote)   | BE     | backend/engine/remote.py              |
| ⚠️ P1     | Structured session file I/O          | BE     | backend/main.py                       |
| 🍀 P2     | Tuning config export formatting      | FE     | frontend/routes/tuning/+page.svelte   |
| 🍀 P2     | Prompt evaluation integration         | FE     | frontend/routes/compare/+page.svelte  |
| 🍀 P2     | Prompt truncation UI control          | FE     | frontend/routes/tuning/+page.svelte   |
| 🍀 P2     | Model fallback status indicator       | FE     | frontend/routes/compare/+page.svelte  |
| 🍬 P3     | Shareable compare URL preview         | FE     | frontend/routes/compare/+page.svelte  |
| 🍬 P3     | Config tag generation                | FE     | frontend/routes/tuning/+page.svelte   |
| 🍬 P3     | Glossary search bar                  | FE     | frontend/routes/glossary/+page.svelte |
| 🍬 P3     | Toast after copy/export              | FE     | frontend/routes/compare/+page.svelte  |
`;