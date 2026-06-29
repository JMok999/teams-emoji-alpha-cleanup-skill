# ChatGPT / Claude 使用指南

这份指南适合主要使用 ChatGPT、Claude 或其他聊天式 GenAI 的同事。

它的目标不是让聊天模型“画一张看起来像的表情”，而是尽可能让模型遵守原图编辑、透明背景和 Teams 文件规格。更重要的是：当聊天界面做不到真实图片编辑或无法导出可验证文件时，应该明确停止，而不是输出一张看似成功的新图。

## 先理解限制

不是每个聊天模型、免费方案或网页界面都能做到以下全部事情：

1. 读取 GitHub 链接中的 Skill 内容。
2. 对上传原图进行像素级编辑，而不是重新生成。
3. 导出可下载的、带真实 Alpha 通道的 lossless WEBP。
4. 验证文件确实为 256 × 256，且透明背景没有白边。

因此，**只贴 GitHub 链接并要求“按 Skill 做”并不可靠。** 如果模型没有真正读到 `SKILL.md`，或只能生成一张预览图，不能把它视为完成。

## 推荐操作方式

1. 下载或保存仓库中的 `SKILL.md`。
2. 准备需要处理的原始图片文件。
3. 在 ChatGPT、Claude 或其他聊天模型中，同时上传：
   - 原始图片
   - `SKILL.md`
4. 粘贴下面的指令。
5. 只有在模型提供可下载文件时才继续检查。没有可下载的 WebP 文件时，结果仅能算视觉预览，不算 Teams 成品。

## 可直接复制的指令

```text
Read the uploaded SKILL.md completely before doing anything.

Use the uploaded image as the exact source. This is a source-pixel image-editing and technical asset-export task, not a text-to-image generation task.

Do not redraw, restyle, reinterpret, enhance creatively, or generate a replacement emoji. Preserve the original subject exactly.

First confirm that you can edit the supplied source image and return a downloadable 256 × 256 lossless WEBP with a real RGBA alpha channel. If you cannot verify that capability, do not generate a substitute image. Reply only that a verified Teams-ready export is unsupported in this environment.

If the capability is available, follow SKILL.md exactly. Before delivery, verify:
- 256 × 256 px
- lossless WEBP
- real RGBA alpha channel
- outer canvas border alpha = 0
- 8–12% transparent padding
- no white box, white halo, gray fringe, checkerboard, or opaque background
- output is an edit of the uploaded source image, not a newly generated illustration

Return the downloadable final file only after those checks pass.
```

## 正确行为与失败信号

### 可以继续的信号

- 模型确认已读取上传的 `SKILL.md`。
- 模型明确把任务称为“编辑原图 / 移除背景”，而不是“生成一个表情”。
- 模型说明会输出文件，而不是只有对话中的图片预览。
- 模型能够解释如何验证 Alpha、尺寸和 WebP。

### 应该停止的信号

- 模型说无法读取 GitHub 链接，但随后仍直接生成图片。
- 模型生成了新的 3D、插画或不同表情风格。
- 结果带渐变、纯色、白色或棋盘格背景。
- 模型只显示聊天内图片预览，无法给出文件。
- 模型把“看起来透明”当作“已经有 RGBA Alpha”。
- 模型声称完成，却无法确认 WebP、尺寸或透明通道。

## 最终验证清单

拿到文件后，至少检查：

- 文件扩展名是否为 `.webp`
- 是否为 256 × 256 px
- 上传 Teams 后是否出现白框、白边或灰边
- 在白底、Teams 浅色、深灰和黑底上是否都干净
- 主体是否与原图一致，而不是被重新设计

## 可靠性建议

| 使用方式 | 适合用途 | 结果可信度 |
|---|---|---|
| 只贴 GitHub 链接 | 让模型了解项目大概用途 | 低 |
| 上传原图 + `SKILL.md` | 测试聊天模型能否遵守编辑约束 | 中 |
| 使用 Python helper 或 Codex / Agent | 生成并验证真实 Teams 文件 | 高 |

聊天模型可以作为体验和前期测试工具；需要稳定交付给 Teams 使用时，优先使用仓库中的 Python helper 或具备文件操作能力的 Agent。
