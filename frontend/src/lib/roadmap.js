export const roadmapMarkdown = `
| Priority | Task                             | Domain | File                                  |
|----------|----------------------------------|--------|---------------------------------------|
| ⚠️ P1     | Export filename personalization  | FE     | frontend/routes/compare/+page.svelte  |
| ⚠️ P1     | Dark mode contrast audit         | FE     | frontend/src/app.css                  |
| 🍀 P2     | Theme preference auto-detect     | FE     | frontend/routes/+layout.svelte        |
| 🍀 P2     | Markdown syntax highlighting     | FE     | frontend/src/app.css                  |
| 🍀 P2     | Persistent compare history       | FE     | frontend/routes/compare/+page.svelte  |
| 🍀 P2     | Tuning config export formatting  | FE     | frontend/routes/tuning/+page.svelte   |
| 🍀 P2     | Prompt truncation enforcement    | BE     | backend/engine/model.py               |
| 🍀 P2     | Model fallback routing           | BE     | backend/engine/remote.py              |
| 🍀 P2     | Prompt evaluation scoring        | BE     | backend/eval/metrics.py               |
| 🍬 P3     | Shareable compare URL preview    | FE     | frontend/routes/compare/+page.svelte  |
| 🍬 P3     | Config tag generation            | FE     | frontend/routes/tuning/+page.svelte   |
| 🍬 P3     | Glossary search bar              | FE     | frontend/routes/glossary/+page.svelte |
| 🍬 P3     | Toast after copy/export          | FE     | frontend/routes/compare/+page.svelte  |
`;