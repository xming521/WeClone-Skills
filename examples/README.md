# Examples

这个目录按语言拆成两层：

- `examples/zh/`：中文样例
- `examples/en/`：英文样例

每种语言下都包含同样两个场景：

- `social-content-twitter-fan-dm`：社交与内容创作场景，模拟创作者在 Twitter/X 上自动回复粉丝私信。
- `workplace-email-draft`：职场与效率场景，模拟职场用户自动起草或回复邮件。

## 渲染中文样例

```bash
python3 skills/twin-reply/scripts/render_clone_prompt.py \
  --persona-dir examples/zh/social-content-twitter-fan-dm \
  --scene examples/zh/social-content-twitter-fan-dm/scene.md \
  --dialogue examples/zh/social-content-twitter-fan-dm/dialogue.md
```

## 渲染英文样例

```bash
python3 skills/twin-reply/scripts/render_clone_prompt.py \
  --persona-dir examples/en/workplace-email-draft \
  --scene examples/en/workplace-email-draft/scene.md \
  --dialogue examples/en/workplace-email-draft/dialogue.md
```

如果你要继续扩展更多行业或平台，最稳妥的方式是从最接近的语言目录复制一个现有场景，再按同样结构改内容。
