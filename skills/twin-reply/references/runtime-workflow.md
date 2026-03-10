# Twin Reply Runtime Workflow

## Minimum Inputs

- A persona directory at `weclone/` by default, with `profile.md`, `persona_examples.md`, and `guardrails.md`
- A short scene summary
- The active dialogue window
- Optional extra context files only when they change the likely reply

`profile.md` should be rich enough to describe stable personality, values, worldview, and decision logic, not just tone markers.

## Isolation Rule

Use a separate model call for the clone run. The rendered prompt must be the only context passed into that call, aside from the fixed system wrapper required by the runtime. Do not pass:

- The current agent's scratchpad
- Unrelated planning notes
- Other users' memories
- Earlier tasks from the same thread

If the runtime cannot guarantee that isolation, stop and tell the user you can only produce a manual draft.

## Execution Sequence

1. Verify the default persona directory `weclone/` exists, unless the run explicitly uses another `--persona-dir`.
2. If it does not exist yet, stop and hand off to `$init-twin-profile`.
3. Confirm that the persona files are filled with real content rather than placeholders.
   Check that they capture deeper traits such as conflict style, priorities, and worldview, not only favorite phrases.
4. Capture the current scene in a short markdown file.
   This is usually `scene.md`. It should summarize the non-obvious facts the reply depends on: who the other person is, the relationship, the situation, the user's intent or constraint, and any caution such as avoiding a commitment. Keep it brief and high-signal.
5. Capture the current dialogue in a short markdown file.
   This is usually `dialogue.md`. It should contain the recent message turns the model must answer directly. Preserve speaker labels and wording where possible instead of paraphrasing.
6. Render the prompt with `skills/twin-reply/scripts/render_clone_prompt.py`.
   The renderer places `scene.md` under `Runtime Scene` and `dialogue.md` under `Active Dialogue` in the isolated prompt. Those rendered sections are how the runtime context reaches the clone model.
7. Invoke the separate model with the rendered prompt only.
8. Present the model output to the user for review.
9. Send only after explicit approval.

## Scene Vs Dialogue

- Put distilled background and reply strategy in `scene.md`.
- Put the raw recent messages in `dialogue.md`.
- If information is already visible in the chat, prefer leaving it in `dialogue.md` instead of repeating it in `scene.md`.
- If a fact is useful but peripheral, add it through `--extra-context` rather than turning `scene.md` into a long memo.

Example `scene.md`:

```md
# Scene

Other person: client contact, friendly but time-sensitive.
Situation: they are asking whether the user can deliver by Friday.
User goal: stay cooperative without confirming a deadline yet.
Reply caution: avoid promises and avoid sounding evasive.
```

Example `dialogue.md`:

```md
# Dialogue

Client: Can you confirm you'll have this by Friday?
User: I am checking the schedule now.
Client: I need to update my team this afternoon.
```

## Review Handoff

Prefer a three-part result:

- `DRAFT_REPLY`: the exact message candidate
- `RISK_FLAGS`: `none` or a comma-separated list from `promise`, `privacy`, `reputation`, `ambiguity`
- `REVIEW_NOTE`: one short sentence explaining what the reviewer should watch for

## Failure Handling

- Missing persona pack: hand off to `$init-twin-profile` and stop until the user fills the templates.
- Missing scene or dialogue: ask for the missing input instead of guessing.
- Guardrail conflict: produce a safer fallback draft or stop with a clear reason.
- Value conflict: preserve the user's stable values and boundaries over stylistic mimicry.
- Missing approval: do not send.
