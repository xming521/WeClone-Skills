![download](https://github.com/user-attachments/assets/cd4a87c6-1649-4ce5-bce8-bd5b08b278de)

<h3 align="center">一套帮助智能体成为你的 AI 分身的技能集。</h3>

[English README](README.md)

`WeClone-Skill` 用一套轻量的人格包，把“像某个人一样回复”这件事拆成可维护、可审阅的工作流。
先定义人设与边界，再注入当前回复场景信息，最后给人审阅。仓库核心分成两个技能：

- `init-twin`：初始化人格包模板
- `twin-reply`：把人格文件和当前场景拼装成隔离提示词，用于起草回复


## 使用场景

- 个人 AI 助手代写消息
- 创作者或社媒私信草稿生成
- 职场邮件起草与润色
- 保留人工审核环节的数字分身实验

## 工作流

### 1. 初始化人格包

通过 `init-twin` 生成一组 markdown 文件：

- `profile.md`：稳定身份信息、价值观、世界观、决策方式
- `state.md`：近期状态、当前目标、短期约束
- `persona_examples.md`：表达样例与行为证据
- `guardrails.md`：硬边界、不能做的承诺、隐私限制

### 2. 补充真实内容

模板只是骨架。最终回复质量高度依赖这些文件是否足够具体、真实、信息密度高。

### 3. 提供实时上下文

每次生成前，补充两类运行时信息：

- `scene.md`：简洁描述当前场景和背景
- `dialogue.md`：当前要回复的对话窗口

### 4. 渲染隔离提示词

通过 `twin-reply` 把人格文件和运行时信息组合成单一提示词包，交给下游模型独立生成草稿。

### 5. 人工审阅后再发送

这个仓库默认保留审核门。它负责起草，不负责静默发送。


## 快速开始

### 初始化人格包

在仓库根目录生成默认的英文 `ai_twin/`：

```bash
python3 skills/init-twin/scripts/init_twin_profile.py --user-name "Alex"
```

生成中文人格包到自定义目录：

```bash
python3 skills/init-twin/scripts/init_twin_profile.py \
  --user-name "张三" \
  --language zh \
  ./my_twin
```

如果目标目录里已经有同名文件，脚本会拒绝覆盖；只有显式传入 `--force` 才会重写。

### 基于人格包渲染提示词

```bash
python3 skills/twin-reply/scripts/render_clone_prompt.py \
  --persona-dir ./ai_twin \
  --scene ./scene.md \
  --dialogue ./dialogue.md
```

输出到文件：

```bash
python3 skills/twin-reply/scripts/render_clone_prompt.py \
  --persona-dir ./ai_twin \
  --scene ./scene.md \
  --dialogue ./dialogue.md \
  --output ./rendered_prompt.md
```

只有在确实会影响回复结果时，再追加额外上下文：

```bash
python3 skills/twin-reply/scripts/render_clone_prompt.py \
  --persona-dir ./ai_twin \
  --scene ./scene.md \
  --dialogue ./dialogue.md \
  --extra-context ./constraints.md
```

## 内置示例

仓库内置了中英文示例，说明见 [examples/README.md](examples/README.md)：

- `examples/zh/social-content-twitter-fan-dm`
- `examples/zh/workplace-email-draft`
- `examples/en/social-content-twitter-fan-dm`
- `examples/en/workplace-email-draft`

示例命令：

```bash
python3 skills/twin-reply/scripts/render_clone_prompt.py \
  --persona-dir examples/zh/social-content-twitter-fan-dm \
  --scene examples/zh/social-content-twitter-fan-dm/scene.md \
  --dialogue examples/zh/social-content-twitter-fan-dm/dialogue.md
```

## 设计原则

- 长期人格信息与实时对话上下文分离
- 用 `guardrails.md` 固化行为边界
- 运行时上下文尽量短，但要高信号
- 对外发送前保留人工确认
