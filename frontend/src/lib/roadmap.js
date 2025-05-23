export const roadmapMarkdown = `
| Phase | Priority | Impact | Complexity | Task Description                                      | Filename / Location                                  |
|-------|----------|--------|------------|------------------------------------------------------|------------------------------------------------------|
| 2 – Full Training  | 🧪 P2    | ✅      | 🟡 Medium    | Launch full training via train_runner.py           | backend/train_runner.py                              |
| 2 – Full Training  | 🧪 P2    | ✅      | 🟡 Medium    | Show training output log                             | frontend/routes/forge/+page.svelte                     |
| 3 – Fine-Tune UX   | ⚠️ P1    | 🔥      | 🟡 Medium    | Validate JSONL/Chat format + field structure         | frontend/routes/forge/+page.svelte                     |
| 3 – Fine-Tune UX   | ⚠️ P1    | 🔥      | 🟡 Medium    | Token + cost estimate                                | frontend/routes/forge/+page.svelte                     |
| 3 – Fine-Tune UX   | ⚠️ P1    | 🔥      | 🟢 Easy      | Generate + preview training YAML                     | frontend/routes/forge/+page.svelte                     |
| 3 – Fine-Tune UX   | ⚠️ P1    | 🔥      | 🟡 Medium    | Launch job and save config to runs/                | backend/train_runner.py                              |
| 4 – Evaluation     | 🧪 P3    | ✅      | 🟡 Medium    | Add Eval tab: run test prompts vs checkpoints        | frontend/routes/forge/+page.svelte                     |
| 4 – Evaluation     | 🧪 P3    | ✅      | 🟡 Medium    | Show metrics (diversity, task accuracy, etc.)        | backend/eval.py, frontend/routes/forge/+page.svelte    |
| 5 – Iteration      | 🧪 P3    | ✅      | 🔴 Complex   | Save all configs + results with notes                | backend/session.py, frontend/routes/logs             |
| 5 – Iteration      | 🧪 P3    | ✅      | 🟡 Medium    | Allow “Fork config” and diff between runs            | frontend/routes/forge/+page.svelte                     |
| 5 – Iteration      | 🧪 P3    | ✅      | 🟡 Medium    | Link Codex → Forge (Send optimized prompt)           | frontend/routes/codex, frontend/routes/forge           |
| 6 – Export & Deploy| 🧠 P4    | 🌱      | 🟡 Medium    | Export model + config for Hugging Face or Ollama     | frontend/routes/forge, backend/train_runner.py         |
| 6 – Export & Deploy| 🧠 P4    | 🌱      | 🟡 Medium    | Auto-generate README from config                     | backend/train_runner.py                              |
| 7 – Learn Mode     | 🧠 P4    | 🌱      | 🟢 Easy      | Add inline “explain this setting” toggles            | frontend/routes/forge/+page.svelte                     |
| 7 – Learn Mode     | 🧠 P4    | 🌱      | 🟡 Medium    | Add LLM tips, best practices, and external links     | frontend/routes/forge/+page.svelte                     |
`;