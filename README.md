# Teams Emoji Alpha Cleanup Skill

[English](#english) · [中文](#中文)

Turn emojis, stickers, avatars, and simple icons into **Microsoft Teams-ready custom emoji** without the common white box, white halo, gray fringe, or baked checkerboard background.

> **Output target:** a centered **256 × 256 lossless WEBP** with a real RGBA alpha channel, clean anti-aliased edges, and no background contamination.

---

## Preview

### Before → after

A white-backed source asset can look “transparent” in a viewer while still failing in Teams. The cleaned output removes only the outer connected background, preserving intended white details inside the emoji.

![Before and after](docs/images/before-after-teams.png)

### Validation backgrounds

A Teams-ready emoji should be checked on light and dark surfaces. There should be no rectangular box, white halo, colored fringe, or checkerboard texture.

![Validation backgrounds](docs/images/validation-backgrounds.png)

---

## What this solves

- White squares or boxes around custom emoji in Teams
- White / gray halos around the subject edge
- Checkerboard transparency previews accidentally baked into the file
- Global “remove white” operations that delete eye whites, highlights, teeth, or logos
- Excessively tight crops that cut off a face, chin, hands, dots, or accents
- WEBP files that appear transparent but are actually flattened

## Output standard

| Item | Standard |
|---|---|
| Format | Lossless WEBP |
| Canvas | 256 × 256 px by default |
| Transparency | Real RGBA alpha channel |
| Padding | Around 8–12% transparent margin |
| Edge quality | Smooth anti-aliasing, with edge-color decontamination |
| Internal white details | Preserved when not connected to the outside background |
| Validation | Previewed on white, Teams-like light gray, dark gray, and black |

## Repository layout

```text
teams-emoji-alpha-cleanup-skill/
├─ README.md
├─ SKILL.md
├─ requirements.txt
├─ docs/
│  └─ images/
│     ├─ before-after-teams.png
│     └─ validation-backgrounds.png
└─ scripts/
   └─ clean_teams_emoji.py
```

- `SKILL.md` — reusable instructions for Codex, agents, and image-editing workflows.
- `scripts/clean_teams_emoji.py` — helper for source images with flat or near-flat backgrounds.
- `docs/images/` — README reference images.

---

# English

## Best use cases

Use the script for an emoji, sticker, icon, avatar, mascot, or simple illustration where the background is connected to the outer edge of the image:

- white, black, or solid-color backgrounds
- simple gradients
- chat screenshots and web emojis
- graphics with internal white details such as eye whites, gloss, teeth, or logo elements

## Use a different method first when

Use semantic segmentation or manually refine a mask before using this workflow when the source contains:

- a detailed photographic background
- hair, fur, glass, smoke, translucent material, or complex shadows
- a subject touching the original canvas edge
- background colors extremely close to the edge of the subject
- multiple subjects that must be retained separately

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/JMok999/teams-emoji-alpha-cleanup-skill.git
cd teams-emoji-alpha-cleanup-skill
```

### 2. Create an optional virtual environment

**Windows PowerShell**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the dependency

```bash
pip install -r requirements.txt
```

### 4. Process an image

```bash
python scripts/clean_teams_emoji.py input.webp output_teams_emoji_256.webp
```

Example:

```bash
python scripts/clean_teams_emoji.py sly-smile.webp sly-smile_teams_emoji_256.webp
```

The script creates:

1. One transparent, lossless 256 × 256 WEBP file.
2. A preview folder with the result composited on white, Teams-like light gray, dark gray, and black.

## Options

```bash
python scripts/clean_teams_emoji.py INPUT_IMAGE OUTPUT.webp \
  --size 256 \
  --padding 0.10 \
  --tolerance 34 \
  --edge-softness 0.55
```

| Option | Default | Meaning |
|---|---:|---|
| `--size` | `256` | Final square canvas size. |
| `--padding` | `0.10` | Transparent margin. Recommended: `0.08` to `0.12`. |
| `--tolerance` | `34` | Exterior background matching tolerance. Increase carefully for uneven flat backgrounds. |
| `--edge-softness` | `0.55` | Alpha smoothing amount. Lower it for a sharper edge; raise it slightly for softer art. |

## How it works

1. Samples border pixels to estimate the outer background color.
2. Flood-fills only matching pixels connected to the canvas edge.
3. Builds a subject alpha mask by inverting that exterior-background mask.
4. Applies a narrow smoothing pass for anti-aliased edges.
5. Decontaminates semi-transparent edge pixels so they do not retain white background color.
6. Fits the full visible subject into a centered 256 × 256 transparent canvas.
7. Validates that all corner pixels are fully transparent.
8. Exports lossless WEBP plus background-check previews.

## Teams upload checklist

- [ ] Upload the generated `.webp` directly; do not screenshot or re-export it through Photos.
- [ ] Confirm the canvas is 256 × 256.
- [ ] Confirm the full subject is visible, with no cropped chin, mouth, hands, or accents.
- [ ] Check the generated dark-background preview for pale fringes.
- [ ] Use a new Teams emoji name during testing to avoid showing a cached old asset.

## Troubleshooting

### Teams still shows a white box

Possible causes:

- The image was flattened by a second export or converted to JPG.
- A checkerboard or white background was baked into the source.
- Semi-transparent edges still contain white matte contamination.
- Teams is displaying a cached emoji with the same name.

Try uploading the script-produced WEBP directly under a new emoji name. For complex source images, create a semantic mask first instead of relying on flat-background cleanup.

### Important white details disappeared

Do not use a global “remove white” tool. This project removes only background connected to the outer canvas edge, so enclosed white details should remain intact.

### Edge is too harsh / too soft

```bash
# Softer edge
python scripts/clean_teams_emoji.py input.webp output.webp --edge-softness 0.8

# Sharper edge
python scripts/clean_teams_emoji.py input.webp output.webp --edge-softness 0.25
```

### Subject is too small or too close to the edge

```bash
# More surrounding space
python scripts/clean_teams_emoji.py input.webp output.webp --padding 0.12

# Larger subject with less padding
python scripts/clean_teams_emoji.py input.webp output.webp --padding 0.08
```

---

# 中文

## 这个 Skill 是做什么的？

这个 Skill 用于把用户上传的表情包、头像、贴纸、图标或简单插画，处理成适合上传至 **Microsoft Teams 自定义 Emoji** 的文件。

它重点解决一个常见问题：图片在本地看起来已经透明，但上传到 Teams 后仍出现白底、白框、白色光晕、灰边，或者把透明棋盘格一起显示出来。

最终输出标准：

- **256 × 256 px**
- **Lossless WEBP**
- **真实 RGBA Alpha 透明通道**
- **边缘平滑，没有白边或灰边**
- **主体完整，不裁切嘴巴、下巴、耳朵、手部、问号、省略号等元素**
- **能适配 Teams 浅色和深色界面**

## 适用场景

以下情况可以直接使用脚本：

- 表情图片是白底、黑底、纯色底或简单渐变底
- 原图来自聊天截图、网页表情、简单贴纸或头像
- 表情内部有眼白、反光、牙齿、白色 Logo 或白色高光
- 你不希望“去白底”时把眼白、反光一起删除
- 你需要把图上传为 Teams Custom Emoji

## 不适用或需要先抠图的场景

以下情形建议先用 AI 语义分割或人工蒙版抠图，再按本 Skill 的规则清理边缘和导出：

- 复杂照片背景，例如办公室、人群、街景、室内环境
- 发丝、毛发、烟雾、玻璃、透明材质或复杂阴影
- 主体贴住原图边缘
- 背景颜色与主体边缘颜色非常接近
- 多个主体需要被分别保留

## 快速开始

### 1. 下载或 Clone 项目

```bash
git clone https://github.com/JMok999/teams-emoji-alpha-cleanup-skill.git
cd teams-emoji-alpha-cleanup-skill
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 处理图片

```bash
python scripts/clean_teams_emoji.py input.webp output_teams_emoji_256.webp
```

示例：

```bash
python scripts/clean_teams_emoji.py xiaohua.webp xiaohua_teams_emoji_256.webp
```

处理后会得到：

1. 一张可上传 Teams 的 `256 × 256` 透明 WEBP。
2. 一个预览文件夹，自动生成白底、Teams 浅色气泡、深灰和黑色背景的检查图。

## 核心处理逻辑

此脚本不会简单执行“删除所有白色像素”。它会：

1. 从图片四周取样，估计外部背景颜色。
2. 只删除与画布边缘连通的背景区域。
3. 保留被主体包围的白色区域，例如眼白、反光、牙齿、白色图案。
4. 对边缘建立平滑 Alpha 蒙版。
5. 清除半透明边缘中残留的白色蒙版污染，避免 Teams 显示白边或灰边。
6. 自动把主体缩放、居中到 `256 × 256` 的透明画布。
7. 检查四个角是否为真正透明。
8. 输出 lossless WEBP，并生成不同背景下的验证预览图。

## Teams 上传前检查清单

- [ ] 文件是 `.webp`，不是 JPG 或截图。
- [ ] 文件尺寸是 `256 × 256`。
- [ ] 四个角是透明，不是白色。
- [ ] 表情主体没有被裁切。
- [ ] 白底、Teams 浅灰气泡、深灰和黑底预览中都没有白框、白边、灰边或棋盘格。
- [ ] 上传时不要经过 Photos、截图工具或聊天软件二次转存。
- [ ] Teams 内建议使用一个新 Emoji 名称测试，避免读取旧缓存。

## 常见问题

### 明明图片透明，为什么 Teams 还是显示白底？

常见原因：

- 图片不是真透明，只是画上了白色或棋盘格背景。
- 边缘残留半透明白色像素，在 Teams 中变成白边。
- 图片经过 JPG、Photos、截图或复制粘贴流程后，透明通道被移除。
- Teams 正显示同名旧 Emoji 的缓存。

建议直接上传脚本生成的 WEBP，并使用一个新名称测试。

### 为什么不能只写“transparent background”？

因为“透明背景”只是视觉描述，不代表文件真的拥有正确的 Alpha 通道。要避免 Teams 出现白底，必须同时做到：

- 外部背景像素 Alpha = `0`
- 透明棋盘格没有被生成进图片
- 半透明边缘不携带白色底图污染
- 文件没有被重新保存为不支持透明的格式

### 表情里的眼白或反光会不会被误删？

正常情况下不会。脚本只移除与画布四周相连的背景区域，而不是全局删除白色。

### 表情边缘太硬或太糊怎么办？

```bash
# 边缘更平滑
python scripts/clean_teams_emoji.py input.webp output.webp --edge-softness 0.8

# 边缘更清晰
python scripts/clean_teams_emoji.py input.webp output.webp --edge-softness 0.25
```

### 表情太小或离边缘太近怎么办？

```bash
# 留更多透明空白
python scripts/clean_teams_emoji.py input.webp output.webp --padding 0.12

# 主体更大，但仍保留安全边距
python scripts/clean_teams_emoji.py input.webp output.webp --padding 0.08
```

---

## For Codex / Agent use

Read [`SKILL.md`](SKILL.md) before using this workflow. It defines the image-editing rules, segmentation method selection, alpha-matte cleanup requirements, validation steps, and delivery criteria.

## License

No license file is included yet. Add a license before redistributing or accepting outside contributions.
