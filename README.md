# Teams Emoji Alpha Cleanup Skill

[English](#english) · [中文](#中文)

Convert emojis, stickers, avatars, and simple icons into Microsoft Teams-ready custom emoji with a clean transparent background.

**Target output:** 256 × 256 lossless WEBP, real RGBA alpha, smooth anti-aliased edges, and no white box or halo.

## Preview / 预览

### Before → After / 处理前 → 处理后

**EN:** A file can look transparent locally but still show a white rectangle in Teams. This workflow removes only the outer connected background and keeps intentional white details inside the emoji.

**中文：** 图片在本地看似透明，上传 Teams 后仍可能出现白色方框。本流程只移除与画布边缘连通的背景，同时保留眼白、反光、牙齿等内部白色细节。

![Before and after](docs/images/before-after-teams.svg)

### Validation Backgrounds / 背景验证

**EN:** A Teams-ready emoji should remain clean on light and dark surfaces. No white box, white halo, colored fringe, or checkerboard pattern should be visible.

**中文：** 合格的 Teams 表情在浅色和深色背景下都应保持干净，不应出现白框、白边、彩色边缘或棋盘格。

![Validation backgrounds](docs/images/validation-backgrounds.svg)

## What this solves / 解决的问题

- White squares or boxes around custom emoji in Teams
- White or gray halos around the subject edge
- Checkerboard transparency previews baked into the image
- Global “remove white” operations that delete eye whites, highlights, teeth, or logos
- Tight crops that cut off faces, chins, hands, dots, or accents
- Teams 自定义表情出现白框或白底
- 主体边缘出现白边或灰边
- 透明棋盘格被直接生成或保存进图片
- 全局“去白色”误删眼白、反光、牙齿或 Logo

## Output standard / 输出标准

| Item / 项目 | Standard / 标准 |
|---|---|
| Format / 格式 | Lossless WEBP |
| Canvas / 画布 | 256 × 256 px by default / 默认 256 × 256 px |
| Transparency / 透明度 | Real RGBA alpha channel / 真实 RGBA Alpha 通道 |
| Padding / 边距 | About 8–12% transparent margin / 约 8–12% 透明留白 |
| Validation / 验证 | White, Teams-like light gray, dark gray, black / 白底、Teams 浅色、深灰、黑底 |

## Quick start / 快速开始

```bash
git clone https://github.com/JMok999/teams-emoji-alpha-cleanup-skill.git
cd teams-emoji-alpha-cleanup-skill
pip install -r requirements.txt
python scripts/clean_teams_emoji.py input.webp output_teams_emoji_256.webp
```

Example / 示例：

```bash
python scripts/clean_teams_emoji.py sly-smile.webp sly-smile_teams_emoji_256.webp
```

The script creates one transparent 256 × 256 WEBP and a preview folder for white, Teams-like light gray, dark gray, and black backgrounds.

脚本会生成一张 256 × 256 的透明 WEBP，以及白底、Teams 浅色、深灰和黑底预览文件夹。

## Options / 参数

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
| `--edge-softness` | `0.55` | Alpha smoothing amount / Alpha 边缘平滑程度 |

## How it works / 核心逻辑

1. Samples border pixels to estimate the exterior background color.
2. Removes only matching pixels connected to the canvas edge.
3. Preserves enclosed white details such as eye whites and highlights.
4. Smooths the alpha edge and removes white matte contamination.
5. Fits the full subject into a centered 256 × 256 transparent canvas.
6. Exports lossless WEBP and creates validation previews.

1. 从图片四周取样，估计外部背景颜色。
2. 只删除与画布边缘连通的背景区域。
3. 保留被主体包围的眼白、反光、牙齿等白色细节。
4. 平滑 Alpha 边缘并清除白色蒙版残留。
5. 将完整主体居中放入 256 × 256 透明画布。
6. 输出 lossless WEBP，并生成验证预览图。

## Teams upload checklist / Teams 上传前检查

- [ ] Upload the generated `.webp` directly. Do not screenshot or re-export it.
- [ ] Confirm the canvas is 256 × 256 and the full subject is visible.
- [ ] Check the dark-background preview for pale fringes.
- [ ] Test with a new Teams emoji name to avoid cached older assets.
- [ ] 直接上传脚本生成的 `.webp`，不要截图或二次另存。
- [ ] 确认尺寸为 256 × 256，主体没有被裁切。
- [ ] 检查深色背景预览是否仍有白边。
- [ ] 使用新的 Emoji 名称测试，避免 Teams 缓存旧版本。

## Common issues / 常见问题

**Teams still shows a white box / Teams 仍显示白底：** Upload the script-produced WEBP directly. Do not use JPG, screenshots, or a file with baked checkerboard pixels. Try a new emoji name if Teams is caching an older asset.

**Important white details disappeared / 眼白或反光被误删：** Do not use global “remove white”. This script removes only background connected to the outer canvas edge.

**Edge too harsh or too soft / 边缘太硬或太糊：**

```bash
# Softer / 更平滑
python scripts/clean_teams_emoji.py input.webp output.webp --edge-softness 0.8

# Sharper / 更清晰
python scripts/clean_teams_emoji.py input.webp output.webp --edge-softness 0.25
```

## For Codex / Agent use

Read [`SKILL.md`](SKILL.md) before using this workflow.
