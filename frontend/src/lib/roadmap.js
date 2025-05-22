export const roadmapMarkdown = `
| Priority | Description                                            | Filename / Location                                  |
|----------|--------------------------------------------------------|------------------------------------------------------|

| 🧪 P3    | CLI wizard to generate fine-tune configs               | cli/tune_wizard.py                                   |
| 🧪 P3    | Local training job runner (Python)                     | backend/train_runner.py                              |
| 💅 P3    | Theme + visual polish pass                             | frontend/app.css                                     |
| 💅 P3    | Responsive layout for mobile                           | frontend/routes/*                                    |
| 🧪 P4    | Online lab sandbox with GPU-in-browser option          | TBD (possibly Colab + iframe)                        |
| 🧪 P4    | Proxy handler for API key relay (optional)             | src/routes/api/relay.ts, hooks.server.ts (future)    |
| 🧪 P4    | Use API key in training preview calls (future)         | frontend/routes/lab, train_runner.py                 |
| 🧪 P4    | Use API key in CLI training tools (optional)           | cli/tune_wizard.py, backend/train_runner.py          |
`;