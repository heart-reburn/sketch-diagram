import os
"""Tiny helper for hand-drawn, minimalist Excalidraw diagrams.

Style: black ink on white, one red accent, no filled boxes, rough strokes.
Usage: from sketch import Sketch; s = Sketch(); s.title(...); s.save_obsidian(path)
"""
import json

INK, RED, GREY = "#1e1e1e", "#c92a2a", "#868e96"  # roles: text and lines, the one accent, side notes

# A theme remaps those three roles, so every drawing can be re-skinned with Sketch(theme=...).
# tint = light fill for boxes and nodes (None means no fill); title = heading colour.
THEMES = {
    "ink": dict(ink=INK, accent=RED, muted=GREY, tint=None, title=INK, roughness=2, bg="#ffffff"),
    "color": dict(ink="#374151", accent="#d97706", muted="#6b7280", tint="#dbeafe",
                  title="#1e40af", roughness=1, bg="#ffffff"),
    "dark": dict(ink="#e5e7eb", accent="#f87171", muted="#9ca3af", tint=None,
                 title="#ffffff", roughness=2, bg="#1b1b1f"),
    "blueprint": dict(ink="#e0f2fe", accent="#fde047", muted="#93c5fd", tint=None,
                      title="#ffffff", roughness=1, bg="#1e3a8a"),
    "pastel": dict(ink="#4b5563", accent="#ec4899", muted="#9ca3af", tint="#fce7f3",
                   title="#7c3aed", roughness=1, bg="#fffbf5"),
}
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
    def __init__(self, theme="ink", roughness=None, font=5):
        self.t = THEMES[theme]
        self.theme = theme
        self.els, self.n, self.font = [], 0, font
        self.rough = self.t["roughness"] if roughness is None else roughness
        self._roles = {INK: self.t["ink"], RED: self.t["accent"], GREY: self.t["muted"]}

    def _c(self, color):
        return self._roles.get(color, color)

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
                   backgroundColor=color if hatch else (self.t["tint"] or "transparent"),
                   fillStyle="hachure" if hatch else "solid")

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
                   backgroundColor=self.t["tint"] or "transparent", roundness={"type": 3})
        if glyph:
            self.text(glyph, x + size / 2 - text_width(glyph, 34) / 2, y + size / 2 - 22, 34, color)
        lines = label.split("\n")
        # above=True puts the text over the box, for nodes whose bottom edge has an arrow
        ly = y - 12 - (24 if sub else 0) - 22 * len(lines) if above else y + size + 10
        self.text(label, x + size / 2 - max(text_width(l, 18) for l in lines) / 2, ly, 18, color, "center")
        if sub:
            self.text(sub, x + size / 2 - text_width(sub, 14) / 2, ly + 2 + 22 * len(lines), 14, GREY)

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
