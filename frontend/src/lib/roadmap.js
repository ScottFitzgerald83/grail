export const roadmapMarkdown = `
| Priority | ROI | Description                                           | Filename / Location                                  |
|----------|-----|-------------------------------------------------------|------------------------------------------------------|
| ⚠️ P1    | 🔥  | Onboarding welcome screen with intro panels          | frontend/routes/welcome/+page.svelte                 |
| ⚠️ P1    | 🔥  | Track first-time visits with localStorage flag        | frontend/hooks.client.ts                             |
| ⚠️ P1    | 🔥  | Sticky compare/export/clear toolbar                   | frontend/routes/compare/+page.svelte                 |
| ⚠️ P1    | 🔥  | Improve layout toggle with icon and label             | frontend/routes/compare/+page.svelte                 |
| ⚠️ P1    | 🔥  | Add copy-to-clipboard per output                      | frontend/routes/compare/+page.svelte                 |
| ⚠️ P1    | 🔥  | Rename and tag sessions                               | frontend/routes/logs/+page.svelte                    |
| ⚠️ P1    | 🔥  | Restore-to-editor from session log                    | frontend/routes/logs/+page.svelte                    |
| 🧪 P2    | ✅  | Add emoji/thumb + comment feedback UI                 | frontend/routes/compare/+page.svelte, backend/eval.py|
| 🧪 P2    | ✅  | Tooltip help system in compare UI                     | frontend/routes/compare/+page.svelte                 |
| 🧪 P2    | ✅  | Launch Colab with injected config                     | frontend/routes/lab/+page.svelte                     |
| 🧪 P2    | ✅  | Token preview and cost estimate                       | frontend/routes/lab/+page.svelte                     |
| 🧪 P2    | ✅  | JSONL/chat schema validator                           | frontend/routes/lab/+page.svelte                     |
| 🧪 P2    | ✅  | Launch training job locally                           | frontend/routes/lab/+page.svelte, backend/train_runner.py |
| 🧪 P2    | ✅  | Delete/archive sessions                               | frontend/routes/logs/+page.svelte                    |
| 🧪 P2    | ✅  | Batch error/loading UX improvements                   | frontend/routes/compare/+page.svelte                 |
| 🧪 P3    | ✅  | CLI commands: compare, train, help                    | cli/main.py                                          |
| 🧪 P3    | ✅  | YAML presets for major providers                      | cli/tune_wizard.py                                   |
| 📊 P3    | ✅  | Feedback analytics dashboard                          | frontend/routes/feedback/+page.svelte, backend/eval.py |
| 🧠 P3    | ✅  | Prompt template library                               | frontend/routes/compare/+page.svelte, shared/templates.json |
| 💅 P3    | ✅  | Visual polish: spacing, alignment, headers            | frontend/app.css, compare/+page.svelte              |
| 💅 P3    | ✅  | Responsive layout optimization                        | frontend/routes/*                                    |
| 🧠 P4    | 🌱  | Multi-API key manager                                 | frontend/lib/apiKeyManager.ts                        |
| 🧠 P4    | 🌱  | Ollama model manager UI                               | frontend/routes/tuning/+page.svelte                  |
| 🧠 P4    | 🌱  | Proxy API key relay (optional)                        | src/routes/api/relay.ts, hooks.server.ts             |
| 🧠 P4    | 🌱  | Use API key in CLI + preview                          | cli/tune_wizard.py, train_runner.py                  |
| 🧠 P4    | 🌱  | In-browser GPU lab (Colab iframe or future runner)    | TBD                                                  |
| 🧠 P4    | 🌱  | Model metadata (latency, cost, source)                | frontend/routes/compare/+page.svelte                 |
`;