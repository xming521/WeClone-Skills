![download](https://github.com/user-attachments/assets/cd4a87c6-1649-4ce5-bce8-bd5b08b278de)

<h3 align="center">A skill set that helps your agent become your AI twin.</h3>

[中文说明](README.zh-CN.md)

`WeClone-Skill` turns a lightweight persona pack into a reusable prompt workflow for "AI twin" style drafting. The repository is intentionally split into two skills:

- `weclone-init-twin`: scaffold a persona pack with markdown templates.
- `weclone-twin-reply`: compile persona files plus runtime context into an isolated prompt for drafting replies.

The result is a pragmatic workflow: define the user's identity and boundaries once, inject only the current scene and dialogue at runtime, then review the draft before anything is sent.

## What This Repo Is For

This project is useful when you want an agent to draft in a specific person's voice without mixing long-term identity with short-term conversation state.

Typical use cases:

- Personal AI assistant that replies in a consistent tone
- Creator or social-media DM drafting
- Workplace email drafting with style and boundary control
- Sales follow-up scripting across HubSpot and WeCom
- Companion-style chat drafting for family or close friends
- Digital legacy persona preservation based on a deceased person's historical chats, writing, and voice material for memorial-style conversation
- Safe digital twin experiments where human review stays in the loop

## Workflow

### 1. Initialize a persona pack

Use `weclone-init-twin` to create a directory containing:

- `profile.md`: stable identity, values, worldview, decision style
- `state.md`: temporary status, goals, current constraints
- `persona_examples.md`: writing samples and behavioral evidence
- `guardrails.md`: hard limits, promises to avoid, privacy boundaries

### 2. Fill the pack with real content

The templates are only scaffolding. The quality of the downstream draft depends on whether these files contain high-signal, specific, real-world content instead of placeholders.

### 3. Add runtime context

For each drafting task, provide:

- `scene.md`: concise background that explains the situation
- `dialogue.md`: the active message window the reply must answer

### 4. Render an isolated prompt

Use `weclone-twin-reply` to combine persona files and runtime context into one prompt package. That rendered prompt is designed to be passed to a downstream model in isolation.

### 5. Review before sending

This repo is built around a review gate. It helps draft; it does not silently auto-send.

## Repository Layout

```text
.
├── skills/
│   ├── weclone-init-twin/
│   │   ├── SKILL.md
│   │   ├── scripts/init_twin_profile.py
│   │   └── assets/persona-pack/
│   └── weclone-twin-reply/
│       ├── SKILL.md
│       ├── scripts/render_clone_prompt.py
│       └── assets/clone_prompt_template.md
├── examples/
│   ├── zh/
│   └── en/
└── tests/
```

## Quick Start

### Initialize a new persona pack

Create the default `ai_twin/` directory in English:

```bash
python3 skills/weclone-init-twin/scripts/init_twin_profile.py --user-name "Alex"
```

Create a Chinese persona pack in a custom directory:

```bash
python3 skills/weclone-init-twin/scripts/init_twin_profile.py \
  --user-name "张三" \
  --language zh \
  ./my_twin
```

If the target files already exist, the script refuses to overwrite them unless you pass `--force`.

### Render a prompt from a persona pack

```bash
python3 skills/weclone-twin-reply/scripts/render_clone_prompt.py \
  --persona-dir ./ai_twin \
  --scene ./scene.md \
  --dialogue ./dialogue.md
```

Write the rendered prompt to a file:

```bash
python3 skills/weclone-twin-reply/scripts/render_clone_prompt.py \
  --persona-dir ./ai_twin \
  --scene ./scene.md \
  --dialogue ./dialogue.md \
  --output ./rendered_prompt.md
```

Add extra runtime context only when it materially changes the draft:

```bash
python3 skills/weclone-twin-reply/scripts/render_clone_prompt.py \
  --persona-dir ./ai_twin \
  --scene ./scene.md \
  --dialogue ./dialogue.md \
  --extra-context ./constraints.md
```

## Included Examples

The repository ships with bilingual examples under [examples/README.md](examples/README.md):

- `examples/zh/social-content-twitter-fan-dm`
- `examples/zh/workplace-email-draft`
- `examples/zh/sales-copy-hubspot-wecom`
- `examples/zh/companion-chat-whatsapp-qq`
- `examples/zh/digital-legacy-memorial-reply`
- `examples/en/social-content-twitter-fan-dm`
- `examples/en/workplace-email-draft`
- `examples/en/sales-copy-hubspot-wecom`
- `examples/en/companion-chat-whatsapp-qq`
- `examples/en/digital-legacy-memorial-reply`

Example render:

```bash
python3 skills/weclone-twin-reply/scripts/render_clone_prompt.py \
  --persona-dir examples/en/workplace-email-draft \
  --scene examples/en/workplace-email-draft/scene.md \
  --dialogue examples/en/workplace-email-draft/dialogue.md
```

## Design Principles

- Separate stable persona from live conversation context
- Keep prompt assembly explicit and inspectable
- Preserve hard behavioral boundaries in `guardrails.md`
- Bias toward minimal, high-signal runtime context
- Keep a human approval step before outbound sending

## Testing

Run the renderer tests with:

```bash
python3 -m unittest tests/test_render_clone_prompt.py
```

The tests cover:

- rendering persona files into the final template
- writing prompt output to disk
- verifying all bundled examples render successfully

## Notes

- `render_clone_prompt.py` requires `profile.md`, `persona_examples.md`, and `guardrails.md`
- `state.md` is optional but strongly recommended
- additional `*.md` files in the persona directory are appended automatically
- files used as `scene`, `dialogue`, or `extra-context` are excluded from persona auto-loading

## License

[MIT](LICENSE)
