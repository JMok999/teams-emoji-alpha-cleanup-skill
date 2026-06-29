# Self Test

[English](SELF_TEST.md) · [中文](SELF_TEST.zh-CN.md)

This folder provides a deterministic regression test for the Python helper and a manual compatibility checklist for chat tools.

## Run the automated helper test

```bash
python -m pip install -r requirements.txt
python tests/test_helper.py
```

The test generates fixtures in a temporary directory. No fixture binaries are committed.

It verifies that selected flat-background and transparent-source cases produce:

- a decodable WEBP file
- exactly 256 × 256 pixels
- an Alpha channel
- fully transparent outer canvas borders
- a non-empty visible subject
- white, Teams-light, dark-gray, and black preview files
- preserved enclosed white detail in the white-background case
- a static output from the first frame of an animated GIF
- rejection of non-WebP output paths

## Fixture catalogue

`generate_fixtures.py` creates the following deterministic inputs:

| File | Purpose | Expected handling |
|---|---|---|
| `01-white-background-internal-white.png` | White background plus enclosed white detail | Remove only exterior white. Preserve the white inset. |
| `02-existing-alpha.png` | Source already has Alpha | Preserve source transparency and produce a valid Teams canvas. |
| `03-dark-background.png` | Dark flat background | Use edge-connected background removal. |
| `04-near-background-color.png` | Background close to subject tones | Manual review case. Do not solve by aggressively raising tolerance. |
| `05-soft-edge.png` | Anti-aliased illustration edge | Manual review case for smooth edges and no halo. |
| `06-subject-near-edge.png` | Subject approaches canvas boundary | Manual review case. Check for accidental crop or mask loss. |
| `07-animated-first-frame.gif` | Animated source | Process the first frame only and export a static WebP. |

## Manual visual review

For every completed file, composite the final WebP on:

- `#FFFFFF`
- `#ECEEF6`
- `#242424`
- `#000000`

Reject the result if any of the following is visible:

- white box or rectangular residue
- white or gray halo
- colored fringe
- checkerboard baked into the image
- jagged edge
- lost internal white detail
- accidental crop

## Chat-model compatibility test

ChatGPT, Claude, and similar tools are not deterministic test runners. Test them manually with the same fixture images and record:

- date and model / plan
- whether the original image was treated as an editable source
- whether a downloadable file was returned
- reported file type and dimensions
- actual Teams upload result
- whether the output matches the selected source rather than a redesign

For everyday use, start with the short prompt in:

- [`../prompts/chatgpt-teams-emoji-quick-prompt.en.md`](../prompts/chatgpt-teams-emoji-quick-prompt.en.md)
- [`../prompts/teams-emoji-quick.zh-CN.md`](../prompts/teams-emoji-quick.zh-CN.md)
