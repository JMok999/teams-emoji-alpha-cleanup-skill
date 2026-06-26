# Teams Emoji Alpha Cleanup Skill

A reusable Codex/agent skill for preparing Microsoft Teams custom emoji from uploaded images.

## What it prevents

- White squares around an emoji in Teams
- Checkerboard previews embedded as image pixels
- White or gray halo around cutout edges
- Global color deletion that removes intentional white elements
- Cropped emoji faces or icon details
- Non-transparent WEBP exports

## Package contents

- `SKILL.md` — agent instructions and quality standard
- `scripts/clean_teams_emoji.py` — flat-background cleanup helper
- `requirements.txt` — minimal dependency list

## Quick start

```bash
pip install -r requirements.txt
python scripts/clean_teams_emoji.py input.webp output_teams_emoji_256.webp
```

The script is best for emojis/icons on flat white, black, or colored backgrounds. It uses edge-connected background removal instead of deleting one color globally, so internal white details remain intact.

For a photographic or highly textured background, first generate a semantic subject mask with your preferred segmentation tool, then use the skill’s edge-cleanup and validation steps.
