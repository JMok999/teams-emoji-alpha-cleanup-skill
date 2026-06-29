# ChatGPT / Claude Guide

This guide is for colleagues who mainly use ChatGPT, Claude, or another chat-based GenAI tool.

Its purpose is not to make a model create an emoji that merely looks similar. Its purpose is to help the model follow source-image editing, transparency, and Teams file requirements. When a chat interface cannot perform real image editing or export a verifiable file, it should stop instead of presenting a convincing-looking new image as success.

## Understand the limitations

Not every chat model, free plan, or web interface can do all of the following:

1. Read a GitHub-linked Skill file.
2. Edit the uploaded source pixels instead of generating a replacement image.
3. Export a downloadable lossless WEBP with a real Alpha channel.
4. Verify that the file is 256 × 256 and free from white halos.

Therefore, pasting only a GitHub link and saying “follow this Skill” is not reliable. If the model has not actually read `SKILL.md`, or can only show a preview image, the task is not complete.

## Recommended workflow

1. Download or save `SKILL.md` from this repository.
2. Prepare the original image file.
3. Upload both files to ChatGPT, Claude, or another chat model:
   - the original image
   - `SKILL.md`
4. Run the preflight prompt below before requesting any edit or generation.
5. Continue only if the model can provide a downloadable file. Without a downloadable WebP, the result is only a visual preview, not a Teams asset.

## Step 1: preflight prompt

```text
Do not generate, edit, redraw, or call any image-generation tool yet.

Read the uploaded SKILL.md completely and inspect the uploaded source image.

Reply with exactly one of the following:

READY:
I can perform source-pixel editing on the uploaded image and return a downloadable 256 × 256 lossless WEBP with verified RGBA alpha.

BLOCKED:
I cannot reliably perform source-pixel editing and verified lossless RGBA WEBP export in this environment. I will not generate a replacement image.
```

`BLOCKED` is the correct answer when the environment can only create a new image or show a preview.

## Step 2: execution prompt

Use this only after the model explicitly returns `READY`:

```text
Proceed with source-pixel editing only.

Use the uploaded image as the exact source. Do not redraw, reinterpret, enhance creatively, or generate a new emoji.

Follow SKILL.md exactly. If any requirement cannot be verified, stop and return no image.

Deliver only a downloadable 256 × 256 lossless WEBP with verified RGBA alpha.
```

## Good signals

- The model confirms it read the uploaded `SKILL.md`.
- It describes the task as editing the original image or removing its background.
- It explains that it will return a file, not only a chat preview.
- It can explain how Alpha, canvas size, and WEBP will be verified.

## Stop signals

- The model says it cannot read the GitHub link but then generates an image anyway.
- It creates a new 3D, illustrated, or stylistically different emoji.
- The result has a gradient, solid-color, white, or checkerboard background.
- It only displays an image preview and cannot provide a file.
- It treats “looks transparent” as proof of RGBA Alpha.
- It claims completion without confirming WEBP, dimensions, and Alpha.

## Final validation checklist

Check the downloaded file:

- `.webp` extension
- 256 × 256 px
- clean on white, Teams light gray, dark gray, and black backgrounds
- no white box, white halo, or gray fringe after upload to Teams
- subject matches the selected source image rather than a redesigned version

## Reliability guide

| Usage method | Best for | Reliability |
|---|---|---|
| GitHub link only | Explaining the rough project purpose | Low |
| Upload original image + `SKILL.md` | Testing whether a chat model can honor the editing constraints | Medium |
| Python helper or Codex / Agent | Producing and verifying a real Teams asset | High |

Chat models are useful for exploration and early testing. For dependable Teams delivery, use the Python helper or an agent that can manipulate files and verify the exported asset.
