#!/usr/bin/env python3
"""
Convert a flat-background emoji or icon into a Teams-ready 256x256 transparent WEBP.

Designed for static raster source images with backgrounds connected to canvas edges.
Accepted input includes formats readable by Pillow, such as JPG, PNG, WEBP,
BMP, TIFF, and the first frame of GIF files.

The helper intentionally does NOT globally remove "white" so internal white
features, such as eyes or highlights, remain intact. It is not intended for
complex photographic backgrounds, hair, fur, smoke, glass, or translucent
materials without a refined mask.

Usage:
    python clean_teams_emoji.py input.jpg output_teams_emoji_256.webp
"""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path
from statistics import median
from typing import Tuple

from PIL import Image, ImageChops, ImageFilter


RGBA = Tuple[int, int, int, int]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Create a verified 256x256 transparent Teams emoji WEBP from a flat-background raster image."
    )
    p.add_argument(
        "input",
        type=Path,
        help="Input static raster image readable by Pillow, for example JPG, PNG, WEBP, BMP, TIFF, or GIF.",
    )
    p.add_argument("output", type=Path, help="Output lossless .webp path")
    p.add_argument("--size", type=int, default=256, help="Teams output size. Must remain 256.")
    p.add_argument("--padding", type=float, default=0.10, help="Transparent padding fraction (0.08-0.12 recommended)")
    p.add_argument("--tolerance", type=int, default=34, help="Background color tolerance for exterior flood fill")
    p.add_argument("--edge-softness", type=float, default=0.55, help="Alpha edge smoothing radius")
    return p.parse_args()


def sample_border_background(img: Image.Image) -> tuple[int, int, int]:
    """Estimate background color from opaque border pixels using robust medians."""
    w, h = img.size
    samples = []

    # Sample a thin perimeter and ignore fully transparent source pixels.
    for x in range(w):
        for y in (0, min(h - 1, 1), max(0, h - 2), h - 1):
            r, g, b, a = img.getpixel((x, y))
            if a > 0:
                samples.append((r, g, b))
    for y in range(h):
        for x in (0, min(w - 1, 1), max(0, w - 2), w - 1):
            r, g, b, a = img.getpixel((x, y))
            if a > 0:
                samples.append((r, g, b))

    if not samples:
        return (255, 255, 255)

    return tuple(int(median([v[i] for v in samples])) for i in range(3))


def color_distance_sq(px: RGBA, bg: tuple[int, int, int]) -> int:
    r, g, b, _ = px
    return (r - bg[0]) ** 2 + (g - bg[1]) ** 2 + (b - bg[2]) ** 2


def edge_connected_background_mask(
    img: Image.Image, bg: tuple[int, int, int], tolerance: int
) -> Image.Image:
    """Return an L mask where 255 means exterior background connected to an edge."""
    w, h = img.size
    px = img.load()
    mask = Image.new("L", (w, h), 0)
    out = mask.load()
    visited = bytearray(w * h)
    q: deque[tuple[int, int]] = deque()

    threshold_sq = tolerance * tolerance * 3

    def add_seed(x: int, y: int) -> None:
        idx = y * w + x
        if not visited[idx]:
            q.append((x, y))

    # Seed every boundary pixel. Existing transparent pixels are exterior
    # background and must remain transparent after the output alpha is built.
    for x in range(w):
        add_seed(x, 0)
        add_seed(x, h - 1)
    for y in range(h):
        add_seed(0, y)
        add_seed(w - 1, y)

    while q:
        x, y = q.popleft()
        idx = y * w + x
        if visited[idx]:
            continue
        visited[idx] = 1

        cur = px[x, y]
        if cur[3] == 0:
            out[x, y] = 255
        elif color_distance_sq(cur, bg) <= threshold_sq:
            out[x, y] = 255
        else:
            continue

        if x > 0:
            q.append((x - 1, y))
        if x + 1 < w:
            q.append((x + 1, y))
        if y > 0:
            q.append((x, y - 1))
        if y + 1 < h:
            q.append((x, y + 1))

    return mask


def decontaminate_white_matte(img: Image.Image, alpha: Image.Image, bg: tuple[int, int, int]) -> Image.Image:
    """
    Remove flat background contamination from semi-transparent edge pixels.

    Uses unmixing:
        output = alpha * foreground + (1 - alpha) * background
        foreground = (output - (1 - alpha) * background) / alpha

    It affects only pixels with 0 < alpha < 255.
    """
    rgba = img.convert("RGBA")
    pix = rgba.load()
    apx = alpha.load()
    w, h = rgba.size

    for y in range(h):
        for x in range(w):
            a = apx[x, y]
            if a <= 0:
                pix[x, y] = (0, 0, 0, 0)
                continue
            r, g, b, _ = pix[x, y]
            if a < 255:
                af = a / 255.0
                # Skip unstable values that are almost fully transparent.
                if af > 0.08:
                    nr = int(round((r - (1.0 - af) * bg[0]) / af))
                    ng = int(round((g - (1.0 - af) * bg[1]) / af))
                    nb = int(round((b - (1.0 - af) * bg[2]) / af))
                    r = max(0, min(255, nr))
                    g = max(0, min(255, ng))
                    b = max(0, min(255, nb))
            pix[x, y] = (r, g, b, a)

    return rgba


def fit_to_canvas(img: Image.Image, size: int, padding: float) -> Image.Image:
    alpha = img.getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        raise ValueError("No visible subject remained after background removal.")

    crop = img.crop(bbox)
    inner = max(1, int(round(size * (1 - 2 * padding))))
    cw, ch = crop.size
    scale = min(inner / cw, inner / ch)
    resized = crop.resize((max(1, round(cw * scale)), max(1, round(ch * scale))), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    x = (size - resized.width) // 2
    y = (size - resized.height) // 2
    canvas.alpha_composite(resized, (x, y))
    return canvas


def validate(img: Image.Image, expected_size: int) -> None:
    """Verify the in-memory asset meets the required Teams geometry and alpha checks."""
    if img.mode != "RGBA":
        raise ValueError("Output is not RGBA.")
    if img.width != expected_size or img.height != expected_size:
        raise ValueError(f"Output must be exactly {expected_size}x{expected_size}.")

    # Because the final subject is fitted with transparent padding, every edge
    # pixel must be fully transparent. This catches full-frame backgrounds and
    # rectangular alpha residue more reliably than checking corners alone.
    for x in range(img.width):
        if img.getpixel((x, 0))[3] != 0 or img.getpixel((x, img.height - 1))[3] != 0:
            raise ValueError("Top or bottom canvas border is not fully transparent.")
    for y in range(img.height):
        if img.getpixel((0, y))[3] != 0 or img.getpixel((img.width - 1, y))[3] != 0:
            raise ValueError("Left or right canvas border is not fully transparent.")


def save_preview_composites(img: Image.Image, output_path: Path) -> None:
    """Save visual inspection previews on the required validation backgrounds."""
    preview_dir = output_path.parent / f"{output_path.stem}_previews"
    preview_dir.mkdir(exist_ok=True)
    colors = {
        "white": (255, 255, 255, 255),
        "teams_light": (236, 238, 246, 255),
        "dark": (36, 36, 36, 255),
        "black": (0, 0, 0, 255),
    }
    for label, color in colors.items():
        bg = Image.new("RGBA", img.size, color)
        bg.alpha_composite(img)
        bg.convert("RGB").save(preview_dir / f"{label}.png")


def main() -> None:
    args = parse_args()

    if args.output.suffix.lower() != ".webp":
        raise ValueError("Output path must end with .webp")
    if args.size != 256:
        raise ValueError("Teams custom emoji output must use --size 256.")
    if not 0.02 <= args.padding <= 0.20:
        raise ValueError("--padding must be between 0.02 and 0.20")
    if args.tolerance < 0:
        raise ValueError("--tolerance must be non-negative")
    if args.edge_softness < 0:
        raise ValueError("--edge-softness must be non-negative")

    with Image.open(args.input) as loaded:
        # Pillow opens the first frame by default. Explicitly select it so GIF
        # input is handled predictably as a static source image.
        if getattr(loaded, "is_animated", False):
            loaded.seek(0)
        src = loaded.convert("RGBA")

    bg = sample_border_background(src)
    exterior_bg = edge_connected_background_mask(src, bg, args.tolerance)

    # Subject alpha equals the inverse exterior background, while preserving
    # alpha that already existed in the source image.
    alpha = ImageChops.multiply(ImageChops.invert(exterior_bg), src.getchannel("A"))

    # A very small blur preserves natural anti-aliasing without creating a hard cut.
    if args.edge_softness > 0:
        alpha = alpha.filter(ImageFilter.GaussianBlur(radius=args.edge_softness))

    cleaned = decontaminate_white_matte(src, alpha, bg)
    final = fit_to_canvas(cleaned, args.size, args.padding)
    validate(final, args.size)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    final.save(args.output, "WEBP", lossless=True, quality=100, method=6)

    # Verify the actual encoded file, not only the in-memory image.
    with Image.open(args.output) as encoded:
        if "A" not in encoded.getbands():
            raise ValueError("Saved WEBP is missing an alpha channel.")
        decoded = encoded.convert("RGBA")
    validate(decoded, args.size)

    save_preview_composites(decoded, args.output)

    print(f"Saved: {args.output}")
    print(f"Detected border background: #{bg[0]:02X}{bg[1]:02X}{bg[2]:02X}")
    print(f"Canvas: {decoded.width}x{decoded.height}, RGBA, lossless WEBP")


if __name__ == "__main__":
    main()
