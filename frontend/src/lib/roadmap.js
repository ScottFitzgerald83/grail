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
    ],
    P1: [
        {
            title: "Streaming responses",
            detail: "Character-by-character reply display like ChatGPT.",
        },
        {
            title: "Typing indicator",
            detail: "Show loading dots while assistant is 'thinking'.",
        },
        {
            title: "Persistent memory",
            detail: "Store chat in localStorage or backend.",
        },
    ]
};