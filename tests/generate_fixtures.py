#!/usr/bin/env python3
"""Generate deterministic raster fixtures for the Teams emoji helper tests."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


SIZE = 320
SCALE = 4


def _canvas(background: tuple[int, int, int, int]) -> Image.Image:
    return Image.new("RGBA", (SIZE * SCALE, SIZE * SCALE), background)


def _draw_face(image: Image.Image, *, shift_x: int = 0) -> None:
    """Draw a simple face with intentionally enclosed white details."""
    d = ImageDraw.Draw(image)
    s = SCALE
    x = shift_x * s

    d.ellipse((44 * s + x, 38 * s, 276 * s + x, 270 * s), fill=(255, 205, 26, 255))
    d.ellipse((102 * s + x, 112 * s, 127 * s + x, 148 * s), fill=(79, 49, 20, 255))
    d.ellipse((193 * s + x, 112 * s, 218 * s + x, 148 * s), fill=(79, 49, 20, 255))
    d.rounded_rectangle((132 * s + x, 154 * s, 188 * s + x, 238 * s), radius=23 * s, fill=(92, 47, 15, 255))
    # This white inset is not connected to the canvas edge and must survive cleanup.
    d.rounded_rectangle((142 * s + x, 165 * s, 178 * s + x, 182 * s), radius=8 * s, fill=(255, 255, 255, 255))
    d.ellipse((72 * s + x, 72 * s, 112 * s + x, 102 * s), fill=(255, 240, 103, 150))


def _downsample(image: Image.Image) -> Image.Image:
    return image.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def create_fixtures(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    white = _canvas((255, 255, 255, 255))
    _draw_face(white)
    _downsample(white).convert("RGB").save(output_dir / "01-white-background-internal-white.png")

    transparent = _canvas((0, 0, 0, 0))
    _draw_face(transparent)
    _downsample(transparent).save(output_dir / "02-existing-alpha.png")

    dark = _canvas((25, 25, 25, 255))
    _draw_face(dark)
    _downsample(dark).convert("RGB").save(output_dir / "03-dark-background.png")

    near = _canvas((250, 243, 215, 255))
    _draw_face(near)
    _downsample(near).convert("RGB").save(output_dir / "04-near-background-color.png")

    soft = _canvas((255, 255, 255, 255))
    _draw_face(soft)
    _downsample(soft).convert("RGB").save(output_dir / "05-soft-edge.png")

    touch = _canvas((255, 255, 255, 255))
    _draw_face(touch, shift_x=-48)
    _downsample(touch).convert("RGB").save(output_dir / "06-subject-near-edge.png")

    first = _downsample(white).convert("P", palette=Image.Palette.ADAPTIVE)
    second = Image.new("P", first.size, color=0)
    first.save(
        output_dir / "07-animated-first-frame.gif",
        save_all=True,
        append_images=[second],
        duration=100,
        loop=0,
        disposal=2,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate deterministic Teams emoji test fixtures.")
    parser.add_argument("--output", type=Path, default=Path("tests/fixtures"))
    args = parser.parse_args()
    create_fixtures(args.output)
    print(f"Generated fixtures in: {args.output}")


if __name__ == "__main__":
    main()
