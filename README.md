# Teams Emoji Alpha Cleanup Skill

[English](#english) · [中文](#中文)

Convert emojis, stickers, avatars, and simple icons into **Microsoft Teams-ready custom emoji** with a clean transparent background.

> **Target output:** 256 × 256 lossless WEBP, real RGBA alpha, smooth anti-aliased edges, preserved internal white details, and no white box or halo.

## Preview / 预览

### Before → After / 处理前 → 处理后

**EN:** A file can look transparent locally but still show a white rectangle in Teams. This workflow removes only the exterior-connected background and keeps intended white details inside the emoji.

**中文：** 图片在本地看似透明，上传 Teams 后仍可能出现白色方框。本流程只移除与画布边缘连通的背景，同时保留眼白、反光、牙齿等内部白色细节。

![Before and after](docs/images/before-after-teams.svg)

### Validation Backgrounds / 背景验证

**EN:** A Teams-ready emoji should remain clean on light and dark surfaces. No white box, white halo, colored fringe, or checkerboard pattern should be visible.

**中文：** 合格的 Teams 表情在浅色和深色背景下都应保持干净，不应出现白框、白边、彩色边缘或棋盘格。

![Validation backgrounds](docs/images/validation-backgrounds.svg)

## Choose the right path / 选择合适的使用方式

| Your situation / 使用场景 | Recommended path / 建议方式 | Reliability / 可靠性 |
|---|---|---|
| You mainly use ChatGPT, Claude, or another chat-based GenAI / 主要使用 ChatGPT、Claude 等聊天模型 | Upload the original image **and** `SKILL.md`, then follow [ChatGPT / Claude 使用指南](docs/CHATGPT_CLAUDE_GUIDE.md) | Medium: only accept a downloadable file that passes verification |
| You can run Python locally / 可在本地运行 Python | Use the included helper script | High for flat or nearly flat backgrounds |
| You use Codex or another file-capable agent / 使用 Codex 或具备文件操作能力的 Agent | Give it the source image and `SKILL.md`, then require technical verification | High when the validation checks are performed |

> A GitHub link alone is not proof that a chat model has read the Skill. For ChatGPT or Claude, upload `SKILL.md` with the original image. Do not accept a newly generated illustration, a chat preview, or a checkerboard mockup as a Teams-ready file.

## What this solves / 解决的问题

- White squares or boxes around custom emoji in Teams
- White or gray halos around the subject edge
- Checkerboard transparency previews baked into the image
- Global “remove white” operations that delete eye whites, highlights, teeth, or logos
- Tight crops that cut off faces, chins, hands, dots, or accents
- WEBP files that look transparent but were flattened during export
- Teams 自定义表情出现白框、白底、白边或灰边
- 透明棋盘格被直接生成或保存进图片
- 全局“去白色”误删眼白、反光、牙齿或 Logo
- 看似透明的 WEBP 在导出时被压平为不透明背景

## Quick start: Python helper / 快速开始：Python 工具

```bash
git clone https://github.com/JMok999/teams-emoji-alpha-cleanup-skill.git
cd teams-emoji-alpha-cleanup-skill
python -m pip install -r requirements.txt
python scripts/clean_teams_emoji.py input.jpg input_teams_emoji_256.webp
```

The helper accepts static raster images readable by Pillow, including JPG, PNG, WEBP, BMP, TIFF, and the first frame of GIF files.

工具可处理 Pillow 能读取的静态栅格图片，包括 JPG、PNG、WEBP、BMP、TIFF，以及 GIF 的第一帧。

### Optional parameters / 可选参数

```bash
python scripts/clean_teams_emoji.py INPUT_IMAGE OUTPUT.webp \
  --size 256 \
  --padding 0.10 \
  --tolerance 34 \
  --edge-softness 0.55
```

| Option | Default | Meaning / 说明 |
|---|---:|---|
| `--size` | `256` | Final square canvas size / 最终画布尺寸 |
| `--padding` | `0.10` | Transparent margin / 透明边距，建议 0.08 至 0.12 |
| `--tolerance` | `34` | Exterior background matching tolerance / 外部背景识别容差 |
| `--edge-softness` | `0.55` | Alpha-edge smoothing amount / Alpha 边缘平滑程度 |

## ChatGPT / Claude users / ChatGPT 与 Claude 用户

Read [ChatGPT / Claude 使用指南](docs/CHATGPT_CLAUDE_GUIDE.md) before testing this Skill in a chat-only environment.

The guide includes a copy-ready instruction and clear stop conditions. It is designed to prevent a common false success: a model generates a new emoji with an opaque or decorative background, then presents it as though it were an edited, transparent Teams asset.

使用聊天模型前，请先阅读 [ChatGPT / Claude 使用指南](docs/CHATGPT_CLAUDE_GUIDE.md)。其中提供了可直接复制的指令、正确行为与失败信号，避免模型重新画一张相似表情，再把带背景的预览图误称为透明 Teams 文件。

## Output standard / 输出标准

| Item / 项目 | Standard / 标准 |
|---|---|
| Format / 格式 | Lossless WEBP |
| Canvas / 画布 | Exactly 256 × 256 px / 必须为 256 × 256 px |
| Transparency / 透明度 | Real RGBA alpha channel / 真实 RGBA Alpha 通道 |
| Padding / 边距 | About 8–12% transparent margin / 约 8–12% 透明留白 |
| Subject / 主体 | Complete, centered, and not redrawn / 完整居中且不可重绘 |
| Edge quality / 边缘 | Smooth, decontaminated, no white or gray halo / 平滑、无白边与灰边 |
| Validation / 验证 | `#FFFFFF`, `#ECEEF6`, `#242424`, `#000000` / 白底、Teams 浅色、深灰、黑底 |

## How it works / 核心逻辑

1. Inspect the source and choose flat-background segmentation, semantic segmentation, or manual masking.
2. Remove only exterior background connected to the image edge.
3. Preserve enclosed white details such as eye whites, gloss, teeth, and logos.
4. Build a clean alpha matte and decontaminate partially transparent edges.
5. Fit the full subject into a 256 × 256 canvas with safe padding.
6. Verify the actual exported file and inspect background previews.

1. 检查原图，并选择边缘连通分割、语义分割或人工蒙版。
2. 只删除与图片边缘连通的外部背景。
3. 保留眼白、反光、牙齿、Logo 等被主体包围的白色细节。
4. 建立干净的 Alpha 蒙版，并清除半透明边缘的白色蒙版残留。
5. 将完整主体放入带安全留白的 256 × 256 画布。
6. 验证实际导出的文件，并检查不同背景预览。

## Repository layout / 项目结构

```text
teams-emoji-alpha-cleanup-skill/
├─ README.md
├─ SKILL.md
├─ requirements.txt
├─ docs/
│  ├─ CHATGPT_CLAUDE_GUIDE.md
│  └─ images/
│     ├─ before-after-teams.svg
│     └─ validation-backgrounds.svg
└─ scripts/
   └─ clean_teams_emoji.py
```

## Source of truth / 规则来源

`SKILL.md` is the authoritative execution contract for agents. It includes dependencies, supported inputs, default parameters, source-access checks, fallback rules, filename derivation, and mandatory technical acceptance checks.

`SKILL.md` 是 Agent 的唯一执行规范，涵盖依赖、支持格式、默认参数、源文件可用性、fallback、文件命名与技术验收条件。

## Limitations / 限制

- The reference helper is optimized for flat or nearly flat backgrounds.
- Complex photographic scenes, hair, fur, glass, smoke, or translucent materials need semantic segmentation or manual mask refinement.
- A tool that cannot produce and verify a genuine transparent WEBP must not claim the output is Teams-ready.
- 聊天模型中的图片预览不等于真实透明文件；没有可验证的下载文件，就不应视为最终成品。

## License

No license file is included yet. Add a license before redistributing or accepting outside contributions.
