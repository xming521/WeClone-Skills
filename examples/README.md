# Examples

这个目录按语言拆成两层：

- `examples/zh/`：中文样例
- `examples/en/`：英文样例

当前内置中文样例如下：

- `social-content-twitter-fan-dm`：社交与内容创作场景，模拟创作者在 Twitter/X 上自动回复粉丝私信。
- `workplace-email-draft`：职场与效率场景，模拟职场用户自动起草或回复邮件。
- `sales-copy-hubspot-wecom`：销售跟进场景，模拟销售在 HubSpot 记录线索后，用企业微信延续跟进和报价沟通。
- `companion-chat-whatsapp-qq`：陪伴式聊天场景，模拟家人或朋友在 WhatsApp / QQ 中获得更温和、稳定的“分身陪伴”回复。
- `digital-legacy-memorial-reply`：身后数字遗产场景，模拟基于逝者历史聊天记录重建的人格分身，在纪念性对话中延续熟悉的表达方式与陪伴感。

当前内置英文样例如下：

- `social-content-twitter-fan-dm`：creator / fan DM scenario on Twitter/X.
- `workplace-email-draft`：workplace email drafting scenario.
- `sales-copy-hubspot-wecom`：sales follow-up scenario across HubSpot notes and WeCom client messaging.
- `companion-chat-whatsapp-qq`：companion-style chat scenario for family or close-friend conversations on WhatsApp / QQ.
- `digital-legacy-memorial-reply`：digital legacy scenario where a memorial twin is reconstructed from a deceased person's historical chats and used for remembrance-oriented conversation.

## 渲染中文样例

```bash
python3 skills/weclone-twin-reply/scripts/render_clone_prompt.py \
  --persona-dir examples/zh/social-content-twitter-fan-dm \
  --scene examples/zh/social-content-twitter-fan-dm/scene.md \
  --dialogue examples/zh/social-content-twitter-fan-dm/dialogue.md
```

## 渲染英文样例

```bash
python3 skills/weclone-twin-reply/scripts/render_clone_prompt.py \
  --persona-dir examples/en/workplace-email-draft \
  --scene examples/en/workplace-email-draft/scene.md \
  --dialogue examples/en/workplace-email-draft/dialogue.md
```

## 渲染新增中文销售样例

```bash
python3 skills/weclone-twin-reply/scripts/render_clone_prompt.py \
  --persona-dir examples/zh/sales-copy-hubspot-wecom \
  --scene examples/zh/sales-copy-hubspot-wecom/scene.md \
  --dialogue examples/zh/sales-copy-hubspot-wecom/dialogue.md
```

如果你要继续扩展更多行业或平台，最稳妥的方式是从最接近的语言目录复制一个现有场景，再按同样结构改内容。
