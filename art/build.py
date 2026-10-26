#!/usr/bin/env python3
"""Draw the Edgerunners logo art: Lucy's moon over Night City, the rocket
climbing toward it.

    python3 art/build.py

Writes unlock.png (login and boot logo, an SVG rendered by rsvg-convert),
preview-unlock.png, and fastfetch-logo.txt: the same scene as pixel art in
24-bit half-blocks, which fastfetch's `file` logo type passes through."""
import math
import pathlib
import random
import subprocess
import tempfile

OUT = pathlib.Path(__file__).resolve().parent.parent

CYAN, CYAN_HI, BLUE, VIOLET = "#03D1EA", "#B8F6FF", "#5A96F9", "#BC48DD"
PINK, YELLOW, YELLOW_HI = "#FE5F7E", "#F1E607", "#FFFBD0"
TOWER, TOWER_EDGE = "#121335", "#24265E"


def crescent(cx, cy, r, ox, oy, r2):
    """Path of a disc (cx, cy, r) minus a disc (cx+ox, cy+oy, r2)."""
    d = math.hypot(ox, oy)
    a = (r * r - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(r * r - a * a)
    ux, uy = ox / d, oy / d
    px, py = cx + a * ux, cy + a * uy
    p1 = (px + h * uy, py - h * ux)
    p2 = (px - h * uy, py + h * ux)
    return (f"M {p1[0]:.1f} {p1[1]:.1f} "
            f"A {r} {r} 0 1 0 {p2[0]:.1f} {p2[1]:.1f} "
            f"A {r2} {r2} 0 0 1 {p1[0]:.1f} {p1[1]:.1f} Z")


# Hand-placed towers: (left, width, height, top) as fractions of the canvas;
# top is "flat", "antenna", "step" or "spire".
FAR = [(0.10, 0.05, 0.30, "antenna"), (0.20, 0.04, 0.36, "flat"), (0.33, 0.06, 0.26, "step"),
       (0.47, 0.04, 0.40, "spire"), (0.66, 0.05, 0.32, "flat"), (0.80, 0.04, 0.37, "antenna")]
NEAR = [(0.04, 0.08, 0.17, "flat"), (0.13, 0.06, 0.25, "step"), (0.20, 0.05, 0.14, "flat"),
        (0.26, 0.07, 0.31, "antenna"), (0.34, 0.05, 0.19, "flat"), (0.40, 0.09, 0.22, "step"),
        (0.50, 0.05, 0.28, "flat"), (0.56, 0.07, 0.16, "flat"), (0.64, 0.06, 0.24, "antenna"),
        (0.71, 0.08, 0.18, "step"), (0.80, 0.05, 0.27, "flat"), (0.86, 0.09, 0.15, "flat")]
NEAR_EDGES = {3: PINK, 6: CYAN, 10: PINK}   # neon roof lines
SIGN = 8                                   # tower with a vertical neon sign


def tower(x, w, h, top, base, fill, s):
    out = [f'<rect x="{x:.1f}" y="{base - h:.1f}" width="{w:.1f}" height="{h + 2:.1f}" fill="{fill}"/>']
    if top == "antenna":
        out.append(f'<rect x="{x + w * 0.45:.1f}" y="{base - h - h * 0.22:.1f}" width="{2 * s:.1f}" height="{h * 0.22:.1f}" fill="{fill}"/>')
    elif top == "step":
        out.append(f'<rect x="{x + w * 0.2:.1f}" y="{base - h - h * 0.10:.1f}" width="{w * 0.6:.1f}" height="{h * 0.10 + 1:.1f}" fill="{fill}"/>')
    elif top == "spire":
        out.append(f'<path d="M {x:.1f} {base - h:.1f} L {x + w / 2:.1f} {base - h * 1.35:.1f} L {x + w:.1f} {base - h:.1f} Z" fill="{fill}"/>')
    return out


def skyline(W, H, base, s):
    rnd = random.Random(11)
    far, near, glow = [], [], []
    for fx, fw, fh, top in FAR:
        far += tower(fx * W, fw * W, fh * H, top, base, TOWER_EDGE, s)
    for i, (fx, fw, fh, top) in enumerate(NEAR):
        x, w, h = fx * W, fw * W, fh * H
        near += tower(x, w, h, top, base, TOWER, s)
        if i in NEAR_EDGES:
            glow.append(f'<rect x="{x:.1f}" y="{base - h:.1f}" width="{w:.1f}" height="{2.2 * s:.1f}" fill="{NEAR_EDGES[i]}"/>')
        if i == SIGN:
            glow.append(f'<rect x="{x + w * 0.62:.1f}" y="{base - h * 0.88:.1f}" width="{w * 0.16:.1f}" height="{h * 0.55:.1f}" rx="{s:.1f}" fill="{PINK}"/>')
        for j in range(int(w / (8 * s))):
            for k in range(1, int(h / (10 * s))):
                if rnd.random() < 0.16:
                    c = rnd.choice([CYAN, CYAN, YELLOW, PINK])
                    near.append(f'<rect x="{x + (3 + j * 8) * s:.1f}" y="{base - h + k * 10 * s:.1f}" '
                                f'width="{2.6 * s:.1f}" height="{3.4 * s:.1f}" fill="{c}" opacity="0.9"/>')
    return far, near, glow


def scene(W, H, s):
    """s scales strokes and features with the canvas."""
    cx, cy, r = W * 0.58, H * 0.40, H * 0.30
    moon = crescent(cx, cy, r, r * 0.38, -r * 0.26, r * 0.90)
    base = H * 0.97
    far, near, glowing = skyline(W, H, base, s)
    # Rocket: trail curving up from the lower left toward the moon's hollow.
    rx, ry = cx - r * 0.05, cy + r * 0.05
    trail = f"M {W * 0.18:.1f} {base - H * 0.16:.1f} Q {W * 0.30:.1f} {H * 0.45:.1f} {rx:.1f} {ry:.1f}"
    g = []
    g.append(f'''<defs>
  <linearGradient id="moonfill" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{CYAN}"/><stop offset="0.5" stop-color="{BLUE}"/><stop offset="1" stop-color="{VIOLET}"/>
  </linearGradient>
  <linearGradient id="trail" gradientUnits="userSpaceOnUse" x1="{W * 0.18:.1f}" y1="{base:.1f}" x2="{rx:.1f}" y2="{ry:.1f}">
    <stop offset="0" stop-color="{YELLOW}" stop-opacity="0"/><stop offset="1" stop-color="{YELLOW}"/>
  </linearGradient>
  <linearGradient id="horizon" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{PINK}" stop-opacity="0"/><stop offset="1" stop-color="{PINK}" stop-opacity="0.55"/>
  </linearGradient>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="{10 * s:.1f}" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{12 * s:.1f}"/></filter>
  <filter id="softglow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="{4 * s:.1f}" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="slice1"><rect x="0" y="{cy - r * 0.10:.1f}" width="{W}" height="{r * 0.07:.1f}"/></clipPath>
  <clipPath id="slice2"><rect x="0" y="{cy + r * 0.38:.1f}" width="{W}" height="{r * 0.05:.1f}"/></clipPath>
  <mask id="unsliced"><rect width="{W}" height="{H}" fill="white"/>
    <rect x="0" y="{cy - r * 0.10:.1f}" width="{W}" height="{r * 0.07:.1f}" fill="black"/>
    <rect x="0" y="{cy + r * 0.38:.1f}" width="{W}" height="{r * 0.05:.1f}" fill="black"/></mask>
  <linearGradient id="fadex" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="white" stop-opacity="0"/><stop offset="0.14" stop-color="white"/>
    <stop offset="0.86" stop-color="white"/><stop offset="1" stop-color="white" stop-opacity="0"/></linearGradient>
  <mask id="sides"><rect width="{W}" height="{H}" fill="url(#fadex)"/></mask>
  <clipPath id="above"><rect x="0" y="0" width="{W}" height="{base:.1f}"/></clipPath>
</defs>''')
    # Horizon glow behind the city.
    g.append(f'<rect x="0" y="{base - H * 0.30:.1f}" width="{W}" height="{H * 0.30:.1f}" fill="url(#horizon)" mask="url(#sides)"/>')
    # Moon with a bright rim; its glow sits on its own layer so the glitch
    # cut-outs don't cut the glow too.
    g.append(f'<path d="{moon}" fill="url(#moonfill)" opacity="0.8" filter="url(#blur)"/>')
    g.append(f'<g mask="url(#unsliced)"><path d="{moon}" fill="url(#moonfill)"/>'
             f'<path d="{moon}" fill="none" stroke="{CYAN_HI}" stroke-opacity="0.75" stroke-width="{2.2 * s:.1f}"/></g>')
    # Glitch: two thin slices of the moon pushed sideways, split into cyan and magenta.
    for clip, dx in (("slice1", 16 * s), ("slice2", -11 * s)):
        g.append(f'<g clip-path="url(#{clip})">'
                 f'<path d="{moon}" fill="{VIOLET}" opacity="0.9" transform="translate({dx + 4 * s:.1f},0)"/>'
                 f'<path d="{moon}" fill="{CYAN}" opacity="0.9" transform="translate({dx - 4 * s:.1f},0)"/>'
                 f'<path d="{moon}" fill="url(#moonfill)" transform="translate({dx:.1f},0)"/></g>')
    # Rocket trail and flare.
    g.append(f'<path d="{trail}" fill="none" stroke="url(#trail)" stroke-width="{4 * s:.1f}" stroke-linecap="round" '
             f'filter="url(#softglow)"/>')
    g.append(f'<g filter="url(#softglow)">'
             f'<rect x="{rx - W * 0.16:.1f}" y="{ry - 1.2 * s:.1f}" width="{W * 0.32:.1f}" height="{2.4 * s:.1f}" fill="{YELLOW}" opacity="0.85"/>'
             f'<rect x="{rx - 1.2 * s:.1f}" y="{ry - H * 0.06:.1f}" width="{2.4 * s:.1f}" height="{H * 0.12:.1f}" fill="{YELLOW}" opacity="0.7"/></g>')
    g.append(f'<circle cx="{rx:.1f}" cy="{ry:.1f}" r="{6 * s:.1f}" fill="{YELLOW_HI}" filter="url(#glow)"/>')
    # City.
    city = (f'<g opacity="0.75">' + "".join(far) + "</g>" + "".join(near)
            + '<g filter="url(#softglow)">' + "".join(glowing) + "</g>")
    g.append(f'<g clip-path="url(#above)" mask="url(#sides)">{city}</g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            + "\n".join(g) + "</svg>")


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def mix(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def pixel_logo(W=48, H=52):
    """The same scene drawn pixel by pixel for fastfetch: crisp at 1 pixel per half-cell."""
    px = [[None] * W for _ in range(H)]          # (r, g, b, alpha 0..1)

    def put(x, y, c, a=1.0):
        if 0 <= x < W and 0 <= y < H:
            under = px[y][x]
            if under and a < 1:
                c = mix(under[:3], c, a)
                a = max(a, under[3])
            px[y][x] = (*c, a)

    # Horizon glow, behind everything else.
    for y in range(30, H):
        for x in range(W):
            edge = min(x, W - 1 - x) / 8
            put(x, y, hexrgb(PINK), 0.55 * ((y - 30) / (H - 30)) ** 1.6 * min(1, edge))
    # Stars.
    for x, y in ((4, 4), (11, 9), (6, 20), (44, 6), (40, 14), (16, 2)):
        put(x, y, hexrgb("#C3C4E1"), 0.8)
    # Moon: a disc minus a disc, gradient cyan -> blue -> violet, bright outer rim.
    cx, cy, r, ox, oy, r2 = 23.5, 17.5, 13.0, 6.5, -4.5, 11.6
    stops = [hexrgb(CYAN), hexrgb(BLUE), hexrgb(VIOLET)]
    for y in range(H):
        for x in range(W):
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            if d <= r and math.hypot(x + 0.5 - cx - ox, y + 0.5 - cy - oy) > r2:
                t = min(1, max(0, ((x - cx) + (y - cy) + r * 1.2) / (r * 2.4)))
                c = mix(stops[0], stops[1], t * 2) if t < 0.5 else mix(stops[1], stops[2], t * 2 - 1)
                if d > r - 1.3:
                    c = mix(c, hexrgb(CYAN_HI), 0.55)
                put(x, y, c)
    # Rocket: a vertical trail rising from the city, flare at its head.
    hx, hy = 39, 21
    for y in range(hy + 1, 40):
        put(hx, y, hexrgb(YELLOW), 0.95 * (1 - (y - hy) / (40 - hy)) ** 1.3)
    for dx in range(-7, 8):
        put(hx + dx, hy, hexrgb(YELLOW), 1 - abs(dx) / 8)
    for dy in (-2, -1, 1, 2):
        put(hx, hy + dy, hexrgb(YELLOW), 1 - abs(dy) / 3)
    put(hx, hy, hexrgb(YELLOW_HI))
    # City: (x, width, height, roof neon, top); 1-pixel gaps between towers.
    near = [(0, 5, 11, None, ""), (6, 4, 18, PINK, "antenna"), (11, 5, 9, None, ""), (17, 3, 21, None, "spire"),
            (21, 6, 14, CYAN, ""), (28, 4, 8, None, ""), (33, 4, 15, None, "step"), (38, 5, 11, PINK, ""),
            (44, 4, 16, CYAN, "antenna")]
    rnd = random.Random(5)
    fills = [hexrgb("#1D1F52"), hexrgb("#24275F")]
    for i, (x0, w, h, roof, top) in enumerate(near):
        y0 = H - h
        for y in range(y0, H):
            for x in range(x0, x0 + w):
                put(x, y, fills[i % 2])
        if top == "antenna":
            for y in range(y0 - 4, y0):
                put(x0 + w // 2, y, fills[i % 2])
        elif top == "spire":
            for k in range(1, 4):
                put(x0 + 1, y0 - k, fills[i % 2])
        elif top == "step":
            for x in range(x0 + 1, x0 + w - 1):
                put(x, y0 - 1, fills[i % 2])
        if roof:
            for x in range(x0, x0 + w):
                put(x, y0, hexrgb(roof))
        for y in range(y0 + 2, H - 1, 2):
            for x in range(x0 + 1, x0 + w - 1, 2):
                if rnd.random() < 0.3:
                    put(x, y, hexrgb(rnd.choice([CYAN, CYAN, YELLOW, PINK])))
    for y in range(H - 13, H - 6):                 # vertical neon sign
        put(35, y, hexrgb(PINK))
    return px


def halfblocks(px, bg=(11, 12, 36)):
    """Pixel grid -> lines of half-blocks in 24-bit colour; transparent stays the terminal's."""
    h, w = len(px), len(px[0])

    def col(p):
        if p is None or p[3] < 0.12:
            return None
        return mix(bg, p[:3], p[3])

    lines = []
    for y in range(0, h, 2):
        line, last = "", None
        for x in range(w):
            top = col(px[y][x])
            bot = col(px[y + 1][x]) if y + 1 < h else None
            if top is None and bot is None:
                code, ch = "\x1b[0m", " "
            elif bot is None:
                code, ch = "\x1b[0;38;2;%d;%d;%dm" % top, "▀"
            elif top is None:
                code, ch = "\x1b[0;38;2;%d;%d;%dm" % bot, "▄"
            else:
                code, ch = "\x1b[0;38;2;%d;%d;%d;48;2;%d;%d;%dm" % (top + bot), "▀"
            line += ("" if code == last else code) + ch
            last = code
        lines.append(line.rstrip(" ") + "\x1b[0m")
    return "\n".join(lines) + "\n"


def preview_unlock(logo, path):
    """The login screen as SDDM draws it: logo above a lock and password field."""
    fg, field = "#DDDDF7", "#141534"
    subprocess.run([
        "magick", "-size", "1920x1080", "xc:#0B0C24", str(logo), "-gravity", "center", "-geometry", "+0-60",
        "-composite", "+gravity",
        "-fill", field, "-stroke", fg, "-strokewidth", "2", "-draw", "rectangle 842,750 1126,796", "-stroke", "none",
        "-fill", fg, *sum((["-draw", f"circle {x},773 {x + 4},773"] for x in (864, 876, 888, 900)), []),
        "-fill", "none", "-stroke", fg, "-strokewidth", "5",
        "-draw", "path 'M 798,770 L 798,762 A 10,10 0 0 1 818,762 L 818,770'", "-stroke", "none",
        "-fill", fg, "-draw", "roundrectangle 791,768 825,792 4,4",
        "-fill", "#0B0C24", "-draw", "circle 808,778 811,778", "-draw", "rectangle 806,778 810,786",
        str(path)], check=True)


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        svg = pathlib.Path(tmp) / "unlock.svg"
        svg.write_text(scene(1416, 854, 2.0))
        subprocess.run(["rsvg-convert", "-w", "708", "-h", "427", str(svg), "-o", str(OUT / "unlock.png")], check=True)
    preview_unlock(OUT / "unlock.png", OUT / "preview-unlock.png")
    # fastfetch: 48 columns x 26 rows of half-blocks, drawn as pixel art.
    (OUT / "fastfetch-logo.txt").write_text(halfblocks(pixel_logo()))
    print("wrote unlock.png, preview-unlock.png, fastfetch-logo.txt")
