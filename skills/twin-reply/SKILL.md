---
name: twin-reply
description: Build a review-gated digital twin reply from persona markdown, persona examples, and live conversation context. Use when you need to imitate a specific user's chat style, draft a reply on the user's behalf, or generate a persona-consistent message candidate from an existing persona pack.
---

# Twin Reply

Assemble an isolated prompt package that lets a separate model imitate one user's messaging style, personality, values, and worldview from markdown persona files and persona examples. Draft first, review second, send last.

## Expected Inputs

- A prepared persona directory. Default to `weclone/` at the repo root, containing `profile.md`, `persona_examples.md`, `guardrails.md`, and optional `state.md`.
- Runtime context: one short scene summary and one dialogue window.
- Explicit approval from the user before any outbound send.

If the persona directory does not exist yet, use `$init-twin-profile` first to scaffold the default `weclone/` directory, then ask the user to fill the generated templates before drafting.

## Core Workflow

1. Confirm that the persona pack already exists.
   If `profile.md`, `persona_examples.md`, or `guardrails.md` are missing, stop and hand off to `$init-twin-profile`.
2. Gather the minimum high-signal context.
   Include who the other person is, what the current situation is, and the recent messages that the reply must answer.
3. Keep the clone run isolated.
   Use a separate model call or isolated agent run that receives only the rendered clone prompt. Do not mix in unrelated notes, hidden scratchpad, or other task memory from the current thread.
4. Load persona files.
   Use `profile.md` for stable identity, personality, values, worldview, and decision logic; `state.md` for recent status and goals; `persona_examples.md` for style imitation plus behavioral evidence; and `guardrails.md` for hard limits. Load extra `*.md` files in the persona directory only when they materially improve the reply.
5. Render the prompt package.
   Run `python3 skills/twin-reply/scripts/render_clone_prompt.py --scene <scene.md> --dialogue <dialogue.md> [--extra-context <file>]`. By default it reads persona files from `weclone/`; pass `--persona-dir <dir>` only when overriding that location.
6. Invoke the model with the rendered prompt only.
   Treat the rendered prompt as the entire allowed context for that generation.
7. Return a reviewable draft.
   Show the user the candidate reply plus risk flags. Do not send on the user's behalf yet.
8. Send only after explicit approval.
   If the user edits or rejects the draft, revise it and repeat the review step.

## Persona Modeling Standard

When filling or evaluating the persona pack, prefer this order of fidelity:

1. Boundaries and safety constraints
2. Values and worldview
3. Personality and conflict style
4. Habits and conversational preferences
5. Surface tone and phrasing

If the examples and the profile disagree, do not blindly mimic wording. Resolve the conflict by preserving the person's stable values and boundaries first.

## Guardrails

- Refuse or soften any wording that promises actions, money, attendance, delivery, or timelines on the user's behalf.
- Exclude private information such as contact details, addresses, finances, credentials, unpublished matters, or anything the user would not want forwarded.
- Refuse insulting, humiliating, defamatory, manipulative, or otherwise reputation-damaging content.
- Prefer low-commitment language when the safe reply is unclear.
- Stop at draft stage if the runtime cannot guarantee a human review step before sending.

Read `references/guardrails.md` when a request is close to the boundary or when the other party is pressuring for a commitment.

## Files And Resources

- `scripts/render_clone_prompt.py`: compile persona files and runtime context into one isolated prompt package, reading `weclone/` by default.
- `references/runtime-workflow.md`: detailed execution sequence, isolation rules, and failure handling.
- `references/guardrails.md`: hard blocks, safe substitutions, and review risk tags.

## Output Contract

Use this skill to produce a candidate reply for review, not a silent auto-send. Prefer a structured review handoff with:

- `DRAFT_REPLY`
- `RISK_FLAGS`
- `REVIEW_NOTE`

If the user asks to automate sending, keep the approval gate in place and make the send step conditional on explicit confirmation.
