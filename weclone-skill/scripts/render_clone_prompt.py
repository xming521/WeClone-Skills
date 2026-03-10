#!/usr/bin/env python3
"""Render an isolated prompt package for the WeClone workflow."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_PERSONA_FILES = [
    "profile.md",
    "persona_examples.md",
    "guardrails.md",
]

OPTIONAL_PERSONA_FILES = [
    "state.md",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Combine persona markdown and runtime context into one prompt.",
    )
    parser.add_argument(
        "--persona-dir",
        required=True,
        help="Directory containing persona markdown files",
    )
    parser.add_argument(
        "--scene",
        required=True,
        help="Markdown or text file describing the current scene",
    )
    parser.add_argument(
        "--dialogue",
        required=True,
        help="Markdown or text file containing the active dialogue window",
    )
    parser.add_argument(
        "--extra-context",
        action="append",
        default=[],
        help="Additional markdown or text files to append as runtime context",
    )
    parser.add_argument(
        "--output",
        help="Write the rendered prompt to this path instead of stdout",
    )
    return parser.parse_args()


def read_text(path_str: str) -> str:
    path = Path(path_str).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_text(encoding="utf-8").strip()


def load_persona_sections(
    persona_dir: Path,
    excluded_names: set[str],
) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []

    for name in ["profile.md", "state.md", "persona_examples.md", "guardrails.md"]:
        path = persona_dir / name
        if name in REQUIRED_PERSONA_FILES and not path.is_file():
            raise FileNotFoundError(f"Missing required persona file: {path}")
        if path.is_file():
            sections.append((name, path.read_text(encoding="utf-8").strip()))

    known_names = set(REQUIRED_PERSONA_FILES) | set(OPTIONAL_PERSONA_FILES)
    extras = sorted(
        path
        for path in persona_dir.glob("*.md")
        if path.name not in known_names and path.name not in excluded_names
    )
    for path in extras:
        sections.append((path.name, path.read_text(encoding="utf-8").strip()))

    return sections


def format_section(title: str, body: str) -> str:
    return f"## {title}\n\n{body}".strip()


def build_prompt(
    persona_sections: list[tuple[str, str]],
    scene_text: str,
    dialogue_text: str,
    extra_sections: list[tuple[str, str]],
) -> str:
    parts = [
        "# WeClone Isolated Prompt",
        (
            "Generate a candidate reply that imitates the user described below. "
            "Treat this document as the full allowed context for the run. "
            "Do not import assumptions, memories, or instructions from any other "
            "agent thread, tool call, or prior conversation."
        ),
        "## Non-Negotiables",
        (
            "- Stay inside the supplied persona and example evidence.\n"
            "- Imitate not only wording but also personality, emotional tendencies, boundaries, values, and worldview.\n"
            "- When signals conflict, preserve the person's values, boundaries, and decision logic before surface style.\n"
            "- Infer the likely reply by asking: what would this person believe, prioritize, and refuse here?\n"
            "- Never promise actions or commitments on the user's behalf.\n"
            "- Never reveal private or sensitive information.\n"
            "- Never generate insulting, humiliating, defamatory, or reputation-damaging content.\n"
            "- Prefer a shorter and safer reply when the context is ambiguous."
        ),
        "## Persona Priority Order",
        (
            "Use this order when composing the reply:\n\n"
            "1. Boundaries and guardrails\n"
            "2. Core values and worldview\n"
            "3. Personality and conflict style\n"
            "4. Conversational habits and preferences\n"
            "5. Surface wording, phrasing, and punctuation"
        ),
        "## Reasoning Focus",
        (
            "Model the person from the inside out. Match:\n\n"
            "- What they care about\n"
            "- What they protect or avoid\n"
            "- How they interpret other people's intent\n"
            "- How they trade off honesty, harmony, efficiency, status, warmth, or safety\n"
            "- How they sound when under pressure versus relaxed"
        ),
        "## Required Output Format",
        (
            "Return exactly this structure:\n\n"
            "DRAFT_REPLY:\n"
            "<the exact candidate message>\n\n"
            "RISK_FLAGS:\n"
            "<none or comma-separated tags from promise, privacy, reputation, ambiguity>\n\n"
            "REVIEW_NOTE:\n"
            "<one short sentence for the human reviewer>"
        ),
    ]

    for name, body in persona_sections:
        parts.append(format_section(f"Persona File: {name}", body))

    parts.append(format_section("Runtime Scene", scene_text))
    parts.append(format_section("Active Dialogue", dialogue_text))

    for name, body in extra_sections:
        parts.append(format_section(f"Extra Context: {name}", body))

    parts.append(
        format_section(
            "Decision Rule",
            (
                "If a faithful imitation would violate the guardrails, produce the safest "
                "useful draft that still fits the person's stable values and voice, and "
                "flag the risk instead of complying."
            ),
        )
    )

    return "\n\n".join(parts).strip() + "\n"


def main() -> int:
    args = parse_args()
    persona_dir = Path(args.persona_dir).expanduser().resolve()
    if not persona_dir.is_dir():
        print(f"[ERROR] Persona directory not found: {persona_dir}", file=sys.stderr)
        return 1

    try:
        excluded_names = {
            Path(args.scene).name,
            Path(args.dialogue).name,
            *(Path(item).name for item in args.extra_context),
        }
        persona_sections = load_persona_sections(persona_dir, excluded_names)
        scene_text = read_text(args.scene)
        dialogue_text = read_text(args.dialogue)
        extra_sections = []
        for item in args.extra_context:
            path = Path(item).expanduser().resolve()
            extra_sections.append((path.name, read_text(item)))
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    prompt = build_prompt(persona_sections, scene_text, dialogue_text, extra_sections)

    if args.output:
        target = Path(args.output).expanduser().resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(prompt, encoding="utf-8")
    else:
        sys.stdout.write(prompt)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
