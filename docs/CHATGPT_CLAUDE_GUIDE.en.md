# ChatGPT / Claude Guide

This guide is for colleagues who mainly use ChatGPT, Claude, or another chat-based GenAI tool.

## Use the short path first

For normal use, upload the original image and copy the short prompt from:

[`../prompts/chatgpt-teams-emoji-quick-prompt.en.md`](../prompts/chatgpt-teams-emoji-quick-prompt.en.md)

Do not ask the model to summarize `SKILL.md`, explain its algorithm, or complete a preflight report before editing. Those steps increase response length without improving a simple one-image task.

## What to upload

1. The original image file.
2. The short prompt above.

A JPG or PNG saved from a webpage is still a valid input file. Whether a chat platform passes that file to its editing tool depends on the current session's attachment binding state, not on whether the image came from a screenshot.

Upload `SKILL.md` only when you need a detailed technical workflow, are using an agent or local tool, or need to diagnose a failed result.

## Accept or reject the result

Accept it only when:

- a downloadable file is returned;
- WEBP is preferred;
- when the chat tool can only return PNG, the downloadable file may be accepted as a real transparent `.png` if the model reports PNG honestly;
- JPG or JPEG is not accepted as a transparent final asset;
- the image remains faithful to the selected source;
- it uploads to Teams without a visible box, halo, or fringe.

A chat preview or checkerboard display is not a deliverable.

## When a chat tool cannot finish

The assistant should reply with one concise sentence and stop. It should not generate a new lookalike emoji, provide a long explanation, or claim the result is verified.

Example:

```text
I cannot access this image as an editable source or return a downloadable Teams file in this chat.
```

Re-uploading the source, starting a new chat, or changing browsers can sometimes rebind the attachment. They are not guaranteed fixes. If one chat continues to report that no editable image target exists, do not keep asking the user to resave the image or upload a screenshot.

## Optional diagnostic prompt

Use this only after a failed attempt, not as the default first step:

```text
Read the uploaded SKILL.md and diagnose why this image cannot be returned as a downloadable Teams WebP or transparent PNG.
Keep the response under five bullets. Do not generate a replacement image.
```

## Reliability guide

| Method | Best use | Reliability |
|---|---|---|
| Original image + short prompt | One-off chat-based processing | Depends on the returned file and actual Teams upload |
| Original image + `SKILL.md` | Diagnosis or detailed technical execution | Better instruction coverage, more context cost |
| Python helper | Repeatable flat-background processing with strict WebP output | High |
| File-capable agent | Automated processing and metadata checks | High when validation is performed |

## Technical verification

When a tool exposes file metadata, verify:

- the real file format is WEBP or PNG. Do not accept a mismatched filename and file type;
- 256 × 256 pixels;
- Alpha channel present;
- transparent outer canvas border.

When it does not expose metadata but returns a downloadable file, treat the result as a Teams candidate. Confirm it by uploading it to Teams and checking white, Teams-light, dark-gray, and black surfaces.

For deterministic regression tests, see [`../tests/SELF_TEST.md`](../tests/SELF_TEST.md).
