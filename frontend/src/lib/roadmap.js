export const roadmapMarkdown = `
| Priority | Description                                            | Filename / Location                                  |
|----------|--------------------------------------------------------|------------------------------------------------------|
| ⚠️ P1    | Persist OpenAI API key and attach to all requests     | frontend/routes/tuning/+page.svelte, fetchWithKey    |
| ⚠️ P2    | Session management + export                            | backend/session.py, frontend/logs                    |
| 🍀 P2    | Prompt evaluation metrics + feedback loop              | backend/eval.py, frontend/compare/+page.svelte       |
| 🧪 P2    | User training lab scaffold                             | frontend/routes/lab, backend/train.py                |
| 🧪 P3    | CLI wizard to generate fine-tune configs               | cli/tune_wizard.py                                   |
| 🧪 P3    | Local training job runner (Python)                     | backend/train_runner.py                              |
| 🍬 P3    | Visual layout toggle (stacked vs side)                 | frontend/routes/compare/+page.svelte                 |
| 🍬 P3    | Shareable compare URL + export toast                   | frontend/routes/compare/+page.svelte                 |
| 🍬 P3    | Model feature badges                                   | frontend/routes/compare/+page.svelte                 |
| 💅 P3    | Theme + visual polish pass                             | frontend/app.css                                     |
| 💅 P3    | Responsive layout for mobile                           | frontend/routes/*                                    |
| 🧪 P4    | Online lab sandbox with GPU-in-browser option          | TBD (possibly Colab + iframe)                        |
| 🧪 P4    | Proxy handler for API key relay (optional)             | src/routes/api/relay.ts, hooks.server.ts (future)    |
| 🧪 P4    | Extend fetchWithKey use to compare page                | frontend/routes/compare/+page.svelte                 |
| 🧪 P4    | Use API key in training preview calls (future)         | frontend/routes/lab, train_runner.py                 |
| 🧪 P4    | Use API key in CLI training tools (optional)           | cli/tune_wizard.py, backend/train_runner.py          |
`;