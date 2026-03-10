---
name: init-twin
description: Scaffold a digital twin persona directory with markdown templates such as profile, state, persona examples, and guardrails. Use when the user wants to initialize, bootstrap, reset, or regenerate the persona files that twin-reply will read.
---

# Init Twin Profile

Create or refresh the markdown persona pack for a user's digital twin. This skill prepares files only. It does not draft replies.

## Expected Inputs

- A user name for template placeholders.
- An optional target directory. Default to `weclone/` at the repo root.
- Explicit approval before overwriting existing persona files.

## Core Workflow

1. Check whether the target persona directory already exists.
   If files already exist, do not overwrite them unless the user explicitly asks for regeneration.
2. Scaffold the persona pack.
   Run `python3 skills/init-twin/scripts/init_twin_profile.py --user-name <name> [output_dir]`.
3. Regenerate only with explicit overwrite approval.
   Add `--force` only when the user clearly wants to replace existing files.
4. Hand off to reply generation.
   Tell the user to fill the generated markdown templates before using `$twin-reply`.

## Files And Resources

- `scripts/init_twin_profile.py`: scaffold the default `weclone/` persona directory from bundled templates.
- `assets/persona-pack/`: starter markdown templates for `profile.md`, `state.md`, `persona_examples.md`, and `guardrails.md`.

## Output Contract

Return a short setup handoff with:

- `CREATED_FILES`
- `TARGET_DIR`
- `NEXT_STEP`
