# Teams Emoji Alpha Cleanup Skill

[English](README.md) · [中文](README.zh-CN.md)

## 这个项目做什么

这个仓库只有一个正式 Skill，用于把已有的表情包、头像、贴纸、图标或简单插画处理成可用于 Microsoft Teams 自定义 Emoji 的文件。

它是一个素材清理流程。它会保留选择的原图主体，不会重新绘制，也不会改造成另一种风格。

**最终目标：** 一个 `256 × 256` 的透明 WEBP，边缘干净、留白合理，并且在 Teams 中没有明显白框或白边。

## 预览

### 处理前 → 处理后

![处理前后](docs/images/before-after-teams.svg)

### 背景验证

![背景验证](docs/images/validation-backgrounds.svg)

## 从这里开始

### ChatGPT、Claude 或其他聊天模型

普通的单张图片需求，上传原图后，直接使用短提示：

- [聊天短提示](prompts/teams-emoji-quick.zh-CN.md)

这是默认路径。它要求模型直接处理图片、不要输出长篇流程说明，并以简短回复返回可下载文件。

只有在结果失败、需要排查限制、或要比较不同工具支持度时，才阅读完整的 [ChatGPT / Claude 使用指南](docs/CHATGPT_CLAUDE_GUIDE.md)。

### 本地 Python 或具备文件操作能力的 Agent

重复处理或需要完整技术规范时，使用 [`SKILL.md`](SKILL.md) 和仓库中的 helper。

```bash
git clone https://github.com/JMok999/teams-emoji-alpha-cleanup-skill.git
cd teams-emoji-alpha-cleanup-skill
python -m pip install -r requirements.txt
python scripts/clean_teams_emoji.py input.jpg input_teams_emoji_256.webp
```

## 一个正式 Skill，加一个可选 Prompt Pack

- [`SKILL.md`](SKILL.md)：原图透明处理、文件检查与 Teams 导出规则。
- [`prompts/teams-emoji-creator-prompts.zh-CN.md`](prompts/teams-emoji-creator-prompts.zh-CN.md)：可选的原创工作场景反应表情 Prompt Pack。

Prompt Pack 不是第二个 Skill，只用于创意探索。生成概念图不自动等于 Teams 成品；选定图片后，仍需通过正式清理流程才能交付。

## 选择合适的使用方式

| 目标 | 使用方式 | 接受标准 |
|---|---|---|
| 创作新的反应表情概念 | [Prompt Pack](prompts/teams-emoji-creator-prompts.zh-CN.md) | 只用于创意，不自动是 Teams 文件 |
| 保留已有表情并去除背景 | [`SKILL.md`](SKILL.md) | 主体保持与原图一致 |
| 在 ChatGPT 或 Claude 中处理单张图片 | [聊天短提示](prompts/teams-emoji-quick.zh-CN.md) | 只接受实际能在 Teams 使用的下载文件 |
| 重复或技术型处理 | Python helper 或具备文件操作能力的 Agent | 运行文件检查与视觉验证 |

## 输出标准

| 项目 | 要求 |
|---|---|
| 文件 | WEBP |
| 画布 | 256 × 256 px |
| 透明度 | 能检查元数据时必须是真实 Alpha |
| 留白 | 约 8–12% 透明边距 |
| 主体 | 完整、居中、不可重新设计 |
| 边缘 | 无白框、白边、灰边或棋盘格残留 |
| 检查背景 | `#FFFFFF`、`#ECEEF6`、`#242424`、`#000000` |

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
- 聊天工具能返回下载文件但无法显示元数据时，请先上传 Teams 测试，再称为已验证。

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
│  ├─ teams-emoji-creator-prompts.md
│  └─ teams-emoji-creator-prompts.zh-CN.md
├─ scripts/
│  └─ clean_teams_emoji.py
└─ tests/
   ├─ generate_fixtures.py
   ├─ test_helper.py
   ├─ SELF_TEST.md
   └─ SELF_TEST.zh-CN.md
```

## License

当前尚未加入 License。准备对外分发或接受外部贡献前，请补充 License。
