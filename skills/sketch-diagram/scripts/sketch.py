"""Tiny helper for hand-drawn, minimalist Excalidraw diagrams.

Style: black ink on white, one red accent, no filled boxes, rough strokes.
Usage: from sketch import Sketch; s = Sketch(); s.title(...); s.save_obsidian(path)
"""
import json
import os

INK, RED, GREY = "#1e1e1e", "#c92a2a", "#868e96"  # roles: text and lines, the one accent, side notes

# A theme remaps those three roles, so every drawing can be re-skinned with Sketch(theme=...).
# tint = light fill for boxes and nodes (None means no fill); title = heading colour.
THEMES = {
    # hand-drawn
    "paper": dict(panel="#f0ece4", ink=INK, accent="#c41e3a", muted="#7a746c", tint=None, title=INK, roughness=2, bg="#faf9f7"),
    "color": dict(panel="#dbeafe", ink="#374151", accent="#d97706", muted="#6b7280", tint="#dbeafe",
                  title="#1e40af", roughness=1, bg="#ffffff"),
    "dark": dict(panel="#2a2a30", ink="#e5e7eb", accent="#f87171", muted="#9ca3af", tint=None,
                 title="#ffffff", roughness=2, bg="#1b1b1f"),
    "blueprint": dict(panel="#1e40af", ink="#e0f2fe", accent="#fde047", muted="#93c5fd", tint=None,
                      title="#ffffff", roughness=1, bg="#1e3a8a"),
    "botanical": dict(panel="#1c1c1c", ink="#e8e4df", accent="#e8b4b8", muted="#9a9590", tint=None,
                      title="#d4a574", roughness=1, bg="#0f0f0f"),
    "neon": dict(panel="#111a2e", ink="#d1fae5", accent="#ff00aa", muted="#67e8f9", tint=None,
                 title="#00ffcc", roughness=1, bg="#0a0f1c"),
    # clean (no wobble, other fonts, sharp or filled shapes)
    "terminal": dict(panel="#161b22", ink="#c9d1d9", accent="#39d353", muted="#8b949e", tint=None,
                     title="#39d353", roughness=0, bg="#0d1117", font=3, round=False),
    "swiss": dict(panel="#f1f1f1", ink="#111111", accent="#ff3300", muted="#6b7280", tint=None,
                  title="#111111", roughness=0, bg="#ffffff", font=2, round=False),
    "notebook": dict(panel="#ffffff", ink="#1a1a1a", accent="#e11d48", muted="#6b6b6b", tint=None,
                     title="#1a1a1a", roughness=0, bg="#f8f6f1", font=2, round=True,
                     cards=["#98d4bb", "#c7b8ea", "#f4b8c5", "#a8d8ea", "#ffe6a7"]),
    "voltage": dict(panel="#1a1a2e", ink="#ffffff", accent="#d4ff00", muted="#bfdbfe", tint=None,
                    title="#d4ff00", roughness=0, bg="#0066ff", font=2, round=False),
}
# panel = fill for cards and split halves. Optional theme keys: font (5 hand, 2 Helvetica, 3 mono), round (rounded corners on boxes and nodes),
# cards (list of fills that boxes and nodes take in turn).
OBSIDIAN_HEADER = """---
excalidraw-plugin: parsed
tags: [excalidraw]
---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠==


# Excalidraw Data

## Text Elements
%%
## Drawing
```json
"""


def text_width(line, size):
    """Estimated pixel width: CJK characters are a full em, Latin about 0.55 em."""
    return sum(size if ord(c) > 0x2E80 else size * 0.55 for c in line)


def open_in_obsidian(path):
    """True if the file is listed as open in its vault's workspace.json (saving over it would be merged)."""
    path = os.path.abspath(path)
    d = os.path.dirname(path)
    while d != os.path.dirname(d):
        ws = os.path.join(d, ".obsidian", "workspace.json")
        if os.path.exists(ws):
            rel = os.path.relpath(path, d)
            try:
                layout = json.load(open(ws, encoding="utf-8"))
            except (OSError, ValueError):
                return False
            # only real tabs count; "lastOpenFiles" is just recent history

            def walk(n):
                if isinstance(n, dict):
                    if n.get("type") == "leaf" and n.get("state", {}).get("state", {}).get("file") == rel:
                        return True
                    return any(walk(v) for k, v in n.items() if k != "lastOpenFiles")
                if isinstance(n, list):
                    return any(walk(v) for v in n)
                return False
            return walk(layout)
        d = os.path.dirname(d)
    return False


class Sketch:
    def __init__(self, theme="paper", roughness=None, font=None):
        self.t = THEMES[theme]
        self.theme = theme
        self.els, self.n, self.card = [], 0, 0
        self.font = font or self.t.get("font", 5)
        self.rough = self.t["roughness"] if roughness is None else roughness
        self._roles = {INK: self.t["ink"], RED: self.t["accent"], GREY: self.t["muted"]}

    def _c(self, color):
        return self._roles.get(color, color)

    def _fill(self):
        """Next card colour for themes that fill shapes, else the tint, else none."""
        cards = self.t.get("cards")
        if cards:
            self.card += 1
            return cards[(self.card - 1) % len(cards)]
        return self.t["tint"] or "transparent"

    def _base(self, kind, x, y, w, h, **kw):
        self.n += 1
        d = dict(id=f"{kind}-{self.n}", type=kind, x=x, y=y, width=w, height=h, angle=0,
                 strokeColor=INK, backgroundColor="transparent", fillStyle="solid",
                 strokeWidth=1, strokeStyle="solid", roughness=self.rough, opacity=100,
                 groupIds=[], roundness=None, seed=3000 + self.n, version=1,
                 isDeleted=False, boundElements=None, updated=1, link=None, locked=False)
        d.update(kw)
        d["strokeColor"] = self._c(d["strokeColor"])
        d["backgroundColor"] = self._c(d["backgroundColor"])
        self.els.append(d)

    def text(self, s, x, y, size=20, color=INK, align="left", width=None):
        lines = s.split("\n")
        w = width or max(text_width(l, size) for l in lines)
        self._base("text", x, y, w, len(lines) * size * 1.25, strokeColor=color, text=s,
                   fontSize=size, fontFamily=self.font, textAlign=align, verticalAlign="top",
                   containerId=None, originalText=s, autoResize=True, lineHeight=1.25)

    def line(self, x1, y1, x2, y2, color=INK, width=2, style="solid"):
        self._base("line", x1, y1, x2 - x1, y2 - y1, strokeColor=color, strokeWidth=width,
                   strokeStyle=style, points=[[0, 0], [x2 - x1, y2 - y1]],
                   startBinding=None, endBinding=None, startArrowhead=None, endArrowhead=None)

    def arrow(self, x1, y1, x2, y2, color=INK, style="solid"):
        self._base("arrow", x1, y1, x2 - x1, y2 - y1, strokeColor=color, strokeStyle=style,
                   strokeWidth=2, roundness={"type": 2}, points=[[0, 0], [x2 - x1, y2 - y1]],
                   startBinding=None, endBinding=None, startArrowhead=None, endArrowhead="arrow")

    def box(self, x, y, w, h, color=INK, style="solid", hatch=False):
        self._base("rectangle", x, y, w, h, strokeColor=color, strokeStyle=style, strokeWidth=2,
                   backgroundColor=color if hatch else self._fill(),
                   fillStyle="hachure" if hatch else "solid",
                   roundness={"type": 3} if self.t.get("round") else None)

    def ellipse(self, x, y, w, h, color=INK, width=2):
        self._base("ellipse", x, y, w, h, strokeColor=color, strokeWidth=width)

    def curve(self, x1, y1, x2, y2, color=INK, style="solid"):
        """Smooth S-curve arrow, for branching connections between nodes."""
        dx, dy = x2 - x1, y2 - y1
        self._base("arrow", x1, y1, dx, dy, strokeColor=color, strokeStyle=style, strokeWidth=2,
                   roundness={"type": 2}, points=[[0, 0], [dx * 0.5, 0], [dx * 0.5, dy], [dx, dy]],
                   startBinding=None, endBinding=None, startArrowhead=None, endArrowhead="arrow")

    def node(self, x, y, label, sub="", glyph="", color=INK, size=90, above=False):
        """Workflow node: rough square, glyph inside, label and grey subtitle below."""
        self._base("rectangle", x, y, size, size, strokeColor=color, strokeWidth=2,
                   backgroundColor=self._fill(),
                   roundness={"type": 3} if self.t.get("round", True) else None)
        if glyph:
            self.text(glyph, x + size / 2 - text_width(glyph, 34) / 2, y + size / 2 - 22, 34, color)
        lines = label.split("\n")
        # above=True puts the text over the box, for nodes whose bottom edge has an arrow
        ly = y - 12 - (24 if sub else 0) - 22 * len(lines) if above else y + size + 10
        self.text(label, x + size / 2 - max(text_width(l, 18) for l in lines) / 2, ly, 18, color, "center")
        if sub:
            self.text(sub, x + size / 2 - text_width(sub, 14) / 2, ly + 2 + 22 * len(lines), 14, GREY)

    # ---- layout pieces: cards, pills, stats, timeline, split panels, tabs ----
    def panel(self, x, y, w, h, fill=None, stroke=None):
        """Solid filled block. Fill defaults to the theme panel colour; no outline unless stroke is given."""
        fill = fill or self.t["panel"]
        self._base("rectangle", x, y, w, h, strokeColor=stroke or fill, backgroundColor=fill,
                   strokeWidth=2 if stroke else 1, roundness={"type": 3} if self.t.get("round") else None)

    def pill(self, x, y, label, color=INK, size=16, filled=False):
        """Small rounded tag. Returns its width so tags can be laid out in a row."""
        w, h = text_width(label, size) + 32, size * 1.25 + 16
        self._base("rectangle", x, y, w, h, strokeColor=color, strokeWidth=2, roundness={"type": 3},
                   backgroundColor=self._fill() if filled else "transparent")
        self.text(label, x + 16, y + 8, size, color)
        return w

    def stat(self, x, y, w, h, value, label, color=INK):
        """Card with a big number and a small label under it."""
        self.panel(x, y, w, h, self._fill() if self.t.get("cards") else None)
        self.text(value, x + 24, y + 22, 54, color)
        self.text(label, x + 24, y + h - 44, 16, GREY)

    def timeline(self, items, x=80, y=300, step=260, current=None):
        """Horizontal line with a dot per item; item = (when, what). The current one is red."""
        self.line(x, y, x + step * (len(items) - 1) + 40, y, INK, 2)
        for i, (when, what) in enumerate(items):
            cx, c = x + i * step, RED if i == current else INK
            self.ellipse(cx - 10, y - 10, 20, 20, c, 3)
            self.text(when, cx - text_width(when, 24) / 2, y - 62, 24, c)
            self.text(what, cx - max(text_width(l, 18) for l in what.split("\n")) / 2, y + 28, 18, INK, "center")

    def split(self, left_w=460, w=1200, h=700, fill=None):
        """Two halves: the right one is a panel. Put the big title on the left, the content on the right."""
        self.panel(left_w, 0, w - left_w, h, fill)

    def tabs(self, labels, x=60, y=40, w=860, h=560):
        """A page with coloured index tabs sticking out of its right edge; the first tab is the active one."""
        self.panel(x, y, w, h, self.t["bg"], INK)
        for i, lab in enumerate(labels):
            ty = y + 30 + i * 70
            self.panel(x + w, ty, 40 + text_width(lab, 18) + 24, 56, self._fill() if self.t.get("cards") else None,
                       RED if i == 0 else None)
            self.text(lab, x + w + 20, ty + 15, 18, RED if i == 0 else INK)

    def crumb(self, s, x=40, y=24, width=1100):
        """Slide look: tiny grey section crumb with a thin rule under it."""
        self.text(s, x, y, 14, GREY)
        self.line(x, y + 30, x + width, y + 30, GREY, 1)

    def subtitle(self, s, x=40, y=150):
        self.text("(" + s + ")", x, y, 16, GREY)

    def checklist(self, items, x=40, y=240, step=75, size=24):
        """Empty square plus label per row."""
        for i, t in enumerate(items):
            yy = y + i * step
            self.box(x, yy, 34, 34)
            self.text(t, x + 60, yy + 1, size)

    def rows(self, pairs, x=40, y=240, step=100, label_w=250, line_w=800, red_last=True):
        """Label column on the left, answer on the right, thin underline per row; last row red."""
        for i, (label, answer) in enumerate(pairs):
            yy = y + i * step
            c = RED if red_last and i == len(pairs) - 1 else INK
            self.text(label, x, yy + 4, 20, c)
            self.text(answer, x + label_w, yy, 22, INK)
            self.line(x + label_w, yy + 44, x + label_w + line_w, yy + 44, c if c == RED else GREY, 1)

    def closing(self, s, x=40, y=480, size=24):
        """One red line, underlined: the point of the slide."""
        self.text(s, x, y, size, RED)
        self.line(x, y + size + 12, x + text_width(s, size), y + size + 12, RED, 2)

    def title(self, s, x=60, y=40, size=32, underline=True):
        self.text(s, x, y, size, self.t["title"])
        if underline:
            self.line(x, y + size * 1.4, x + text_width(s, size), y + size * 1.4, self.t["title"])

    def data(self):
        return dict(type="excalidraw", version=2, source="https://excalidraw.com",
                    elements=self.els, appState=dict(gridSize=None, viewBackgroundColor=self.t["bg"]),
                    files={})

    def save_obsidian(self, path, overwrite=True):
        """Overwrites by default. Close the drawing in Obsidian first, or the open scene merges into the rewrite. Pass overwrite=False to skip existing files."""
        if os.path.exists(path) and not overwrite:
            print("exists, skipped:", path)
            return False
        if open_in_obsidian(path):
            print("OPEN in Obsidian, skipped (close the tab, then re-run):", path)
            return False
        with open(path, "w", encoding="utf-8") as f:
            f.write(OBSIDIAN_HEADER + json.dumps(self.data()) + "\n```\n%%\n")

    def save_excalidraw(self, path, overwrite=True):
        if os.path.exists(path) and not overwrite:
            print("exists, skipped:", path)
            return False
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.data(), f)
