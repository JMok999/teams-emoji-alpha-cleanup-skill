#!/usr/bin/env python3
"""
Convert a flat-background emoji/icon into a Teams-ready 256x256 transparent WEBP.

Designed for source images with backgrounds that are connected to canvas edges.
It intentionally does NOT globally remove "white" so internal white details,
such as eyes or highlights, remain intact.

Usage:
    python clean_teams_emoji.py input.webp output.webp
"""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path
from statistics import median
from typing import Iterable, Tuple

from PIL import Image, ImageChops, ImageFilter


RGBA = Tuple[int, int, int, int]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("input", type=Path, help="Input image path")
    p.add_argument("output", type=Path, help="Output .webp path")
    p.add_argument("--size", type=int, default=256, help="Square output size")
    p.add_argument("--padding", type=float, default=0.10, help="Transparent padding fraction (0.08–0.12 recommended)")
    p.add_argument("--tolerance", type=int, default=34, help="Background color tolerance for exterior flood fill")
    p.add_argument("--edge-softness", type=float, default=0.55, help="Alpha edge smoothing radius")
    return p.parse_args()


def sample_border_background(img: Image.Image) -> tuple[int, int, int]:
    """Estimate background color from border pixels using robust medians."""
    w, h = img.size
    samples = []

    # Sample a thin perimeter; ignore fully transparent source pixels.
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
    r, g, b, a = px
    return (r - bg[0]) ** 2 + (g - bg[1]) ** 2 + (b - bg[2]) ** 2


def edge_connected_background_mask(
    img: Image.Image, bg: tuple[int, int, int], tolerance: int
) -> Image.Image:
    """Return L mask where 255 means exterior background connected to an edge."""
    w, h = img.size
    px = img.load()
    mask = Image.new("L", (w, h), 0)
    out = mask.load()
    visited = bytearray(w * h)
    q: deque[tuple[int, int]] = deque()

    threshold_sq = tolerance * tolerance * 3

    def add_seed(x: int, y: int) -> None:
        idx = y * w + x
        if not visited[idx] and px[x, y][3] > 0:
            q.append((x, y))

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
    Remove white/flat background contamination from semi-transparent edge pixels.

    Uses unmixing:
        output = alpha * foreground + (1 - alpha) * background
        foreground = (output - (1-alpha)*background) / alpha

    It only affects pixels with 0 < alpha < 255.
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


def validate(img: Image.Image) -> None:
    if img.mode != "RGBA":
        raise ValueError("Output is not RGBA.")
    if img.width != img.height:
        raise ValueError("Output is not square.")

    corners = [(0, 0), (img.width - 1, 0), (0, img.height - 1), (img.width - 1, img.height - 1)]
    for point in corners:
        if img.getpixel(point)[3] != 0:
            raise ValueError(f"Corner {point} is not fully transparent.")


def save_preview_composites(img: Image.Image, output_path: Path) -> None:
    """Optional verification previews for visual inspection."""
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
    if not 0.02 <= args.padding <= 0.20:
        raise ValueError("--padding must be between 0.02 and 0.20")

    src = Image.open(args.input).convert("RGBA")
    bg = sample_border_background(src)
    exterior_bg = edge_connected_background_mask(src, bg, args.tolerance)

    # Subject alpha = inverse of exterior background.
    alpha = ImageChops.invert(exterior_bg)

    # A very small blur preserves natural anti-aliasing without creating a hard cut.
    if args.edge_softness > 0:
        alpha = alpha.filter(ImageFilter.GaussianBlur(radius=args.edge_softness))

    cleaned = decontaminate_white_matte(src, alpha, bg)
    final = fit_to_canvas(cleaned, args.size, args.padding)
    validate(final)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    final.save(args.output, "WEBP", lossless=True, quality=100, method=6)
    save_preview_composites(final, args.output)

    print(f"Saved: {args.output}")
    print(f"Detected border background: #{bg[0]:02X}{bg[1]:02X}{bg[2]:02X}")
    print(f"Canvas: {final.width}×{final.height}, RGBA, lossless WEBP")


if __name__ == "__main__":
    main()
