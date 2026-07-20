#!/usr/bin/env python3
"""Render the verified cold-resume session as a compact terminal GIF.

This documentation-only helper requires Pillow. Yakherd itself remains
standard-library-only and has no runtime dependencies.
"""

from __future__ import annotations

import argparse
import json
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1280
HEIGHT = 720
FPS = 6
BACKGROUND = "#07111d"
TERMINAL = "#0b1726"
FOREGROUND = "#dbe7f3"
MUTED = "#73859a"
ACCENT = "#f4b942"
PASS = "#52d273"
BLUE = "#6cb6ff"


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf"),
        Path("/System/Library/Fonts/Menlo.ttc"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def wrap(lines: list[str], width: int = 88) -> list[str]:
    wrapped: list[str] = []
    for line in lines:
        prefix = "$ " if line.startswith("$ ") else ""
        content = line[len(prefix) :]
        parts = textwrap.wrap(
            content,
            width=width - len(prefix),
            replace_whitespace=False,
            drop_whitespace=False,
        ) or [""]
        wrapped.append(prefix + parts[0])
        wrapped.extend("  " + part for part in parts[1:])
    return wrapped


def render_frame(scene: dict[str, object], progress: float) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    regular = font(24)
    small = font(19)
    heading = font(28, bold=True)
    verdict = font(40, bold=True)

    draw.rounded_rectangle((46, 42, WIDTH - 46, HEIGHT - 42), radius=22, fill=TERMINAL)
    draw.ellipse((70, 66, 88, 84), fill="#ff5f57")
    draw.ellipse((98, 66, 116, 84), fill="#febc2e")
    draw.ellipse((126, 66, 144, 84), fill="#28c840")
    draw.text((168, 62), "yakherd · cold-resume proof", font=small, fill=MUTED)
    draw.text((78, 112), str(scene["title"]), font=heading, fill=ACCENT)

    lines = wrap([str(line) for line in scene.get("lines", [])])
    visible = max(1, min(len(lines), round(len(lines) * progress)))
    y = 172
    for line in lines[:visible]:
        color = FOREGROUND
        if line.startswith("$"):
            color = BLUE
        elif "passed" in line.lower() or "pass" == line.strip().lower():
            color = PASS
        elif line.startswith("#"):
            color = MUTED
        draw.text((78, y), line, font=regular, fill=color)
        y += 38

    status = str(scene.get("status", ""))
    if status:
        color = PASS if status.upper() == "PASS" else BLUE
        draw.text((WIDTH - 250, HEIGHT - 112), status, font=verdict, fill=color)

    draw.text(
        (78, HEIGHT - 88),
        "fresh agent · no implementation chat · evidence committed beside this recording",
        font=small,
        fill=MUTED,
    )
    return image


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    session = json.loads(args.session.read_text(encoding="utf-8"))
    frames: list[Image.Image] = []
    durations: list[int] = []
    for scene in session["scenes"]:
        frame_count = max(1, round(float(scene.get("seconds", 1.5)) * FPS))
        for index in range(frame_count):
            progress = min(1.0, (index + 1) / max(1, frame_count // 2))
            frames.append(render_frame(scene, progress))
            durations.append(round(1000 / FPS))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        args.output,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(f"rendered {args.output} frames={len(frames)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
