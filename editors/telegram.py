#!/usr/bin/env python3
"""Build editors/telegram/edgerunners.tdesktop-theme for Telegram Desktop.

    python3 editors/telegram.py

Starts from Telegram's own night theme (fetched from the tdesktop repo, so
every key Telegram expects is present) and recolours it by role rather than
by hand-picking hundreds of keys:

  - near-neutral blue-greys (surfaces, text) move onto Edgerunners' indigo
    and lavender, keeping Telegram's lightness so its contrast stays intact;
  - Telegram's blue accent becomes the Lucy cyan, as in the shell and editors;
  - other hues (online green, error red, name colours) snap to the nearest
    Edgerunners hue: neon red, HOTEL orange, rocket gold, acid green,
    Lucy cyan, Lucy blue, neon violet.

The chat background is the rocket launch wallpaper, dimmed so bubbles stay
readable. Apply the result by opening the file with Telegram and choosing
"Keep changes".
"""
import io
import math
import pathlib
import re
import subprocess
import tomllib
import urllib.request
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
THEME = HERE.parent
NIGHT_URL = "https://raw.githubusercontent.com/telegramdesktop/tdesktop/dev/Telegram/Resources/night.tdesktop-theme"
P = tomllib.loads((THEME / "colors.toml").read_text())


def lin(v):
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def delin(v):
    return 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055


def to_oklch(rgb):
    r, g, b = (lin(c / 255) for c in rgb)
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    A = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    B = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    return L, math.hypot(A, B), math.degrees(math.atan2(B, A)) % 360


def from_oklch(L, C, H):
    while True:
        a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
        l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
        m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
        s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
        rgb = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
               -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
               -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)
        if all(-1e-4 <= v <= 1 + 1e-4 for v in rgb) or C <= 0:
            return tuple(round(max(0, min(1, delin(max(0, v)))) * 255) for v in rgb)
        C -= 0.002


def hue_of(hex_):
    h = hex_.lstrip("#")
    return to_oklch(tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)))[2]


NEUTRAL_HUE = to_oklch(tuple(int(P["background"][i:i + 2], 16) for i in (1, 3, 5)))[2]
def oklch_of(hex_):
    h = hex_.lstrip("#")
    return to_oklch(tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)))


# Each Edgerunners hue with the most chroma the palette gives it (normal or bright),
# so recoloured Telegram colours never get louder than the theme itself.
HUES = {}
for name in ("red", "orange", "yellow", "green", "cyan", "blue", "magenta"):
    _, c1, h = oklch_of(P[name])
    c2 = oklch_of(P.get("bright_" + name, P[name]))[1]
    HUES[name] = (h, max(c1, c2))
ACCENT_HUE = HUES["cyan"][0]


def recolor(key, value):
    m = re.fullmatch(r"#([0-9a-fA-F]{6})([0-9a-fA-F]{2})?", value)
    if not m:
        return value
    rgb = tuple(int(m.group(1)[i:i + 2], 16) for i in (0, 2, 4))
    alpha = m.group(2) or ""
    L, C, H = to_oklch(rgb)
    if C < 0.045:
        # Surfaces and text: Edgerunners indigo (dark) and lavender (light) at Telegram's
        # lightness.
        tint = min(max(C, 0.02), 0.034) if L < 0.6 else 0.03 if L < 0.85 else 0.012
        out = from_oklch(L, tint, NEUTRAL_HUE)
    elif 215 <= H <= 275 and "Peer" not in key and "peer" not in key:
        # Telegram's blue identity colour becomes the Lucy cyan.
        # Softer when dark (bubbles, buttons), like the theme's own selection.
        out = from_oklch(L, min(C, 0.085 if L >= 0.5 else 0.055), ACCENT_HUE)
    else:
        th, tc = min(HUES.values(), key=lambda t: min(abs(t[0] - H), 360 - abs(t[0] - H)))
        out = from_oklch(L, min(C, tc), th)
    return "#" + "".join(f"{v:02x}" for v in out) + alpha


def main():
    data = urllib.request.urlopen(NIGHT_URL, timeout=30).read()
    src = zipfile.ZipFile(io.BytesIO(data)).read("colors.tdesktop-theme").decode()
    lines = ["// Edgerunners for Telegram Desktop: Telegram's night theme recoloured",
             "// by role (editors/telegram.py). Night City neon after rain."]
    for line in src.splitlines():
        m = re.match(r"^(\s*)([A-Za-z0-9_]+)(\s*:\s*)([^;]+)(;.*)$", line)
        if m:
            key, value = m.group(2), m.group(4).strip()
            line = f"{m.group(1)}{key}{m.group(3)}{recolor(key, value)}{m.group(5)}"
        lines.append(line)
    colors = "\n".join(lines) + "\n"

    bg = subprocess.run(
        ["magick", str(THEME / "backgrounds" / "01-edgerunners-rocket.jpg"),
         "-resize", "2560x1440^", "-gravity", "center", "-extent", "2560x1440",
         "-modulate", "55,85", "-quality", "88", "jpg:-"],
        check=True, capture_output=True).stdout

    out = HERE / "telegram"
    out.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out / "edgerunners.tdesktop-theme", "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("colors.tdesktop-theme", colors)
        z.writestr("background.jpg", bg)
    print("wrote", out / "edgerunners.tdesktop-theme")


if __name__ == "__main__":
    main()
