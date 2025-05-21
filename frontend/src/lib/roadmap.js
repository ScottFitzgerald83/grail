export const roadmapMarkdown = `
| Priority | Task                              | Domain    | Difficulty | Description                                                                                     | Value                  |
|----------|----------------------------------|-----------|------------|-------------------------------------------------------------------------------------------------|------------------------|
| 🚩P0       | Backend stability check          | Backend   | Medium     | Ensure \`/infer\` always returns valid JSON even on error.                                       | Reliability            |
| 🚩P0       | Handle blank or failed responses | Frontend  | Medium     | If assistant output is missing or fails, show graceful retry prompt. Applies to creative-style prompts. | User experience        |
| 🚩P0       | Deduplicate or debounce input    | Frontend  | Medium     | Prevent double submits from double-click or fast Enter + click.                                 | Usability              |
| 🚩P0       | Scroll-to-bottom reliability     | Frontend  | Low        | Ensure scrolling always snaps to latest message.                                                | Usability              |
| 🚩P0       | Prevent broken GET /infer nav    | Frontend  | Low        | Block accidental browser navigation to \`/infer\` as a page.                                    | Reliability            |
| 🚩P0       | Persistent memory                | Backend   | Medium     | Store chat in localStorage or backend.                                                          | Data persistence       |
| 🚩P0       | Retry failed messages            | Frontend  | Medium     | Let users retry sending a message that caused an error.                                         | User experience        |
| 🚩P0       | Auto-scroll control              | Frontend  | Medium     | Disable auto-scroll if user scrolls up; show jump-to-bottom.                                    | Usability              |
| ⚠️P1       | Typing indicator                 | Frontend  | Low        | Show loading dots while assistant is 'thinking'.                                                | User feedback          |
| ⚠️P1       | Auto-expanding textarea input   | Frontend  | Low        | Replace single-line input with multi-line growing textarea.                                     | Usability              |
| ⚠️P1       | User personas                   | Frontend  | Medium     | Support configurable styles like creative, precise, sarcastic.                                 | Customization          |
| ⚠️P1       | Message editing                 | Frontend  | Medium     | Allow users to edit previously sent messages.                                                  | Usability              |
| ⚠️P1       | Message deletion                | Frontend  | Medium     | Enable users to delete messages from the chat history.                                         | Usability              |
| ⚠️P1       | Conversation export             | Frontend  | Low        | Allow users to export chat history as text or JSON.                                            | Data portability       |
| ⚠️P1       | Dark mode support               | Frontend  | Low        | Provide a dark theme option for the interface.                                                 | User experience        |
| 🍀P2       | Multi-language support          | Frontend  | High       | Support interface localization in multiple languages.                                          | Accessibility          |
| 🍀P2       | User authentication            | Backend   | High       | Implement user login and authentication system.                                               | Security               |
| 🍀P2       | Rate limiting                  | Backend   | Medium     | Prevent abuse by limiting request rates per user.                                              | Security               |
| 🍀P2       | Analytics dashboard            | Backend   | Medium     | Provide usage statistics and metrics for admins.                                              | Monitoring             |
| 🍀P2       | Plugin integrations            | Backend   | High       | Support third-party plugin integrations for extended functionality.                            | Extensibility          |
| 🍀P2       | Voice input                   | Frontend  | Medium     | Allow users to input messages via speech-to-text.                                             | Accessibility          |
| 🍀P2       | Message reactions             | Frontend  | Low        | Enable users to react to messages with emojis.                                                | User engagement        |
| 🍀P2       | Offline mode                  | Frontend  | High       | Allow users to compose messages offline and sync later.                                       | Usability              |
`;