# Self Test / 自测说明

[English](SELF_TEST.md) · [中文](SELF_TEST.zh-CN.md)

此目录提供两类验证：Python helper 的确定性回归测试，以及聊天模型的人工兼容性测试。

## 运行自动化 helper 测试

```bash
python -m pip install -r requirements.txt
python tests/test_helper.py
```

测试会在临时目录中生成图片素材，不会提交二进制测试图片到仓库。

自动检查以下内容：

- 能够解码的 WEBP 文件
- 尺寸必须为 256 × 256
- 文件包含 Alpha 通道
- 画布最外圈像素完全透明
- 主体区域非空
- 自动生成白底、Teams 浅色、深灰、黑底四张预览图
- 白底测试图中的内部白色细节仍被保留
- 动画 GIF 只使用第一帧并输出静态 WebP
- 非 `.webp` 输出路径会被拒绝

## 测试图目录

`generate_fixtures.py` 会生成以下固定测试输入：

| 文件 | 测试目的 | 预期处理 |
|---|---|---|
| `01-white-background-internal-white.png` | 白底与内部白色细节 | 只移除外部白色，保留内部白色区域。 |
| `02-existing-alpha.png` | 原图已经有 Alpha | 保留原图透明信息，并输出合格的 Teams 画布。 |
| `03-dark-background.png` | 深色纯色背景 | 使用边缘连通方式移除背景。 |
| `04-near-background-color.png` | 背景与主体色接近 | 人工检查案例。不可靠盲目提高 tolerance 解决。 |
| `05-soft-edge.png` | 抗锯齿插画边缘 | 人工检查边缘平滑度与是否有白边。 |
| `06-subject-near-edge.png` | 主体接近画布边缘 | 人工检查是否误裁切或损失蒙版。 |
| `07-animated-first-frame.gif` | 动画来源图片 | 只处理第一帧，并输出静态 WebP。 |

## 人工视觉检查

每个完成文件都应在以下背景下检查：

- `#FFFFFF`
- `#ECEEF6`
- `#242424`
- `#000000`

出现以下任何情况都应判定失败：

- 白框或矩形残留
- 白边或灰边
- 彩色边缘
- 棋盘格被烘焙进图片
- 边缘锯齿明显
- 内部白色细节丢失
- 主体被错误裁切

## 聊天模型兼容性测试

ChatGPT、Claude 与类似工具并不是确定性的测试运行环境。请使用同一批测试图进行人工测试，并记录：

- 测试日期、模型与方案
- 原图是否被当作可编辑来源
- 是否返回可下载文件
- 文件类型与尺寸说明
- 实际上传 Teams 的结果
- 输出是否保留所选原图，而不是被重新设计

日常使用时，请从以下短提示开始：

- [`../prompts/chatgpt-teams-emoji-quick-prompt.en.md`](../prompts/chatgpt-teams-emoji-quick-prompt.en.md)
- [`../prompts/chatgpt-teams-emoji-quick-prompt.zh-CN.md`](../prompts/chatgpt-teams-emoji-quick-prompt.zh-CN.md)
