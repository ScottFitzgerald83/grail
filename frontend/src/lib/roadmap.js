export const roadmap = {
    P0: [
        {
            title: "Backend stability check",
            detail: "Ensure `/infer` always returns valid JSON even on error.",
        },
        {
            title: "Handle blank or failed responses",
            detail: "If backend output is null or malformed, show fallback error.",
        },
        {
            title: "Deduplicate or debounce input",
            detail: "Prevent double submits from double-click or fast Enter + click.",
        },
        {
            title: "Scroll-to-bottom reliability",
            detail: "Ensure scrolling always snaps to latest message.",
        },
        {
            title: "Prevent broken GET /infer nav",
            detail: "Block accidental browser navigation to `/infer` as a page.",
        },
        {
            title: "Persistent memory",
            detail: "Store chat in localStorage or backend.",
        },
        {
            title: "Retry failed messages",
            detail: "Let users retry sending a message that caused an error.",
        },
        {
            title: "Auto-scroll control",
            detail: "Disable auto-scroll if user scrolls up; show jump-to-bottom.",
        },
    ],
    P1: [
        {
            title: "Typing indicator",
            detail: "Show loading dots while assistant is 'thinking'.",
        },
        {
            title: "Auto-expanding textarea input",
            detail: "Replace single-line input with multi-line growing textarea.",
        },
        {
            title: "User personas",
            detail: "Support configurable styles like creative, precise, sarcastic.",
        },
    ]
};