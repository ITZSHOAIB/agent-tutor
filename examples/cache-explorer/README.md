# Example: What survives the cache

A visual page from a real module: "1.1 Messages become one long string", in a topic on how LLMs work, taught to an engineer who builds coding agents. It's the page the tutor made for one step: **the chat template puts tool definitions at the front of the sequence, so changing a tool breaks the prefix cache for everything after it.**

| File | What it is |
|---|---|
| `cache-explorer.data.py` | Renders a coding agent's request with the real Qwen2.5-0.5B-Instruct chat template and tokenizer, applies four edits, and measures how many tokens each edit leaves reusable |
| `cache-explorer.data.json` | The measured numbers |
| `cache-explorer.src.html` | The page, made from [`assets/visual.html`](../../skills/tutor/assets/visual.html) |
| `cache-explorer.html` | The built page (`--standalone`): open it in a browser |

What it shows the method doing:
- **Predict first.** The question and a confidence pick come before anything that gives the answer away; the edits and the reuse bar unlock after.
- **Wrong options carry their beliefs.** After locking, each wrong option says which mental model it came from.
- **Real numbers.** Nothing is typed in: append a message and 318 of 330 tokens are reused; add one tool and only 169 of 375 are; change one word of the system prompt and 17 of 321 are.
- **Answers come back.** "Copy for chat" puts a line like `1.1 cache explorer · predicted A · Fairly sure · wrong · tried: tool, system · noticed: …` on the clipboard for the learner to paste into the session.

"Like vLLM in Q3" in the question refers to an earlier question in the same session.

## Rebuild

```bash
uv run --with transformers --with jinja2 python cache-explorer.data.py cache-explorer.data.json   # downloads the tokenizer (a few MB)
python -I ../../skills/tutor/scripts/build_visual.py cache-explorer.src.html cache-explorer.data.json --standalone
```

Without `--standalone`, the output is the body-only form that hosts such as Claude Artifacts wrap themselves.
