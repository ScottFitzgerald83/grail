export const roadmapMarkdown = `
| Priority | Task                             | Domain    | Description                                                                                           | Value                   |
|----------|----------------------------------|-----------|-------------------------------------------------------------------------------------------------------|-------------------------|
| 🚩P0     | Model execution wiring           | BE        | Connect to real models via Ollama, OpenAI, etc. Route based on config and handle authentication.     | Core functionality      |
| ⚠️P1     | Tuning: history restore          | FE        | Restore previous tuning sessions from history.                                                        | Productivity            |
| ⚠️P1     | Tuning: config presets           | FE        | Allow users to save and load config presets for quick tuning.                                         | Efficiency              |
| ⚠️P1     | Per-model config translation     | BE        | Normalize tuning fields across backends (e.g., Ollama vs OpenAI).                                     | Compatibility           |
| 🍀P2     | Dark mode contrast audit         | FE        | Verify WCAG contrast ratios for all dark mode components.                                              | Accessibility           |
| 🍀P2     | Scroll context memory            | FE        | Preserve scroll position when switching between Chat and Compare tabs.                                | Productivity            |
| 🍀P2     | Export filename personalization  | FE        | Include model names and timestamp in exported chat/compare files.                                     | Clarity/Traceability    |
| 🍀P2     | Multi-language support           | FE        | Localize app UI and prompts.                                                                          | Internationalization    |
| 🍀P2     | Voice input                      | FE        | Add speech-to-text message input.                                                                     | Accessibility           |
| 🍀P2     | Message reactions                | FE        | Add emoji-based reactions to assistant/user messages.                                                 | Engagement              |
| 🍀P2     | Offline mode                     | FE        | Let users write and save messages offline, sync later.                                                | Mobility                |
| 🍀P2     | User authentication              | BE        | Support login system if needed for future backend sync.                                               | Security                |
| 🍀P2     | Rate limiting                    | BE        | Add limits per user/session to prevent overload.                                                      | Abuse prevention        |
| 🍀P2     | Analytics dashboard              | BE        | Track usage metrics and user behavior (locally or securely).                                          | Insight                 |
| 🍀P2     | Plugin integrations              | BE        | Allow third-party plugins to extend app capabilities.                                                 | Extensibility           |
| 🍀P2     | Prompt test suite                | BE        | Framework to test batches of prompts and configs for regression and quality checks.                   | Reliability             |
| 🍀P2     | Chat comparison history          | BE        | Show side-by-side chats from multiple models/configs.                                                 | Evaluation              |
| 🍀P2     | Model fallback handler           | BE        | Automatically fallback to alternate model when preferred model fails or is unavailable.               | Robustness              |
| 🍀P2     | System prompt effectiveness eval | BE        | Measure how system prompt changes affect model behavior or metrics.                                   | Prompt quality          |
| 🍀P2     | Request metrics logging infra    | BE        | Collect latency, token usage, and errors for long-term insight.                                       | Observability           |
| 🍀P2     | Compare: visual mode selector    | FE        | Allow toggle between basic and detailed views for Compare tab.                                        | UX refinement           |
| 🍀P2     | Theme preference auto-detect     | FE        | Match system theme by default on first load (light/dark).                                              | Personalization         |
| 🍀P2     | Markdown syntax highlighting     | FE        | Add syntax highlighting for code blocks inside model replies.                                         | Readability             |
| 🍀P2     | Mobile layout optimization       | FE        | Tune flex/grid layout for narrow viewports across all tabs.                                           | Responsiveness          |
| 🍀P3     | Live shared comparison link      | FE        | Generate a shareable URL or QR to show compare results.                                               | Collaboration           |
| 🍀P3     | Compare run history              | FE        | Let user browse prior comparisons.                                                                    | Insight/recall          |
| 🍀P3     | Emoji summary summary            | FE        | TLDR visual summary of compare result (e.g., GPT-4 🐢💸 vs Mistral 🚀💬)                               | Delight / at-a-glance   |
| 🍀P3     | Prompt instruction formatting    | FE        | Render instructional system prompts with highlight or brackets.                                       | Clarity                 |
`;