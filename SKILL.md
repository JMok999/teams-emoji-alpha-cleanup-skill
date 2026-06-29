---
name: teams-emoji-alpha-cleanup
description: Convert an accessible user-uploaded raster emoji or icon into a Microsoft Teams-ready 256×256 lossless WEBP using source-pixel editing, true RGBA transparency, clean alpha edges, and verified export checks. Never substitute a text-to-image redraw or an opaque preview.
---

# Teams Emoji Alpha Cleanup

Use this skill when a user wants to turn an uploaded emoji, sticker, avatar, icon, or raster illustration into a Microsoft Teams custom emoji.

This is a **technical image-editing and asset-export workflow**. It is not a prompt for recreating an emoji from scratch.

## Read this first: required source and instruction gate

Before any processing, confirm that both of these are actually available:

1. The original image file that must be edited.
2. This `SKILL.md`, or the repository's local helper script and instructions.

A GitHub URL alone is not proof that an assistant has read the repository. If the source image or instructions are unavailable, do not generate a substitute image. Ask the user to upload the source image and `SKILL.md`, or provide a local copy of the repository.

## Task classification and tool selection

Treat the uploaded image as the exact source of truth.

- Perform source-pixel image editing, segmentation, alpha cleanup, resizing, and export.
- Preserve the original subject's proportions, expression, line work, colors, highlights, shadows, and intentional details.
- Do not redraw, restyle, reinterpret, enhance creatively, or create a new emoji that merely resembles the source.
- Do not use text-to-image generation for the final deliverable.
- Do not accept a chat preview, screenshot, checkerboard mockup, or opaque render as proof of transparency.
- If the available environment cannot edit the source pixels and return a downloadable file with verifiable RGBA alpha, do not claim the result is Teams-ready.

## Supported input

Accept a static raster image readable by Pillow, including:

- JPG / JPEG
- PNG
- WEBP
- BMP
- TIFF
- GIF: process the first frame only

Notes:

- The final asset is always a static WEBP.
- Animated GIF or animated WEBP is not preserved as animation.
- SVG, PDF, HEIC, AVIF, and proprietary formats require prior rasterization or an available decoder.
- The helper is best suited to images with a flat or nearly flat exterior background.

## Dependencies

Install the repository dependency before using the reference helper:

```bash
python -m pip install -r requirements.txt
```

The reference workflow requires only:

```bash
python -m pip install "Pillow>=10.0.0"
```

NumPy and SciPy are not required by the reference helper. A direct implementation may use additional packages, but it must not assume they are already installed.

## Core output contract

Produce exactly one final asset that meets all of the following:

- **Format:** lossless WEBP
- **Canvas:** exactly 256 × 256 px
- **Color:** RGBA with a real alpha channel
- **Background:** fully transparent outside the subject
- **Composition:** centered, with 8–12% transparent padding on all four sides
- **Subject:** fully visible and never cropped
- **Edges:** smooth and naturally anti-aliased, without white or gray halos
- **Internal white details:** preserved when they are not connected to the exterior background
- **No baked background:** no white, black, colored, or checkerboard background; no frames, panels, or decorative backdrop
- **Teams compatibility:** validate on light and dark chat-style backgrounds before delivery

## Default parameters

Use these defaults for flat or near-flat background cleanup unless the source needs a more conservative setting:

| Parameter | Default | Recommended range | Purpose |
|---|---:|---:|---|
| Output size | `256` | Fixed | Final square canvas size |
| Padding | `0.10` | `0.08–0.12` | Transparent outer margin |
| Background tolerance | `34` | Adjust gradually | Exterior flood-fill similarity threshold |
| Edge softness | `0.55` | `0.25–0.80` | Alpha-edge smoothing radius |

Adjustment rules:

- Lower `tolerance` when the subject edge is close in color to the background.
- Raise `tolerance` slowly when flat background residue remains. Reinspect after each small change.
- Lower `edge-softness` for crisp icons or pixel art.
- Raise `edge-softness` slightly for soft illustrated edges.
- Never compensate for a poor segmentation mask simply by raising `tolerance`.

## Execution modes

### Mode A: reference helper available

Use the included helper for a flat or nearly flat exterior background:

```bash
python scripts/clean_teams_emoji.py INPUT_IMAGE OUTPUT.webp
```

Example:

```bash
python scripts/clean_teams_emoji.py source.jpg source_teams_emoji_256.webp
```

Optional parameters:

```bash
python scripts/clean_teams_emoji.py INPUT_IMAGE OUTPUT.webp \
  --size 256 \
  --padding 0.10 \
  --tolerance 34 \
  --edge-softness 0.55
```

### Mode B: helper unavailable, direct implementation

Implement the workflow directly with Pillow and follow every step below.

For flat or nearly flat backgrounds:

1. Open the first static frame and convert it to RGBA.
2. Estimate the exterior background color from opaque border pixels.
3. Seed an edge-connected flood fill only from outer canvas pixels.
4. Classify a pixel as exterior background only when it is within the chosen tolerance and connected to the edge.
5. Invert that exterior-background mask to create the subject alpha mask.
6. Preserve enclosed light details, such as eye whites, reflections, teeth, logos, or highlights.
7. Apply narrow edge smoothing only where anti-aliasing is needed.
8. Decontaminate partially transparent edge pixels so they retain nearby subject color rather than white-background color.
9. Fit the complete visible subject proportionally into a centered 256 × 256 transparent canvas.
10. Run the mandatory acceptance checks before export.

For complex photographic backgrounds:

1. Create a semantic segmentation mask or manually refine a mask first.
2. Do not use global color deletion.
3. Continue with alpha cleanup, canvas fitting, validation, and export.

If segmentation confidence is low, do not claim the output is Teams-ready until the mask has been refined.

### Mode C: chat-only or image-generation-only environment

A chat interface may be used only when it can both edit the supplied source image and return a downloadable file with verifiable alpha data.

If the interface can only generate a new image, show a visual preview, or cannot verify/export RGBA WEBP, it is not a valid final-export environment. Do not generate a replacement image and do not claim success. Explain the limitation and use a technical editing path instead.

## Preferred workflow

### 1. Inspect the source

Before processing, determine:

- whether the source has a flat white, black, solid-color, or photographic background
- whether the subject includes intentional white or light-colored details
- whether the source already contains partial alpha
- whether the subject touches the original image boundary
- whether the original file is a real image asset rather than a screenshot of a transparency checkerboard

If the source has a clean flat background, use edge-connected segmentation. This protects white details enclosed inside the subject.

### 2. Select the correct segmentation method

Use one of these methods in order of preference:

1. **Semantic segmentation or matting** for complex photographic backgrounds.
2. **Edge-connected flood-fill segmentation** for flat or nearly flat backgrounds.
3. **Manual mask refinement** when the subject touches the canvas or the background color is close to the subject edge.

Never remove pixels globally based only on one color.

### 3. Create a clean alpha matte

- Set all confirmed exterior-background pixels to alpha = 0.
- Keep the subject interior opaque where appropriate.
- Preserve a narrow soft transition at genuine anti-aliased edges.
- Do not leave a rectangular semi-transparent residue around the subject.
- Remove white or gray matte contamination from semi-transparent edge pixels.

When the original opaque pixel color `C` is known to be composited over a background color `B`, and edge alpha `a` is normalized from 0 to 1, a decontaminated foreground estimate can be calculated as:

```text
F = clamp((C - (1 - a) × B) / max(a, ε))
```

Use this only for genuine edge pixels with partial alpha. Do not alter fully opaque interior pixels merely to remove white.

### 4. Fit the subject to the Teams canvas

- Find the non-transparent subject bounding box.
- Resize proportionally into a 256 × 256 transparent canvas.
- Keep approximately 8–12% padding on each side.
- Use high-quality resampling.
- Never crop the chin, hair, ears, hands, icons, ellipsis dots, or other intentional elements.

## Output filename rule

Derive the final filename from the input filename stem:

```text
<sanitized-input-stem>_teams_emoji_256.webp
```

Sanitization rules:

1. Remove the input extension.
2. Replace spaces, underscores, and repeated separators with one hyphen.
3. Remove file-system-reserved characters: `\ / : * ? " < > |`.
4. Preserve Unicode letters and numbers where the file system supports them.
5. If no usable stem remains, use `teams-emoji`.

Examples:

```text
sunglass_ok.jpg
→ sunglass-ok_teams_emoji_256.webp

滑稽表情.webp
→ 滑稽表情_teams_emoji_256.webp
```

## Mandatory technical verification

Before delivery, decode the exported file and verify all of the following:

- file extension is `.webp`
- format is WEBP and the export is lossless where supported
- dimensions are exactly 256 × 256
- image mode includes alpha / RGBA
- every pixel on the outermost canvas border has alpha = 0
- all four corner pixels have alpha = 0
- the visible subject lies fully inside the required transparent padding area
- the file was derived from the uploaded source image, not a newly generated illustration

Create temporary previews by compositing the result on:

- White: `#FFFFFF`
- Teams-like light chat tone: `#ECEEF6`
- Dark gray: `#242424`
- Black: `#000000`

Reject and refine the cutout if any preview shows:

- a white square or box
- white or gray halo
- light fringe
- colored rectangle
- checkerboard pattern
- jagged or harsh edge
- missing intentional internal white details
- cropped subject
- a visible opaque or semi-transparent background outside the subject

The preview images are validation artifacts only. They are not the final deliverable.

## Failure handling

If the available tool cannot produce or verify a real transparent WEBP:

- do not substitute a generated PNG, JPEG, opaque render, or screenshot;
- do not claim the file is Teams-ready;
- state that the final asset requires source-pixel editing and technical alpha export;
- preserve the original source unchanged until a suitable editing or export path is available.

## Delivery response

When the final file has passed validation, report only the useful outcome:

- state that it is a 256 × 256 transparent WEBP suitable for Teams;
- provide the file link;
- mention that it was verified on white, `#ECEEF6`, dark gray, and black backgrounds;
- do not describe a generated preview as though it were the final file.
