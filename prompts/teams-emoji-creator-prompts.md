# Teams Emoji Creator Prompt Pack

[English](#english) · [中文](#中文)

# English

## What this is

This is an optional **prompt pack**, not a second formal Skill.

Use it to create original reaction-emoji concepts in ChatGPT, Claude, or another image-generation tool. It helps colleagues start from clearer, more consistent prompts instead of writing every request from scratch.

It does **not** guarantee that the generated image is a Microsoft Teams-ready file. A generated preview can be useful for creative exploration, but it is not a verified 256 × 256 lossless WEBP with real RGBA alpha.

For a production-ready Teams asset, pass the chosen source image through the technical workflow in [`SKILL.md`](../SKILL.md).

## When to use this prompt pack

Use it when you want to create a new visual concept such as:

- acknowledgement, approval, celebration, surprise, confusion, or facepalm reactions
- a themed reaction set for a project, team, or event
- a consistent collection of original 3D, clay, flat, or illustrated emojis
- a concept image that can later be cleaned and converted into a Teams asset

Do not use it when you need to preserve an existing emoji exactly. In that case, use [`SKILL.md`](../SKILL.md) with the original image.

## Basic generation prompt

Copy this template and replace the bracketed fields:

```text
Create one original reaction emoji for workplace chat.

Subject: [emotion, gesture, or situation]
Style: [soft 3D emoji / clay / flat vector / glossy illustration]
Visual direction: [friendly, clean, playful, minimal]
Composition: centered single subject, 1:1 square, generous empty margin around the subject.
Background: simple and low-detail. Do not include interface elements, text, captions, logos, watermarks, frames, or decorative scenes.
Keep the silhouette clear and easy to read at small size.
```

## Starter prompts

### 1. Acknowledged

```text
Create one original workplace reaction emoji that means “acknowledged”.
A friendly character gives a clear thumbs-up with a calm, confident expression.
Soft 3D emoji style, warm lighting, centered single subject, 1:1 square, generous empty margin.
Simple low-detail background. No text, no watermark, no logo, no UI elements.
```

### 2. Great job

```text
Create one original celebration emoji for “great job”.
A cheerful character claps with subtle confetti accents kept away from the outer edge.
Polished clay style, bright but restrained colors, centered single subject, 1:1 square.
No text, no brand references, no watermark, no frame, no interface screenshot.
```

### 3. I am on it

```text
Create one original reaction emoji that means “I am on it”.
A focused character rolls up one sleeve and gives a determined nod.
Clean 3D emoji style, readable at small size, centered composition with clear outer spacing.
Simple background only. No text, no watermark, no logo, no UI elements.
```

### 4. Please wait

```text
Create one original reaction emoji that means “please wait a moment”.
A patient character raises one hand gently with a small hourglass icon beside it.
Minimal soft 3D illustration, centered single subject, 1:1 square, clean silhouette.
No words, no labels, no frame, no watermark, no busy background.
```

### 5. Mind blown

```text
Create one original reaction emoji that means “mind blown”.
A surprised character with wide eyes and a small burst of abstract light above the head.
Glossy emoji style, clean readable shape, centered on a simple low-detail background.
No text, no watermark, no brand logo, no interface elements.
```

### 6. Facepalm

```text
Create one original reaction emoji that means “facepalm”.
A friendly character lightly covers the forehead with one hand, expressive but not dramatic.
Soft clay emoji style, centered subject, 1:1 square, generous margin around all sides.
No text, no watermark, no logo, no decorative scene.
```

### 7. Thank you

```text
Create one original reaction emoji that means “thank you”.
A warm character places both hands together in appreciation with a gentle smile.
Clean modern emoji illustration, centered subject, simple background, 1:1 square.
No text, no frame, no watermark, no brand elements.
```

### 8. Coffee break

```text
Create one original workplace reaction emoji that means “coffee break”.
A relaxed character holding one small coffee cup with a content expression.
Friendly 3D emoji style, centered single subject, clear silhouette, 1:1 square.
Simple background only. No text, no logo, no watermark, no UI elements.
```

## Build a consistent emoji set

For a series, keep these fixed across prompts:

- visual style
- material and lighting
- camera angle
- subject scale and outer margin
- background simplicity
- palette family

Example series instruction:

```text
Use the same visual system for every emoji in this set: friendly soft 3D material, front-facing angle, centered subject, 1:1 square, clean silhouette, 10% outer margin, restrained warm palette, no text or background scene.
```

## Handoff to the cleanup workflow

After you select a generated concept:

1. Download the highest-quality source image available.
2. Do not treat a chat preview or checkerboard display as technical transparency proof.
3. Use [`SKILL.md`](../SKILL.md) and the Python helper to create a verified Teams-ready file.
4. Check the final file on white, Teams-like light gray, dark gray, and black backgrounds.

The final Teams deliverable must be a real 256 × 256 lossless WEBP with verified RGBA alpha. The creative prompt alone does not create that guarantee.

---

# 中文

## 这是什么

这是一个可选的 **Prompt Pack 提示词包**，不是第二个正式 Skill。

它用于在 ChatGPT、Claude 或其他图片生成工具中，快速创建原创的反应表情概念。它的价值是帮助同事以较一致的方式表达需求，而不是每次从零开始写提示词。

它**不保证**生成结果已经是可直接上传 Microsoft Teams 的技术成品。聊天中的生成图可以用于创意探索，但不等于已经得到 `256 × 256`、lossless WEBP、真实 RGBA Alpha 的文件。

当你选定了一张创作图后，请使用 [`SKILL.md`](../SKILL.md) 的技术流程，把它处理成可验证的 Teams 文件。

## 什么时候使用这个 Prompt Pack

以下场景适合使用：

- 想做“收到、赞、庆祝、震惊、疑惑、捂脸”等原创反应表情
- 想为项目、团队或活动建立一套统一风格的表情
- 想测试 3D、黏土、扁平插画等不同视觉方向
- 想先产出概念图，之后再进入透明背景清理与 Teams 导出流程

如果你的目标是**保留一个已有表情的原貌**，请直接使用 [`SKILL.md`](../SKILL.md)，不要使用本 Prompt Pack。

## 基础生成提示词

复制以下模板，替换方括号中的内容：

```text
Create one original reaction emoji for workplace chat.

Subject: [emotion, gesture, or situation]
Style: [soft 3D emoji / clay / flat vector / glossy illustration]
Visual direction: [friendly, clean, playful, minimal]
Composition: centered single subject, 1:1 square, generous empty margin around the subject.
Background: simple and low-detail. Do not include interface elements, text, captions, logos, watermarks, frames, or decorative scenes.
Keep the silhouette clear and easy to read at small size.
```

## 可直接使用的提示词

### 1. 收到 / 已知悉

```text
Create one original workplace reaction emoji that means “acknowledged”.
A friendly character gives a clear thumbs-up with a calm, confident expression.
Soft 3D emoji style, warm lighting, centered single subject, 1:1 square, generous empty margin.
Simple low-detail background. No text, no watermark, no logo, no UI elements.
```

### 2. 做得好

```text
Create one original celebration emoji for “great job”.
A cheerful character claps with subtle confetti accents kept away from the outer edge.
Polished clay style, bright but restrained colors, centered single subject, 1:1 square.
No text, no brand references, no watermark, no frame, no interface screenshot.
```

### 3. 我来处理

```text
Create one original reaction emoji that means “I am on it”.
A focused character rolls up one sleeve and gives a determined nod.
Clean 3D emoji style, readable at small size, centered composition with clear outer spacing.
Simple background only. No text, no watermark, no logo, no UI elements.
```

### 4. 请稍等

```text
Create one original reaction emoji that means “please wait a moment”.
A patient character raises one hand gently with a small hourglass icon beside it.
Minimal soft 3D illustration, centered single subject, 1:1 square, clean silhouette.
No words, no labels, no frame, no watermark, no busy background.
```

### 5. 震惊 / 脑袋爆炸

```text
Create one original reaction emoji that means “mind blown”.
A surprised character with wide eyes and a small burst of abstract light above the head.
Glossy emoji style, clean readable shape, centered on a simple low-detail background.
No text, no watermark, no brand logo, no interface elements.
```

### 6. 捂脸

```text
Create one original reaction emoji that means “facepalm”.
A friendly character lightly covers the forehead with one hand, expressive but not dramatic.
Soft clay emoji style, centered subject, 1:1 square, generous margin around all sides.
No text, no watermark, no logo, no decorative scene.
```

### 7. 谢谢

```text
Create one original reaction emoji that means “thank you”.
A warm character places both hands together in appreciation with a gentle smile.
Clean modern emoji illustration, centered subject, simple background, 1:1 square.
No text, no frame, no watermark, no brand elements.
```

### 8. 咖啡休息

```text
Create one original workplace reaction emoji that means “coffee break”.
A relaxed character holding one small coffee cup with a content expression.
Friendly 3D emoji style, centered single subject, clear silhouette, 1:1 square.
Simple background only. No text, no logo, no watermark, no UI elements.
```

## 制作统一风格的一组表情

同一组表情建议固定以下元素：

- 视觉风格
- 材质和光线
- 镜头角度
- 主体比例与外部留白
- 背景复杂度
- 配色方向

可在每条提示词前加入：

```text
Use the same visual system for every emoji in this set: friendly soft 3D material, front-facing angle, centered subject, 1:1 square, clean silhouette, 10% outer margin, restrained warm palette, no text or background scene.
```

## 进入透明背景处理流程

选定创作图之后：

1. 下载可取得的最高质量源图。
2. 不要把聊天预览或棋盘格显示当成真实透明的证明。
3. 使用 [`SKILL.md`](../SKILL.md) 与 Python helper 生成经过验证的 Teams 文件。
4. 在白底、Teams 浅色、深灰与黑底上检查最终文件。

最终可上传 Teams 的文件必须是**真实的 `256 × 256` lossless WEBP，并且带有已经验证的 RGBA Alpha**。单靠创意提示词不提供这项保证。
