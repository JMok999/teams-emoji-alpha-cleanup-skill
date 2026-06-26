---
name: teams-emoji-alpha-cleanup
description: Convert a user-uploaded emoji or icon into a Microsoft Teams-ready 256×256 lossless WEBP with true RGBA transparency, smooth anti-aliased edges, no baked checkerboard, and no white matte or halo.
---

# Teams Emoji Alpha Cleanup

Use this skill whenever the user wants to turn an uploaded emoji, sticker, avatar, icon, or raster illustration into a Microsoft Teams custom emoji.

## Core output contract

Produce a final asset that meets all of the following:

- **Format:** lossless WEBP
- **Canvas:** 256 × 256 px
- **Color:** RGBA with a real alpha channel
- **Background:** fully transparent (alpha = 0 outside the subject)
- **Composition:** centered, with 8–12% transparent padding on all four sides
- **Subject:** fully visible, never cropped
- **Edges:** smooth and naturally anti-aliased, without white/gray halos
- **No baked background:** no white, black, colored, or checkerboard background; no frames, boxes, or shadow panels
- **Teams compatibility:** validate against light and dark chat-bubble backgrounds before delivery

## Non-negotiable visual rules

1. Treat this as an **image-editing / cutout task**, not a redesign task.
2. Preserve the original subject’s proportions, expression, line work, colors, highlights, shadows, and intended white details.
3. Remove only the original background that is connected to the outer canvas edge.
4. Preserve intentional internal white areas, for example eye whites, reflections, teeth, logos, highlights, and white design details.
5. Do not use a simplistic global white-color deletion. It will damage intended white details and create poor edges.
6. Use smooth alpha matting. Edge pixels must be decontaminated so partially transparent pixels retain the nearby subject color rather than white background contamination.
7. Do not output a PNG screenshot of a checkerboard transparency preview. The final file must carry real alpha transparency.

## Preferred workflow

### 1. Inspect the source

Before processing, determine:

- Whether the source has a flat white/black/color background or a photographic background
- Whether the subject includes intentional white or light-colored details
- Whether the source already contains partial alpha
- Whether the subject touches the image boundary

If the original source has a clean flat background, use **edge-connected background segmentation**. This protects white details enclosed inside the subject.

### 2. Remove the background safely

Use one of these methods in order of preference:

1. **Semantic segmentation / matting** for complex photographic backgrounds.
2. **Edge-connected flood-fill segmentation** for flat or nearly flat backgrounds.
3. **Manual mask refinement** when the subject touches the canvas or the background color is close to the subject color.

Never remove all pixels based solely on one color globally.

### 3. Create a clean alpha matte

- Make exterior background pixels alpha = 0.
- Keep subject interior opaque.
- Preserve a narrow soft edge transition where anti-aliasing is needed.
- Remove white/gray matte contamination from semi-transparent edge pixels.
- Do not leave a rectangular semi-transparent residue around the subject.

### 4. Fit the subject to the Teams canvas

- Find the non-transparent bounding box.
- Resize proportionally into a 256 × 256 transparent canvas.
- Keep approximately 8–12% padding per side.
- Use high-quality resampling.
- Never crop the chin, hair, ears, hands, icons, ellipsis dots, or other intentional elements.

### 5. Verify before export

Create temporary previews by compositing the result on:

- White: `#FFFFFF`
- Light Teams-like chat tone: `#ECEEF6`
- Dark gray: `#242424`
- Black: `#000000`

Reject and refine the cutout if any preview shows:

- a white square or box
- white/gray halo
- light fringe
- colored rectangle
- checkerboard pattern
- jagged / harsh edge
- missing internal white details
- cropped subject

### 6. Export

Export exactly one final file:

```text
<descriptive-name>_teams_emoji_256.webp
```

Use lossless WEBP where available. Confirm:

- 256 × 256 pixels
- RGBA / alpha present
- all corner pixels have alpha = 0
- output is not flattened on white

## Command-line helper

This skill includes a flat-background helper script:

```bash
python scripts/clean_teams_emoji.py INPUT_IMAGE OUTPUT.webp
```

Example:

```bash
python scripts/clean_teams_emoji.py source.webp sly-smile_teams_emoji_256.webp
```

The helper is optimized for emoji or icon source images with a flat background. For complex backgrounds, create a semantic mask first, then run edge cleanup and validation.

## Delivery response

When the file is ready, report only the useful outcome:

- State that it is a 256 × 256 transparent WEBP suitable for Teams.
- Provide the file link.
- Mention that the output was checked against light and dark backgrounds for white halo / background residue.
