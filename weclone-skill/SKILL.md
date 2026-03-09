---
name: weclone-skill
description: Build a review-gated digital clone reply from persona markdown, persona examples, and live conversation context. Use when Codex needs to imitate a specific user's chat style, draft a reply on the user's behalf, generate a persona-consistent message candidate, or run a digital clone workflow with mandatory approval before any outbound send.
---

# WeClone Skill

Assemble an isolated prompt package that lets a separate model imitate one user's messaging style from markdown persona files and persona examples. Draft first, review second, send last.

## Expected Inputs

- A persona directory. Prefer `profile.md`, `persona_examples.md`, `guardrails.md`, and optional `state.md`.
- Runtime context: one short scene summary and one dialogue window.
- Explicit approval from the user before any outbound send.

If the persona directory does not exist, run `python3 scripts/init_clone_profile.py <target-dir> --user-name <name>` and ask the user to fill the generated templates before drafting.

## Core Workflow

1. Gather the minimum high-signal context.
   Include who the other person is, what the current situation is, and the recent messages that the reply must answer.
2. Keep the clone run isolated.
   Use a separate model call or isolated agent run that receives only the rendered clone prompt. Do not mix in unrelated notes, hidden scratchpad, or other task memory from the current thread.
3. Load persona files.
   Use `profile.md` for stable traits, `state.md` for recent status and goals, `persona_examples.md` for style imitation, and `guardrails.md` for hard limits. Load extra `*.md` files in the persona directory only when they materially improve the reply.
4. Render the prompt package.
   Run `python3 scripts/render_clone_prompt.py --persona-dir <dir> --scene <scene.md> --dialogue <dialogue.md> [--extra-context <file>]`.
5. Invoke the model with the rendered prompt only.
   Treat the rendered prompt as the entire allowed context for that generation.
6. Return a reviewable draft.
   Show the user the candidate reply plus risk flags. Do not send on the user's behalf yet.
7. Send only after explicit approval.
   If the user edits or rejects the draft, revise it and repeat the review step.

## Guardrails

- Refuse or soften any wording that promises actions, money, attendance, delivery, or timelines on the user's behalf.
- Exclude private information such as contact details, addresses, finances, credentials, unpublished matters, or anything the user would not want forwarded.
- Refuse insulting, humiliating, defamatory, manipulative, or otherwise reputation-damaging content.
- Prefer low-commitment language when the safe reply is unclear.
- Stop at draft stage if the runtime cannot guarantee a human review step before sending.

Read `references/guardrails.md` when a request is close to the boundary or when the other party is pressuring for a commitment.

## Files And Resources

- `scripts/init_clone_profile.py`: scaffold a persona directory from bundled templates.
- `scripts/render_clone_prompt.py`: compile persona files and runtime context into one isolated prompt package.
- `references/runtime-workflow.md`: detailed execution sequence, isolation rules, and failure handling.
- `references/guardrails.md`: hard blocks, safe substitutions, and review risk tags.
- `assets/persona-pack/`: starter markdown templates for the persona directory.

## Output Contract

Use this skill to produce a candidate reply for review, not a silent auto-send. Prefer a structured review handoff with:

- `DRAFT_REPLY`
- `RISK_FLAGS`
- `REVIEW_NOTE`

If the user asks to automate sending, keep the approval gate in place and make the send step conditional on explicit confirmation.
