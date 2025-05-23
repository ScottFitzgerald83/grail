export const roadmapMarkdown = `
| Phase | Priority | Impact | Complexity | Task Description                                      | Filename / Location                                  |
|-------|----------|--------|------------|------------------------------------------------------|------------------------------------------------------|
| 2 – Full Training  | 🧪 P2    | ✅      | 🟡 Medium    | Launch full training via train_runner.py           | backend/train_runner.py                              |
| 3 – Fine-Tune UX   | ⚠️ P1    | 🔥      | 🟡 Medium    | Launch job and save config to runs/                | backend/train_runner.py                              |
| 5 – Iteration      | 🧪 P3    | ✅      | 🔴 Complex   | Save all configs + results with notes                | backend/session.py, frontend/routes/logs             |
| 5 – Iteration      | 🧪 P3    | ✅      | 🟡 Medium    | Link Codex → Forge (Send optimized prompt)           | frontend/routes/codex, frontend/routes/forge           |
| 6 – Export & Deploy| 🧠 P4    | 🌱      | 🟡 Medium    | Export model + config for Hugging Face or Ollama     | frontend/routes/forge, backend/train_runner.py         |
| 6 – Export & Deploy| 🧠 P4    | 🌱      | 🟡 Medium    | Auto-generate README from config                     | backend/train_runner.py                              |
`;