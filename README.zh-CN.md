# Teams Emoji Alpha Cleanup Skill

[English](README.md) · [中文](README.zh-CN.md)

## 这个项目做什么

这个仓库只有一个正式 Skill，用于将已有的表情包、头像、贴纸、图标或简单插画，处理成可用于 **Microsoft Teams 自定义 Emoji** 的文件。

这是一个基于原图的编辑流程。它会保留原有主体，而不是重新绘制或改造成另一种风格。

**最终目标：** 一个经过验证的 `256 × 256` lossless WEBP，带有真实 RGBA Alpha 透明通道、干净的抗锯齿边缘、被保留的内部白色细节，并且没有白框或白边。

## 预览

### 处理前 → 处理后

图片在本地看似透明，上传 Teams 后仍可能出现白色方框。本流程只移除与画布边缘连通的背景，同时保留眼白、反光、牙齿等内部白色细节。

![处理前后](docs/images/before-after-teams.svg)

### 背景验证

合格的 Teams 表情在浅色和深色背景下都应保持干净，不应出现白框、白边、彩色边缘或棋盘格。

![背景验证](docs/images/validation-backgrounds.svg)

## 一个正式 Skill，加一个可选 Prompt Pack

这个仓库刻意只保留一个正式 Skill：

- [`SKILL.md`](SKILL.md)：负责原图透明处理、技术验证和 Teams 文件导出。

同时提供一个可选的创作资源：

- [`prompts/teams-emoji-creator-prompts.md`](prompts/teams-emoji-creator-prompts.md)：轻量级的原创工作场景反应表情 Prompt Pack。

Prompt Pack 不是第二个正式 Skill。ChatGPT、Claude 和其他图片生成工具本来就能通过自然语言生成新的视觉概念。它的作用只是让同事更快写出适合工作场景反应表情的提示词，并让一组表情保持更一致的视觉方向。

生成出来的概念图不自动等于可上传 Teams 的文件。选定创作图后，请下载源图，并使用 `SKILL.md` 的正式流程完成透明处理与技术验证。

## 选择合适的使用方式

| 你的目标 | 建议方式 | 可靠性 |
|---|---|---|
| 想创作一个新的表情概念 | 使用可选的 [Prompt Pack](prompts/teams-emoji-creator-prompts.md) | 适合创意探索，不保证可直接上传 Teams |
| 想完整保留已有表情的原貌并去除背景 | 使用 [`SKILL.md`](SKILL.md) 和原图 | 原图保留与透明处理必需流程 |
| 主要使用 ChatGPT、Claude 或其他聊天模型 | 同时上传原图与 `SKILL.md`，再阅读 [ChatGPT / Claude 使用指南](docs/CHATGPT_CLAUDE_GUIDE.md) | 下载文件通过验证前，可靠性有限 |
| 可在本地运行 Python | 使用仓库附带的 helper script | 平面或接近平面背景时可靠性较高 |
| 使用 Codex 或其他具备文件操作能力的 Agent | 提供原图和 `SKILL.md`，并要求进行技术验证 | 完成验证后可靠性较高 |

> 只贴 GitHub 链接，不代表聊天模型真的读过 Skill。不要把重新生成的插画、聊天界面的预览图或棋盘格 mockup 当成可用于 Teams 的文件。

## ChatGPT 与 Claude 用户

在仅使用聊天模型的环境中测试前，请先阅读 [ChatGPT / Claude 使用指南](docs/CHATGPT_CLAUDE_GUIDE.md)。

指南说明了如何同时上传原图与 `SKILL.md`、如何在生成前进行预检、如何识别“看似完成但其实失败”的情况，以及为什么没有可下载、可验证的 WebP 文件时不应接受结果。

## 快速开始

```bash
git clone https://github.com/JMok999/teams-emoji-alpha-cleanup-skill.git
cd teams-emoji-alpha-cleanup-skill
python -m pip install -r requirements.txt
python scripts/clean_teams_emoji.py input.jpg input_teams_emoji_256.webp
```

工具可处理 Pillow 能读取的静态栅格图片，包括 JPG、PNG、WEBP、BMP、TIFF，以及 GIF 的第一帧。

### 可选参数

```bash
python scripts/clean_teams_emoji.py INPUT_IMAGE OUTPUT.webp \
  --size 256 \
  --padding 0.10 \
  --tolerance 34 \
  --edge-softness 0.55
```

| 参数 | 默认值 | 说明 |
|---|---:|---|
| `--size` | `256` | 最终方形画布尺寸。Teams 输出固定为 256 × 256。 |
| `--padding` | `0.10` | 透明边距，建议范围为 0.08 至 0.12。 |
| `--tolerance` | `34` | 外部背景识别容差。 |
| `--edge-softness` | `0.55` | Alpha 边缘平滑程度。 |

## 输出标准

| 项目 | 标准 |
|---|---|
| 格式 | Lossless WEBP |
| 画布 | 必须为 256 × 256 px |
| 透明度 | 真实 RGBA Alpha 通道 |
| 留白 | 约 8–12% 透明边距 |
| 主体 | 完整、居中、不可重绘 |
| 边缘 | 平滑、已清理白色蒙版污染、无白边与灰边 |
| 验证背景 | `#FFFFFF`、`#ECEEF6`、`#242424`、`#000000` |

## 清理流程的工作方式

1. 检查原图，并选择边缘连通分割、语义分割或人工蒙版。
2. 只删除与图片边缘连通的外部背景。
3. 保留眼白、反光、牙齿、Logo 等被主体包围的白色细节。
4. 建立干净的 Alpha 蒙版，并清除半透明边缘的白色蒙版残留。
5. 将完整主体放入带安全留白的 256 × 256 画布。
6. 验证实际导出的文件，并检查不同背景预览。

## 项目结构

```text
teams-emoji-alpha-cleanup-skill/
├─ README.md
├─ README.zh-CN.md
├─ SKILL.md
├─ requirements.txt
├─ docs/
│  ├─ CHATGPT_CLAUDE_GUIDE.md
│  └─ images/
│     ├─ before-after-teams.svg
│     └─ validation-backgrounds.svg
├─ prompts/
│  └─ teams-emoji-creator-prompts.md
└─ scripts/
   └─ clean_teams_emoji.py
```

## 规则来源

`SKILL.md` 是 Agent 的唯一执行规范，其中包含依赖、支持格式、默认参数、源文件可用性、fallback、文件命名与技术验收条件。

## 限制

- 参考 helper 主要适合平面或接近平面背景。
- 复杂照片场景、发丝、毛发、玻璃、烟雾或透明材质，需要语义分割或人工优化蒙版。
- 无法生成并验证真实透明 WEBP 的工具，不应声称结果已经可用于 Teams。
- 聊天模型中的图片预览不等于真实透明文件。

## License

当前尚未加入 License。准备对外分发或接受外部贡献前，请补充 License。
