# WeClone Runtime Workflow

## Minimum Inputs

- A persona directory with `profile.md`, `persona_examples.md`, and `guardrails.md`
- A short scene summary
- The active dialogue window
- Optional extra context files only when they change the likely reply

## Isolation Rule

Use a separate model call for the clone run. The rendered prompt must be the only context passed into that call, aside from the fixed system wrapper required by the runtime. Do not pass:

- The current agent's scratchpad
- Unrelated planning notes
- Other users' memories
- Earlier tasks from the same thread

If the runtime cannot guarantee that isolation, stop and tell the user you can only produce a manual draft.

## Execution Sequence

1. Verify the persona directory exists.
2. Initialize it with `scripts/init_clone_profile.py` if it does not exist yet.
3. Confirm that the persona files are filled with real content rather than placeholders.
4. Capture the current scene in a short markdown file.
5. Capture the current dialogue in a short markdown file.
6. Render the prompt with `scripts/render_clone_prompt.py`.
7. Invoke the separate model with the rendered prompt only.
8. Present the model output to the user for review.
9. Send only after explicit approval.

## Review Handoff

Prefer a three-part result:

- `DRAFT_REPLY`: the exact message candidate
- `RISK_FLAGS`: `none` or a comma-separated list from `promise`, `privacy`, `reputation`, `ambiguity`
- `REVIEW_NOTE`: one short sentence explaining what the reviewer should watch for

## Failure Handling

- Missing persona pack: initialize the templates and stop until the user fills them.
- Missing scene or dialogue: ask for the missing input instead of guessing.
- Guardrail conflict: produce a safer fallback draft or stop with a clear reason.
- Missing approval: do not send.
