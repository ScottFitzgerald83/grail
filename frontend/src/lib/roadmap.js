export const roadmapMarkdown = `
| Priority | Task                             | Domain     | Difficulty | Description                                                                                           | Value                   |
|----------|----------------------------------|------------|------------|-------------------------------------------------------------------------------------------------------|-------------------------|
| 🚩P0     | Backend stability check          | Backend    | Medium     | Ensure \`/infer\` always returns valid JSON even on error.                                             | Reliability             |
| 🚩P0     | Handle blank or failed responses | Frontend   | Medium     | Show fallback or retry prompt when output fails.                                                      | User experience         |
| 🚩P0     | Deduplicate or debounce input    | Frontend   | Medium     | Prevent double submits from double-click or Enter + click.                                            | Usability               |
| 🚩P0     | Scroll-to-bottom reliability     | Frontend   | Low        | Ensure scrolling always snaps to newest message unless user has scrolled up.                          | Usability               |
| 🚩P0     | Prevent broken GET /infer nav    | Frontend   | Low        | Block accidental navigation to \`/infer\` as a page.                                                   | Reliability             |
| 🚩P0     | Persistent memory                | Backend    | Medium     | Store chat history per model in localStorage or backend file.                                         | State retention         |
| 🚩P0     | Retry failed messages            | Frontend   | Medium     | Let users retry failed sends.                                                                         | Resilience              |
| 🚩P0     | Auto-scroll control              | Frontend   | Medium     | Pause scroll when user is reviewing; show jump-to-bottom if new messages arrive.                      | UX polish               |
| 🚩P0     | Streaming response               | Backend    | Medium     | Stream assistant reply token-by-token in real time.                                                   | Real-time feedback      |
| 🚩P0     | Backend model router             | Backend    | Medium     | Route inference to different backends (e.g., GPT-4, Ollama).                                          | Extensibility           |
| 🚩P0     | Model tuning config passthrough  | Backend    | Medium     | Allow frontend config to pass through to model backends.                                              | Customization           |
| ⚠️P1     | Typing indicator                 | Frontend   | Low        | Show animated indicator while assistant is generating.                                                | Feedback loop           |
| ⚠️P1     | Multiline message input          | Frontend   | Low        | Allow users to type multi-line messages easily.                                                       | Usability               |
| ⚠️P1     | User personas                    | Frontend   | Medium     | Support system prompt injection for assistant personality presets.                                   | Tone control            |
| ⚠️P1     | Message editing                  | Frontend   | Medium     | Let users edit and resend their own messages.                                                         | Flexibility             |
| ⚠️P1     | Message deletion                 | Frontend   | Medium     | Let users remove messages from history.                                                               | Control                 |
| ⚠️P1     | Chat export (JSON/txt)           | Frontend   | Low        | Allow export of chat to file.                                                                         | Data portability        |
| ⚠️P1     | Compare config diff view         | Frontend   | Medium     | Highlight config differences in Compare tab.                                                          | Clarity                 |
| ⚠️P1     | Compare prompt A/B testing       | Backend    | Medium     | Run a prompt through two configs and return both outputs.                                             | Evaluation              |
| ⚠️P1     | Compare performance insight      | Frontend   | Medium     | Show token count, latency, entropy for each model run.                                                | Feedback                |
| ⚠️P1     | Config save/load/export          | Frontend   | Medium     | Allow users to save, load, and export tuning configs.                                                 | Efficiency              |
| ⚠️P1     | Dark mode support                | Frontend   | Low        | Provide toggle or auto-dark theme.                                                                    | Accessibility           |
| 🍀P2     | Multi-language support           | Frontend   | High       | Localize app UI and prompts.                                                                          | Internationalization    |
| 🍀P2     | User authentication              | Backend    | High       | Support login system if needed for future backend sync.                                               | Security                |
| 🍀P2     | Rate limiting                    | Backend    | Medium     | Add limits per user/session to prevent overload.                                                      | Abuse prevention        |
| 🍀P2     | Analytics dashboard              | Backend    | Medium     | Track usage metrics and user behavior (locally or securely).                                          | Insight                 |
| 🍀P2     | Plugin integrations              | Backend    | High       | Allow third-party plugins to extend app capabilities.                                                 | Extensibility           |
| 🍀P2     | Voice input                      | Frontend   | Medium     | Add speech-to-text message input.                                                                     | Accessibility           |
| 🍀P2     | Message reactions                | Frontend   | Low        | Add emoji-based reactions to assistant/user messages.                                                 | Engagement              |
| 🍀P2     | Offline mode                     | Frontend   | High       | Let users write and save messages offline, sync later.                                                | Mobility                |
| 🍀P2     | Prompt test suite                | Backend    | High       | Add framework to test a batch of prompts across configs/models.                                       | Reliability             |
| 🍀P2     | Chat comparison history          | Frontend   | Medium     | Show side-by-side chats from multiple models/configs.                                                 | Evaluation              |
`;