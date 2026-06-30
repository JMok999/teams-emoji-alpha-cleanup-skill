# Teams Emoji Alpha Cleanup Skill

[English](README.md) · [中文](README.zh-CN.md)

## 这个项目做什么

这个仓库只有一个正式 Skill，用于把已有的表情包、头像、贴纸、图标或简单插画处理成可用于 Microsoft Teams 自定义 Emoji 的文件。

它是一个素材清理流程。它会保留选择的原图主体，不会重新绘制，也不会改造成另一种风格。

**参考输出：** 经过验证的 `256 × 256` lossless WEBP，带真实 RGBA Alpha、干净边缘、合理留白，并且在 Teams 中没有明显白框或白边。

**聊天 fallback：** 当聊天图片工具无法导出 WEBP、但能返回可下载的真实透明 PNG 时，可以把 PNG 作为 Teams 候选文件测试。它必须如实标记为 PNG，并在上传后完成验证。

## 预览

### 处理前 → 处理后

![处理前后](docs/images/before-after-teams.svg)

### 背景验证

![背景验证](docs/images/validation-backgrounds.svg)

## 从这里开始

### ChatGPT、Claude 或其他聊天模型

普通的单张图片需求，上传原图后，直接使用短提示：

- [聊天短提示](prompts/teams-emoji-quick.zh-CN.md)

这是默认路径。它要求模型直接处理图片、不要输出长篇流程说明、优先 WebP；若无法导出 WebP，则必须如实说明 PNG。

只有在结果失败、需要排查限制、或要比较不同工具支持度时，才阅读完整的 [ChatGPT / Claude 使用指南](docs/CHATGPT_CLAUDE_GUIDE.md)。

### 本地 Python 或具备文件操作能力的 Agent

重复处理或需要完整技术规范时，使用 [`SKILL.md`](SKILL.md) 和仓库中的 helper。

```bash
git clone https://github.com/JMok999/teams-emoji-alpha-cleanup-skill.git
cd teams-emoji-alpha-cleanup-skill
python -m pip install -r requirements.txt
python scripts/clean_teams_emoji.py input.jpg input_teams_emoji_256.webp
```

参考 helper 始终导出严格的 lossless WEBP。

## 一个正式 Skill，加一个可选 Prompt Pack

- [`SKILL.md`](SKILL.md)：原图透明处理、文件检查与 Teams 导出规则。
- [`prompts/teams-emoji-creator-prompts.zh-CN.md`](prompts/teams-emoji-creator-prompts.zh-CN.md)：可选的原创工作场景反应表情 Prompt Pack。

Prompt Pack 不是第二个 Skill，只用于创意探索。生成概念图不自动等于 Teams 成品；选定图片后，仍需通过正式清理流程才能交付。

## 选择合适的使用方式

| 目标 | 使用方式 | 接受标准 |
|---|---|---|
| 创作新的反应表情概念 | [Prompt Pack](prompts/teams-emoji-creator-prompts.zh-CN.md) | 只用于创意，不自动是 Teams 文件 |
| 保留已有表情并去除背景 | [`SKILL.md`](SKILL.md) | 主体保持与原图一致 |
| 在 ChatGPT 或 Claude 中处理单张图片 | [聊天短提示](prompts/teams-emoji-quick.zh-CN.md) | 优先下载 WEBP；无法导出时，真实透明 PNG 可作为 Teams 候选文件，但必须如实标记格式 |
| 重复或技术型处理 | Python helper 或具备文件操作能力的 Agent | 严格 lossless WEBP，加文件检查与视觉验证 |

## 输出标准

| 项目 | 严格 helper / Agent 路径 | 聊天 fallback 路径 |
|---|---|---|
| 文件 | Lossless WEBP | 优先 WEBP；聊天工具无法导出时才允许真实透明 PNG |
| 画布 | 必须为 256 × 256 px | 工具允许时必须为 256 × 256 px |
| 透明度 | 已验证的真实 RGBA Alpha | 工具可显示元数据时验证 Alpha；无法显示时上传后实测 |
| 命名 | `.webp` 必须与实际格式一致 | 如实说明 `.png` 或 `.webp`，不可把 PNG 改名为 WebP |
| JPEG | 不允许 | 不允许作为透明最终文件 |
| 留白 | 约 8–12% 透明边距 | 约 8–12% 透明边距 |
| 主体 | 完整、居中、不可重新设计 | 完整、居中、不可重新设计 |
| 边缘 | 无白框、白边、灰边或棋盘格残留 | 无白框、白边、灰边或棋盘格残留 |
| 检查背景 | `#FFFFFF`、`#ECEEF6`、`#242424`、`#000000` | 工具无法提供元数据时，在实际 Teams 上传后检查 |

## 验证与回归测试

运行确定性的 helper 测试：

```bash
python -m pip install -r requirements.txt
python tests/test_helper.py
```

测试图目录、预期行为，以及聊天模型的人工兼容性测试说明见 [Self Test](tests/SELF_TEST.zh-CN.md)。

## 限制

- 参考 helper 主要适合平面或接近平面背景。
- 复杂照片、发丝、毛发、玻璃、烟雾或透明材质，需要语义分割或人工优化蒙版。
- 预览图不等于文件。聊天工具无法返回下载文件，就代表任务尚未完成。
- 网页保存的 JPG 或 PNG 可以作为输入，但某一次聊天会话中，平台仍可能无法将它绑定给图片编辑工具。
- 聊天工具能返回下载 PNG 但无法显示元数据时，请先上传 Teams 测试，再称为已验证。

## 项目结构

```text
teams-emoji-alpha-cleanup-skill/
├─ README.md
├─ README.zh-CN.md
├─ SKILL.md
├─ requirements.txt
├─ docs/
│  ├─ CHATGPT_CLAUDE_GUIDE.en.md
│  ├─ CHATGPT_CLAUDE_GUIDE.md
│  └─ images/
├─ prompts/
│  ├─ chatgpt-teams-emoji-quick-prompt.en.md
│  ├─ teams-emoji-quick.zh-CN.md
│  └─ teams-emoji-creator-prompts.md
├─ scripts/
│  └─ clean_teams_emoji.py
└─ tests/
   ├─ generate_fixtures.py
   ├─ test_helper.py
   ├─ SELF_TEST.md
   └─ SELF_TEST.zh-CN.md
```

## License

本项目采用 [MIT License](LICENSE) 开源。
