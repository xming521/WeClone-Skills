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

If the persona directory does not exist yet, use `$init-twin` first to scaffold the default `weclone/` directory, then ask the user to fill the generated templates before drafting.

## Core Workflow

1. Confirm that the persona pack already exists.
   If `profile.md`, `persona_examples.md`, or `guardrails.md` are missing, stop and hand off to `$init-twin`.
2. Gather the minimum high-signal context.
   Include who the other person is, what the current situation is, and the recent messages that the reply must answer.
   Write that context into two runtime files:
   - `scene.md`: a short summary of background facts that are necessary for the reply but may not be obvious from the raw chat. Include who the other person is, the relationship, the current situation, the platform or app where the reply will be sent, the user's likely goal or constraint, and any reply-specific caution such as "do not commit yet".
   - `dialogue.md`: the active message window, usually the recent turns that the candidate reply is directly answering. Keep the original wording and speaker attribution when possible.
   Use `scene.md` for distilled context and `dialogue.md` for raw conversation. Do not dump the entire chat history into `scene.md`.
3. Render the prompt package.
   Run `python3 skills/twin-reply/scripts/render_clone_prompt.py --scene <scene.md> --dialogue <dialogue.md> [--extra-context <file>]`. By default it reads persona files from `weclone/`; pass `--persona-dir <dir>` only when overriding that location.
   The script injects `scene.md` into the `Runtime Scene` section of the final prompt and `dialogue.md` into `Active Dialogue`. The clone model should see those rendered sections, not the original surrounding task thread.
4. Invoke the model with the rendered prompt only.
   Treat the rendered prompt as the entire allowed context for that generation.
5. Return a reviewable draft.
   Show the user the candidate reply plus risk flags. Do not send on the user's behalf yet.
6. Send only after explicit approval.
   If the user edits or rejects the draft, revise it and repeat the review step.

## Execution Rules

- Keep the clone run isolated.
  Use a separate model call or isolated agent run that receives only the rendered clone prompt. Do not mix in unrelated notes, hidden scratchpad, or other task memory from the current thread.
- Load persona files intentionally.
  Use `profile.md` for stable identity, personality, values, worldview, and decision logic; `state.md` for recent status and goals; `persona_examples.md` for style imitation plus behavioral evidence; and `guardrails.md` for hard limits. Load extra `*.md` files in the persona directory only when they materially improve the reply.

## Persona Fidelity Priority

This section is for creating, checking, or resolving conflicts in the persona pack. It is not a separate runtime step in reply generation.

When filling or evaluating the persona pack, prefer this order of fidelity:

1. Boundaries and safety constraints
2. `persona_examples.md`
3. Values and worldview
4. Personality and conflict style
5. Habits and conversational preferences
6. Surface tone and phrasing

If the examples and the profile disagree, do not blindly mimic wording. Resolve the conflict by preserving the person's stable boundaries first, then follow the behavioral evidence in `persona_examples.md`, then fall back to the profile's stated values and decision logic.

## Guardrails

- Refuse or soften any wording that promises actions, money, attendance, delivery, or timelines on the user's behalf.
- Exclude private information such as contact details, addresses, finances, credentials, unpublished matters, or anything the user would not want forwarded.
- Refuse insulting, humiliating, defamatory, manipulative, or otherwise reputation-damaging content.
- Prefer low-commitment language when the safe reply is unclear.
- Stop at draft stage if the runtime cannot guarantee a human review step before sending.

When a request is close to the boundary or when the other party is pressuring for a commitment, review the persona pack's `guardrails.md` first and bias toward a shorter, safer draft.

## Files And Resources

- `scripts/render_clone_prompt.py`: compile persona files and runtime context into one isolated prompt package, reading `weclone/` by default.
- `references/runtime-workflow.md`: detailed execution sequence, isolation rules, and failure handling.

## Runtime Context Format

Use a short `scene.md` like:

```md
# Scene

Other person: former coworker, familiar but not close lately.
Situation: they asked this morning whether the user can refer them this week.
Platform: WeChat private chat.
User goal: stay polite and leave room without making a commitment.
Reply caution: do not promise a referral or a timeline.
```

Use a short `dialogue.md` like:

```md
# Dialogue

Them: Hey, are you free to refer me for the role we talked about?
User: I saw your message just now.
Them: No rush, but they are moving quickly this week.
```

If some fact materially changes the likely reply but does not belong in either file, pass it as `--extra-context <file>` instead of bloating `scene.md`.

## Output Contract

Use this skill to produce a candidate reply for review, not a silent auto-send. Prefer a structured review handoff with:

- `DRAFT_REPLY`
- `RISK_FLAGS`
- `REVIEW_NOTE`

If the user asks to automate sending, keep the approval gate in place and make the send step conditional on explicit confirmation.
