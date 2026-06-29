# Teams Emoji Alpha Cleanup Skill

[English](README.md) · [中文](README.zh-CN.md)

## Purpose

This repository has one formal Skill for converting an existing emoji, sticker, avatar, icon, or simple illustration into a Microsoft Teams-ready custom emoji.

It is an asset-cleanup workflow. It preserves the selected source image instead of redrawing or creatively reinterpreting it.

**Target output:** a 256 × 256 transparent WEBP with clean edges, safe padding, and no visible box or halo in Teams.

## Preview

### Before → After

![Before and after](docs/images/before-after-teams.svg)

### Validation backgrounds

![Validation backgrounds](docs/images/validation-backgrounds.svg)

## Start here

### ChatGPT, Claude, or another chat model

For ordinary one-image requests, upload the original image and use the short prompt:

- [Chat quick prompt](prompts/chatgpt-teams-emoji-quick-prompt.en.md)

This is the default path. It instructs the model to process directly, avoid a long explanation, and return a short response with a downloadable file.

Use the detailed [ChatGPT / Claude Guide](docs/CHATGPT_CLAUDE_GUIDE.en.md) only when a result fails, you need to diagnose a limitation, or you want to compare tool support.

### Local Python or a file-capable agent

Use [`SKILL.md`](SKILL.md) for the full technical contract and the bundled helper for repeatable processing.

```bash
git clone https://github.com/JMok999/teams-emoji-alpha-cleanup-skill.git
cd teams-emoji-alpha-cleanup-skill
python -m pip install -r requirements.txt
python scripts/clean_teams_emoji.py input.jpg input_teams_emoji_256.webp
```

## One formal Skill, plus an optional Prompt Pack

- [`SKILL.md`](SKILL.md): source-image cleanup, metadata checks, and Teams export rules.
- [`prompts/teams-emoji-creator-prompts.md`](prompts/teams-emoji-creator-prompts.md): optional prompts for original workplace reaction-emoji concepts.

The Prompt Pack is not a second Skill. It is for creative exploration. A generated concept is not automatically a Teams-ready file; download the chosen image and process it through the cleanup workflow before delivery.

## Choose the right path

| Goal | Use | Acceptance rule |
|---|---|---|
| Make a new reaction-emoji concept | [Prompt Pack](prompts/teams-emoji-creator-prompts.md) | Creative output only; not automatically a Teams asset |
| Preserve an existing emoji and remove its background | [`SKILL.md`](SKILL.md) | Subject remains source-faithful |
| One-off processing in ChatGPT or Claude | [Chat quick prompt](prompts/chatgpt-teams-emoji-quick-prompt.en.md) | Accept only a downloadable file that works in Teams |
| Repeated or technical processing | Python helper or file-capable agent | Run export checks and visual validation |

## Output standard

| Item | Requirement |
|---|---|
| File | WEBP |
| Canvas | 256 × 256 px |
| Transparency | Real Alpha when file metadata can be verified |
| Padding | About 8–12% transparent margin |
| Subject | Complete, centered, and not redesigned |
| Edge | No white box, white halo, gray fringe, or checkerboard residue |
| Review surfaces | `#FFFFFF`, `#ECEEF6`, `#242424`, `#000000` |

## Validation and regression tests

Run the deterministic helper test:

```bash
python -m pip install -r requirements.txt
python tests/test_helper.py
```

See [Self Test](tests/SELF_TEST.md) for the fixture catalogue, expected behavior, and the separate manual compatibility procedure for chat models.

## Limitations

- The reference helper is optimized for flat or nearly flat backgrounds.
- Complex photographs, hair, fur, glass, smoke, or translucent materials need semantic segmentation or manual mask refinement.
- A preview is not a file. If a chat tool cannot return a downloadable asset, it has not completed the task.
- If a chat tool returns a downloadable file but cannot expose metadata, test the file in Teams before calling it verified.

## Project layout

```text
teams-emoji-alpha-cleanup-skill/
├─ README.md
├─ README.zh-CN.md
├─ SKILL.md
├─ requirements.txt
├─ docs/
│  ├─ CHATGPT_CLAUDE_GUIDE.en.md
│  ├─ CHATGPT_CLAUDE_GUIDE.md
│  └─ images/
├─ prompts/
│  ├─ chatgpt-teams-emoji-quick-prompt.en.md
│  ├─ teams-emoji-quick.zh-CN.md
│  └─ teams-emoji-creator-prompts.md
├─ scripts/
│  └─ clean_teams_emoji.py
└─ tests/
   ├─ generate_fixtures.py
   ├─ test_helper.py
   ├─ SELF_TEST.md
   └─ SELF_TEST.zh-CN.md
```

## License

No license file is included yet. Add one before redistributing or accepting outside contributions.
