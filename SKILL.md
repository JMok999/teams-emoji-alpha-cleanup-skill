---
name: teams-emoji-alpha-cleanup
description: Convert an accessible user-uploaded raster emoji or icon into a Microsoft Teams-ready 256×256 lossless WEBP using source-faithful editing, true RGBA transparency, clean alpha edges, and export checks. Do not substitute a redesigned image or a screenshot.
---

# Teams Emoji Alpha Cleanup

Use this Skill to turn an existing emoji, sticker, avatar, icon, or simple illustration into a Microsoft Teams custom emoji.

This is an **asset-cleanup and export workflow**. It edits the supplied source image. It does not create a new emoji from a text description.

## Interaction policy: default to silent execution

For normal user requests:

- Do not summarize this Skill.
- Do not explain the algorithm, repeat requirements, or provide a preflight report.
- Do not ask the user to confirm obvious defaults.
- If the source image is accessible, process it directly.
- On success, provide the file link and no more than two short lines.
- On failure, use one concise sentence that states the missing source or capability.

Only give a technical explanation when the user explicitly asks for one.

## Source and result rules

Treat the uploaded image as the source of truth.

- Preserve the subject's proportions, expression, line work, colors, highlights, shadows, and intentional details.
- Do not redraw, restyle, reinterpret, or replace the source with a similar generated emoji.
- Do not treat a chat preview, screenshot, checkerboard mockup, or opaque render as evidence of transparency.
- A GitHub URL alone is not proof that this Skill has been read. Use a local copy or uploaded instructions when a chat tool cannot access the repository.
- If the original image is unavailable as an editable source, stop. Do not create a replacement.

## Supported input

Accept a static raster image readable by Pillow:

- JPG / JPEG
- PNG
- WEBP
- BMP
- TIFF
- GIF: process the first frame only

The final asset is always a static WEBP. SVG, PDF, HEIC, AVIF, and proprietary formats need prior rasterization or a suitable decoder.

## Core output contract

A final validated asset must meet all of the following:

- lossless WEBP
- exactly 256 × 256 px
- real RGBA Alpha channel
- fully transparent background outside the subject
- centered subject with 8–12% transparent outer padding
- complete subject with no accidental crop
- smooth anti-aliased edges with no white or gray halo
- internal white details preserved when not connected to the exterior background
- no baked white, black, colored, or checkerboard background

## Default parameters

| Parameter | Default | Recommended range | Purpose |
|---|---:|---:|---|
| Output size | `256` | Fixed | Final square canvas |
| Padding | `0.10` | `0.08–0.12` | Transparent outer margin |
| Background tolerance | `34` | Adjust gradually | Edge-connected background similarity threshold |
| Edge softness | `0.55` | `0.25–0.80` | Alpha-edge smoothing radius |

Lower tolerance when the subject is close in color to the background. Raise it slowly only for remaining flat-background residue. Do not compensate for a poor mask by aggressively raising tolerance.

## Processing workflow

### 1. Inspect the source

Determine whether the background is flat, nearly flat, or complex. Note internal white details, existing Alpha, and whether the subject touches an image edge.

### 2. Select segmentation

Use:

1. semantic segmentation or matting for complex photographic backgrounds;
2. edge-connected flood fill for flat or nearly flat backgrounds;
3. manual mask refinement when the subject touches the canvas edge or its edge color is close to the background.

Never remove pixels globally based only on one color.

### 3. Build the alpha matte

- Set confirmed exterior background pixels to Alpha = 0.
- Preserve enclosed white details such as eye whites, teeth, reflections, highlights, and logos.
- Apply only narrow smoothing where an anti-aliased edge needs it.
- Remove white or gray matte contamination from partially transparent edge pixels.

For a known background color `B`, original color `C`, and normalized edge Alpha `a`, a foreground estimate can be calculated as:

```text
F = clamp((C - (1 - a) × B) / max(a, ε))
```

Apply this only to genuine partially transparent edge pixels. Do not alter fully opaque interior detail just to remove white.

### 4. Fit the Teams canvas

- Find the visible subject bounding box.
- Resize proportionally into a 256 × 256 transparent canvas.
- Keep 8–12% transparent padding on every side.
- Use high-quality resampling.
- Do not crop any intentional element.

## Execution environments

### Reference helper

For a flat or nearly flat exterior background:

```bash
python -m pip install -r requirements.txt
python scripts/clean_teams_emoji.py INPUT_IMAGE OUTPUT.webp
```

Example:

```bash
python scripts/clean_teams_emoji.py source.jpg source_teams_emoji_256.webp
```

### Direct implementation

If the helper is unavailable, use Pillow or an equivalent pixel-editing workflow to complete the same segmentation, alpha cleanup, canvas fitting, and verification steps.

### Chat environments

A chat model may be used when it can access the supplied image as an editable source and return a downloadable file.

- Do not run a long capability interview by default.
- Attempt direct source-image processing first.
- If the result is a downloadable file, verify technical metadata when the environment exposes it.
- If metadata cannot be inspected, label the file as **unverified** rather than claiming all checks passed. The user must test the downloaded file in Teams.
- If the image cannot be edited or no downloadable file can be returned, stop with one concise sentence. Do not generate a substitute.

## Output filename

Use:

```text
<sanitized-input-stem>_teams_emoji_256.webp
```

Remove the input extension, replace spaces and underscores with hyphens, remove reserved file-system characters, and preserve Unicode letters and numbers where supported.

Example:

```text
sunglass_ok.jpg
→ sunglass-ok_teams_emoji_256.webp
```

## Mandatory verification

When file inspection is available, reopen the exported file and verify:

- extension is `.webp`
- format is WEBP
- dimensions are 256 × 256
- Alpha channel is present
- every pixel on the outer canvas border has Alpha = 0
- the subject is non-empty and remains inside the padding area

Create review previews on:

- `#FFFFFF`
- `#ECEEF6`
- `#242424`
- `#000000`

Reject and refine the result if any preview shows a white box, white or gray halo, colored fringe, checkerboard pattern, jagged edge, missing internal white detail, or cropped subject.

A preview image is never the final deliverable.

## Delivery response

### Validated file

Use no more than two short lines:

```text
Done: <filename>
256 × 256 transparent WEBP, verified for Teams.
```

### Downloadable but unverified chat file

Use no more than two short lines:

```text
Done: <filename>
Downloadable Teams candidate. Please confirm it after upload.
```

### Blocked

Use one sentence only:

```text
I cannot access this image as an editable source or return a downloadable Teams file in this chat.
```
