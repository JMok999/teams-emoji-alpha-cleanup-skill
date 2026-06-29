Teams Emoji Alpha Cleanup Skill
English · 中文
A practical image-cleanup skill and Python helper for converting uploaded emojis, stickers, avatars, and simple icons into Microsoft Teams-ready custom emoji.
It focuses on the failure that matters most in Teams: a file that looks transparent in a local viewer but still shows a white box, white halo, gray fringe, or checkerboard residue after upload.
> **Primary output:** a centered **256 × 256 lossless WEBP** with a real RGBA alpha channel, smooth anti-aliased edges, and no background contamination.
---
Why this exists
Many image generators and quick background-removal tools produce an image that appears transparent, but the file may still contain one or more of the following:
a baked white or checkerboard background
hidden white matte pixels near the edge
semi-transparent white halos around the subject
a rectangular transparent residue
global white-pixel deletion that accidentally removes eye whites, highlights, teeth, or logos
a face or icon cropped too tightly for Teams
Microsoft Teams makes these issues unusually visible because custom emojis are displayed on light chat bubbles, dark interface areas, and compact reaction surfaces.
This project uses edge-connected background removal instead of globally deleting a color. That means an exterior white background can be removed while intentional white details inside the emoji remain intact.
---
Before / after
The reference below shows the type of visual problem this skill is designed to solve: a white-backed source asset versus a real transparent output tested on Teams-like surfaces.
![Before and after reference](docs/images/before-after-teams.png)
Validation surfaces
Every final asset should be inspected on white, Teams-like light chat bubbles, dark gray, and black. A clean result should not reveal a white rectangle, light halo, colored outline, or checkerboard texture on any of them.
![Background validation reference](docs/images/validation-backgrounds.png)
---
What the skill guarantees
Requirement	Standard
Output format	Lossless WEBP
Canvas	256 × 256 px by default
Transparency	Real RGBA alpha channel
Composition	Subject centered with roughly 8–12% transparent padding
Subject visibility	Full subject kept inside the canvas; no accidental crop
Edge quality	Smooth anti-aliasing with edge color decontamination
Internal white details	Preserved whenever they are not connected to the outer background
Background	Alpha = 0 outside the subject; no baked checkerboard or white square
Teams readiness	Checked on light and dark preview backgrounds
---
Repository layout
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
`SKILL.md` — instructions for Codex, agents, or repeatable image-editing workflows.
`scripts/clean_teams_emoji.py` — command-line tool for flat or near-flat backgrounds.
`docs/images/` — reference images used in this README.
---
English
Best use cases
Use the included script when the source image is an emoji, sticker, icon, avatar, or flat illustration with a background that is connected to the outer image edge, such as:
white, black, or solid-color background
simple gradient background
a small emoji copied from chat or a web page
icon or sticker with intentional white eye areas / highlights
simple logo or mascot with a clean outer boundary
Use a different method when
The script is intentionally conservative. For these cases, use semantic segmentation or manually provide a refined mask first:
photographic backgrounds with people, buildings, or detailed scenes
hair, fur, glass, smoke, or translucent fabric against a complex background
subject touching the original canvas edge
background colors very similar to the subject edge
multiple separate subjects that must be preserved independently
After a semantic mask is created, follow the same alpha cleanup and validation requirements in `SKILL.md`.
Quick start
1. Clone or download this repository
```bash
git clone https://github.com/JMok999/teams-emoji-alpha-cleanup-skill.git
cd teams-emoji-alpha-cleanup-skill
```
2. Create an optional virtual environment
Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```
macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```
3. Install the dependency
```bash
pip install -r requirements.txt
```
4. Process an image
```bash
python scripts/clean_teams_emoji.py input.webp output_teams_emoji_256.webp
```
Example:
```bash
python scripts/clean_teams_emoji.py sly-smile.webp sly-smile_teams_emoji_256.webp
```
The tool saves:
one 256 × 256 transparent lossless WEBP
a preview folder beside the output file, containing the result composited on white, Teams-like light gray, dark gray, and black
Command options
```bash
python scripts/clean_teams_emoji.py INPUT_IMAGE OUTPUT.webp \
  --size 256 \
  --padding 0.10 \
  --tolerance 34 \
  --edge-softness 0.55
```
Option	Default	Purpose
`--size`	`256`	Final square canvas size in pixels.
`--padding`	`0.10`	Transparent margin as a fraction of the canvas. Recommended range: `0.08`–`0.12`.
`--tolerance`	`34`	How close a border pixel must be to the estimated background color before it is classified as exterior background. Increase slowly for uneven flat backgrounds.
`--edge-softness`	`0.55`	Small alpha blur for natural anti-aliasing. Reduce for crisp pixel art; increase carefully for soft illustrated edges.
How it works
Samples the source image border to estimate the exterior background color.
Flood-fills only matching pixels connected to an outer canvas edge.
Inverts that exterior-background mask to build the subject alpha.
Applies a narrow alpha smoothing pass.
Decontaminates semi-transparent edge pixels so they do not retain white-background color.
Crops to the visible subject, scales it proportionally, and centers it in a 256 × 256 transparent canvas.
Validates that the corners are fully transparent.
Exports lossless WEBP and saves background-check previews.
Teams upload checklist
Before uploading the output to Microsoft Teams, confirm:
[ ] File extension is `.webp`
[ ] Canvas is `256 × 256`
[ ] The emoji is fully visible, including chin, ears, hands, dots, and accents
[ ] Corners are transparent, not white
[ ] The preview looks clean on both light and dark surfaces
[ ] No screenshot or checkerboard image was exported instead of true transparency
Troubleshooting
Teams still shows a white box
Likely causes:
The uploaded file was converted to JPG or flattened by another app.
The file contains a baked white/checkerboard background.
White edge contamination remains in semi-transparent pixels.
You uploaded an older Teams custom emoji with the same name.
Try this:
Upload the file produced directly by the script; do not screenshot, copy-paste, or re-export it through Photos.
Use a new emoji name in Teams so the previous cached asset is not reused.
Open the generated preview files and inspect the dark-background version. Any pale edge visible there may need a lower `--edge-softness` or better source segmentation.
Confirm the source has a flat, exterior-connected background. Use semantic masking for complex images.
Important white parts disappear
Do not use a global “remove white” tool. This script keeps white details that are enclosed by the subject because it removes only background connected to the outer edge.
The edge looks too harsh
Increase `--edge-softness` gradually, for example:
```bash
python scripts/clean_teams_emoji.py input.webp output.webp --edge-softness 0.8
```
The edge looks too soft or glowy
Reduce `--edge-softness`, for example:
```bash
python scripts/clean_teams_emoji.py input.webp output.webp --edge-softness 0.25
```
The subject is too small or too close to the edge
Adjust `--padding`:
```bash
# More surrounding space
python scripts/clean_teams_emoji.py input.webp output.webp --padding 0.12

# Larger subject, less surrounding space
python scripts/clean_teams_emoji.py input.webp output.webp --padding 0.08
```
---
中文
这个 Skill 是做什么的？
这个 Skill 用于把用户上传的表情包、头像、贴纸、图标或简单插画，处理成适合上传至 Microsoft Teams 自定义 Emoji 的文件。
它重点解决一个常见问题：图片在本地看起来已经透明，但上传到 Teams 后却出现白底、白框、白色光晕、灰边，或把透明棋盘格一起显示出来。
最终目标是输出一张：
256 × 256 px
Lossless WEBP
真实 RGBA Alpha 透明通道
边缘平滑，不带白边或灰边
主体完整，不裁切嘴巴、下巴、耳朵、手部、问号、省略号等元素
可以适配 Teams 浅色和深色界面
适用场景
以下情况建议直接使用脚本：
表情图片是白底、黑底、纯色底或简单渐变底
原图是聊天截图、网页表情、简单贴纸或头像
表情内部有眼白、反光、牙齿、白色 Logo、白色高光等细节
你不希望“去白底”时把眼白或反光一起删掉
你需要上传到 Teams 的 Custom Emoji
不适用或需要先抠图的场景
以下情形建议先通过 AI 语义分割或人工蒙版抠图，再按照本 Skill 的标准做边缘清理与导出：
复杂照片背景，例如办公室、人群、街景、室内环境
发丝、毛发、烟雾、玻璃、透明材质或复杂阴影
主体贴着原图边缘
背景颜色和主体边缘颜色非常接近
多个主体需要被分别保留
快速开始
1. 下载或 Clone 项目
```bash
git clone https://github.com/JMok999/teams-emoji-alpha-cleanup-skill.git
cd teams-emoji-alpha-cleanup-skill
```
2. 安装依赖
```bash
pip install -r requirements.txt
```
3. 处理图片
```bash
python scripts/clean_teams_emoji.py input.webp output_teams_emoji_256.webp
```
例如：
```bash
python scripts/clean_teams_emoji.py xiaohua.webp xiaohua_teams_emoji_256.webp
```
处理完成后会得到：
一张可上传 Teams 的 `256 × 256` 透明 WEBP。
一个预览文件夹，里面会自动生成白底、Teams 浅色气泡、深灰和黑色背景的检查图。
核心处理逻辑
这个脚本不会简单执行“删除所有白色像素”。
它的处理方式是：
从图片四周取样，估计外部背景颜色。
只删除与四周背景连通的区域。
保留被表情主体包围的白色区域，例如眼白、反光、牙齿、白色图案。
对边缘建立平滑 Alpha 蒙版。
清除半透明边缘中残留的白色蒙版污染，避免 Teams 出现白边或灰边。
自动将主体缩放并居中到 `256 × 256` 透明画布。
检查四个角是否为真正透明。
输出 lossless WEBP，并生成不同背景下的预览文件。
Teams 上传前检查清单
上传前请确认：
[ ] 文件是 `.webp`，不是 JPG 或截图
[ ] 文件尺寸是 `256 × 256`
[ ] 四个角是透明，不是白色
[ ] 表情主体没有被裁切
[ ] 白底、浅灰 Teams 气泡、深灰、黑底预览中都没有白框、白边、灰边或棋盘格
[ ] 上传时不要经过 Photos、截图工具或聊天软件二次转存
[ ] Teams 内建议用新 Emoji 名称测试，避免读取旧缓存
常见问题
1. 明明图片透明，为什么 Teams 还是显示白底？
可能原因包括：
图片并不是真透明，只是被画上了棋盘格或白色背景。
图片边缘残留了半透明白色像素；在深色或浅色聊天气泡中会变成白边。
图片经过 JPG、Photos、截图或复制粘贴流程后，透明通道被移除。
Teams 显示的是同名旧 Emoji 的缓存。
建议直接上传脚本生成的 WEBP，不要重新截图或另存。若已经上传同名 Emoji，请改一个新名称再测试。
2. 为什么不能只写“transparent background”？
因为“透明背景”只是视觉描述，不等于文件真的拥有正确的 Alpha 通道。
为了避免 Teams 出现白底，必须同时做到：
外部背景像素 Alpha = `0`
透明棋盘格没有被生成进图片
半透明边缘不携带白色底图污染
输出文件没有被保存为不支持透明的格式
3. 表情里的眼白或反光会不会被误删？
不会，前提是它们被主体本身包围。脚本只移除与画布四周相连的背景区域，而不是全局删除白色。
4. 表情边缘太硬或太糊怎么办？
使用下面两个参数微调：
```bash
# 边缘更平滑
python scripts/clean_teams_emoji.py input.webp output.webp --edge-softness 0.8

# 边缘更清晰
python scripts/clean_teams_emoji.py input.webp output.webp --edge-softness 0.25
```
5. 表情太小或离边缘太近怎么办？
使用 `--padding`：
```bash
# 留更多透明空白，主体更小
python scripts/clean_teams_emoji.py input.webp output.webp --padding 0.12

# 主体更大，但仍保留安全边距
python scripts/clean_teams_emoji.py input.webp output.webp --padding 0.08
```
---
For Codex / Agent use
Read `SKILL.md` before performing the task. It defines the non-negotiable image-editing rules, segmentation method selection, alpha-matte cleanup requirements, background validation steps, and delivery criteria.
License
No license file is included yet. Add a license before redistributing or accepting outside contributions.
