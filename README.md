![download](https://github.com/user-attachments/assets/cd4a87c6-1649-4ce5-bce8-bd5b08b278de)

<h3 align="center">A skill set that helps agents become your AI twin🪞</h3>

[中文说明](README.zh-CN.md)

`WeClone-Skill` uses a lightweight persona pack to turn "reply like a specific person" into a maintainable, reviewable workflow.
Define the persona and boundaries first, inject the live reply context second, and keep a human review step at the end. The repository centers on two skills:

- 🧩 `weclone-init-twin`: initialize a persona pack template
- ✍️ `weclone-twin-reply`: combine persona files with the current scene into an isolated prompt for reply drafting

## ✨ Use Cases

- 💬 Companion-style chats for close friends or family on WhatsApp / QQ and similar apps
- 🌐 Creator or social DM replies that preserve a familiar tone when thanking or encouraging followers
- 📧 Workplace email drafting and review, including current constraints and next steps
- 🤝 Sales follow-up and quoting workflows across HubSpot leads or WeCom conversations
- 🕊️ Digital legacy persona preservation for memorial and companionship-style conversations based on a deceased person's historical data

## Installation
### Quick install (recommended)

```bash
npx skills add xming521/WeClone-Skills
```

### Or tell your agent directly

```bash
Please help me install the skills from github.com/xming521/WeClone-Skills
```

## Workflow

### 1. Initialize a persona pack

Use `weclone-init-twin` to generate a set of markdown files:

- `profile.md`: identity, personality, conversation style, values, worldview, decision style
- `persona_examples.md`: real reply examples from the person being cloned
- `state.md`: recent status, current goals, short-term constraints
- `guardrails.md`: hard boundaries, promises the twin must not make, privacy limits

### 2. Fill the pack with real content

The template is only the skeleton. Reply quality depends heavily on whether these files are concrete, real, and information-dense.

### 3. Add runtime context

Before each generation, add two kinds of runtime information:

- `scene.md`: a concise description of the current scene and background
- `dialogue.md`: the active conversation window that needs a reply

### 4. Render an isolated prompt

Use `weclone-twin-reply` to combine persona files and runtime context into a single prompt package for a downstream model to draft from in isolation.

### 5. Review before sending

This repository keeps the review gate by default. It drafts replies; it does not silently send them.

## Quick Start

### Initialize a persona pack

Generate the default English `ai_twin/` directory from the repository root:

```bash
python3 skills/weclone-init-twin/scripts/init_twin_profile.py --user-name "Alex"
```

Generate a Chinese persona pack in a custom directory:

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

Add extra context only when it will materially affect the reply:

```bash
python3 skills/weclone-twin-reply/scripts/render_clone_prompt.py \
  --persona-dir ./ai_twin \
  --scene ./scene.md \
  --dialogue ./dialogue.md \
  --extra-context ./constraints.md
```

## Included Examples

The repository includes Chinese and English examples. See [examples/README.md](examples/README.md):

- `examples/zh/social-content-twitter-fan-dm`
- `examples/zh/workplace-email-draft`
- `examples/zh/sales-copy-hubspot-wecom`
- `examples/zh/companion-chat-whatsapp-qq`
- `examples/zh/digital-legacy-memorial-reply`
- `examples/en/social-content-twitter-fan-dm`
- `examples/en/workplace-email-draft`

Example command:

```bash
python3 skills/weclone-twin-reply/scripts/render_clone_prompt.py \
  --persona-dir examples/zh/social-content-twitter-fan-dm \
  --scene examples/zh/social-content-twitter-fan-dm/scene.md \
  --dialogue examples/zh/social-content-twitter-fan-dm/dialogue.md
```

## Design Principles

- Separate long-term persona information from live conversation context
- Use `guardrails.md` to make behavioral boundaries explicit
- Keep runtime context short, but high-signal
- Preserve human review before anything is sent externally
