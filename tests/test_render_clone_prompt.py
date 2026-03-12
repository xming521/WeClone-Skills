import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "skills" / "weclone-twin-reply" / "scripts" / "render_clone_prompt.py"
TEMPLATE_PATH = REPO_ROOT / "skills" / "weclone-twin-reply" / "assets" / "clone_prompt_template.md"
EXAMPLES_ROOT = REPO_ROOT / "examples"


class RenderClonePromptCLITest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name)
        self.persona_dir = self.workspace / "persona"
        self.persona_dir.mkdir()

        self._write_persona_file(
            "profile.md",
            (
                "# 角色档案\n\n"
                "姓名：林澈\n"
                "身份：27 岁的独立游戏策划。\n"
                "性格：说话克制、真诚，不喜欢空话。"
            ),
        )
        self._write_persona_file(
            "persona_examples.md",
            (
                "# 表达样例\n\n"
                "- 我先把事实说清楚，再看怎么帮你更合适。\n"
                "- 这件事我可以配合，但我不想先把话说满。"
            ),
        )
        self._write_persona_file(
            "guardrails.md",
            (
                "# 边界\n\n"
                "- 不替别人做无法兑现的承诺。\n"
                "- 不泄露团队内部讨论内容。"
            ),
        )
        self._write_persona_file(
            "state.md",
            (
                "# 近期状态\n\n"
                "最近在赶版本上线，回复会偏简短，但不会显得冷淡。"
            ),
        )
        self._write_persona_file(
            "notes.md",
            (
                "# 补充设定\n\n"
                "对熟人会更温和，对陌生合作会先确认边界。"
            ),
        )

        self.scene_path = self.workspace / "scene.md"
        self.scene_path.write_text(
            (
                "# 场景\n\n"
                "对方：以前合作过的插画师。\n"
                "平台：微信私聊。\n"
                "目标：礼貌回复，但不要立刻答应合作排期。"
            ),
            encoding="utf-8",
        )
        self.dialogue_path = self.workspace / "dialogue.md"
        self.dialogue_path.write_text(
            (
                "# 对话\n\n"
                "对方：这周能不能把新项目也一起接了？\n"
                "用户：我刚看到，你先说下时间要求。"
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _write_persona_file(self, name: str, content: str) -> None:
        (self.persona_dir / name).write_text(content, encoding="utf-8")

    def _run_script(self, *extra_args: str) -> subprocess.CompletedProcess:
        command = [
            sys.executable,
            str(SCRIPT_PATH),
            "--persona-dir",
            str(self.persona_dir),
            "--scene",
            str(self.scene_path),
            "--dialogue",
            str(self.dialogue_path),
            "--template",
            str(TEMPLATE_PATH),
            *extra_args,
        ]
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_renders_chinese_persona_into_template_stdout(self) -> None:
        result = self._run_script()

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("# Twin Reply Isolated Prompt", result.stdout)
        self.assertIn("## Persona File: profile.md", result.stdout)
        self.assertIn("姓名：林澈", result.stdout)
        self.assertIn("## Persona File: state.md", result.stdout)
        self.assertIn("最近在赶版本上线", result.stdout)
        self.assertIn("## Persona File: notes.md", result.stdout)
        self.assertIn("对熟人会更温和", result.stdout)
        self.assertIn("## Runtime Scene", result.stdout)
        self.assertIn("目标：礼貌回复，但不要立刻答应合作排期。", result.stdout)
        self.assertIn("## Active Dialogue", result.stdout)
        self.assertIn("对方：这周能不能把新项目也一起接了？", result.stdout)
        self.assertNotIn("{{PERSONA_SECTIONS}}", result.stdout)
        self.assertEqual(result.stderr, "")

    def test_writes_rendered_prompt_to_output_file(self) -> None:
        output_path = self.workspace / "rendered_prompt.md"

        result = self._run_script("--output", str(output_path))

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertTrue(output_path.is_file())
        rendered = output_path.read_text(encoding="utf-8")
        self.assertIn("DRAFT_REPLY:", rendered)
        self.assertIn("林澈", rendered)
        self.assertIn("微信私聊", rendered)
        self.assertEqual(result.stdout, "")


class RenderClonePromptExamplesCLITest(unittest.TestCase):
    def test_example_persona_packs_render_successfully(self) -> None:
        examples = [
            (
                "zh/social-content-twitter-fan-dm",
                "平台：Twitter/X 私信。",
                "能不能请你帮我看看？",
            ),
            (
                "zh/workplace-email-draft",
                "平台：Email。",
                "could you review the renewal email copy",
            ),
            (
                "zh/sales-copy-hubspot-wecom",
                "平台：HubSpot 线索记录 + 企业微信跟进。",
                "你这边能不能先帮我申请一个更积极的价格？",
            ),
            (
                "zh/companion-chat-whatsapp-qq",
                "平台：WhatsApp 家人聊天。",
                "我这两天不知道为什么，总是晚上睡不着",
            ),
            (
                "zh/digital-legacy-memorial-reply",
                "平台：微信。",
                "如果你还会回我，你大概会跟我说什么？",
            ),
            (
                "en/social-content-twitter-fan-dm",
                "Platform: Twitter/X DM.",
                "Would you mind taking a look?",
            ),
            (
                "en/workplace-email-draft",
                "Platform: Email.",
                "could you review the renewal email copy",
            ),
            (
                "en/sales-copy-hubspot-wecom",
                "Platform: HubSpot lead notes plus WeCom follow-up.",
                "can you help me get a more aggressive price?",
            ),
            (
                "en/companion-chat-whatsapp-qq",
                "Platform: WhatsApp family chat.",
                "I do not know why, but I keep lying awake at night",
            ),
            (
                "en/digital-legacy-memorial-reply",
                "Platform: WeChat.",
                "If you could still answer me, what do you think you would say?",
            ),
        ]

        for example_name, expected_scene, expected_dialogue in examples:
            with self.subTest(example=example_name):
                example_dir = EXAMPLES_ROOT / example_name
                command = [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--persona-dir",
                    str(example_dir),
                    "--scene",
                    str(example_dir / "scene.md"),
                    "--dialogue",
                    str(example_dir / "dialogue.md"),
                    "--template",
                    str(TEMPLATE_PATH),
                ]

                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    check=False,
                )

                self.assertEqual(result.returncode, 0, msg=result.stderr)
                self.assertIn("# Twin Reply Isolated Prompt", result.stdout)
                self.assertIn("## Persona File: profile.md", result.stdout)
                self.assertIn("## Persona File: guardrails.md", result.stdout)
                self.assertIn(expected_scene, result.stdout)
                self.assertIn(expected_dialogue, result.stdout)
                self.assertNotIn("{{PERSONA_SECTIONS}}", result.stdout)
                self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
