export const roadmapMarkdown = `
| Priority | Task                             | Domain    | Description                                                                                           | Value                   |
|----------|----------------------------------|-----------|-------------------------------------------------------------------------------------------------------|-------------------------|
| 🚩P0     | Scroll-to-bottom reliability     | FE        | Ensure scrolling always snaps to newest message unless user has scrolled up.                          | Usability               |
| 🚩P0     | Auto-scroll control              | FE        | Pause scroll when user is reviewing; show jump-to-bottom if new messages arrive.                      | UX polish               |
| 🚩P0     | Ensure consistent layout across themes | FE        | Guarantee all pages maintain layout consistency between light and dark mode, including spacing, alignment, and visibility. | Polish |
| ⚠️P1     | User personas                    | FE        | Support system prompt injection for assistant personality presets.                                     | Tone control            |
| ⚠️P1     | Message editing                  | FE        | Let users edit and resend their own messages.                                                         | Flexibility             |
| ⚠️P1     | Message deletion                 | FE        | Let users remove messages from history.                                                               | Control                 |
| ⚠️P1     | Chat message export              | FE        | Export chat history to file (txt, json, or markdown).                                                 | Data portability        |
| ⚠️P1     | Chat history UI                  | FE        | UI to view and restore previous chat sessions.                                                        | Productivity            |
| ⚠️P1     | Compare: retry run               | FE        | Allow users to retry a comparison run for failed or updated prompts.                                  | Efficiency              |
| ⚠️P1     | Compare: NL summary              | FE        | Provide natural language summary of comparison results.                                               | Insight                 |
| ⚠️P1     | Compare: Markdown sanitization         | FE        | Ensure all Markdown rendered on Compare tab is safely sanitized and styled.                            | Security/Clarity        |
| ⚠️P1     | Compare: consistent tile height        | FE        | Make result cards equal in height and align properly across screen sizes.                             | Visual clarity          |
| ⚠️P1     | Compare: markdown layout integrity     | FE        | Preserve Markdown layout for complex GPT replies.                                                     | UX polish               |
| ⚠️P1     | Tuning: dark mode support        | FE        | Provide toggle or auto-dark theme for tuning interface.                                               | Accessibility           |
| ⚠️P1     | Tuning: history restore          | FE        | Restore previous tuning sessions from history.                                                        | Productivity            |
| ⚠️P1     | Tuning: config presets           | FE        | Allow users to save and load config presets for quick tuning.                                         | Efficiency              |
| ⚠️P1     | Tuning: tooltip repositioning          | FE        | Prevent tooltips from cutting off or rendering outside tile bounds.                                   | Accessibility           |
| ⚠️P1     | Dark mode contrast audit               | FE        | Verify WCAG contrast ratios for all dark mode components.                                              | Accessibility           |
| ⚠️P1     | Theme sync across tabs                 | FE        | Ensure dark mode is consistent when navigating between tabs.                                           | Polish                  |
| ⚠️P1     | Layout baseline cleanup                | FE        | Remove all remaining page-level style overrides and consolidate into app.css                          | Maintainability         |
| ⚠️P1     | Scroll context memory                  | FE        | Preserve scroll position when switching between Chat and Compare tabs.                                | Productivity            |
| ⚠️P1     | Export filename personalization        | FE        | Include model names and timestamp in exported chat/compare files.                                     | Clarity/Traceability    |
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
| 🍀P2     | Compare: visual mode selector          | FE        | Allow toggle between basic and detailed views for Compare tab.                                        | UX refinement           |
| 🍀P2     | Theme preference auto-detect           | FE        | Match system theme by default on first load (light/dark).                                              | Personalization         |
| 🍀P2     | Markdown syntax highlighting           | FE        | Add syntax highlighting for code blocks inside model replies.                                         | Readability             |
| 🍀P2     | Mobile layout optimization             | FE        | Tune flex/grid layout for narrow viewports across all tabs.                                           | Responsiveness          |
`;