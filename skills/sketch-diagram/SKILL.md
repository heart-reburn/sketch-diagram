---
name: sketch-diagram
description: Draw minimalist, hand-drawn Excalidraw diagrams (flows, comparisons, simple charts) as Obsidian .excalidraw.md or plain .excalidraw files. Minimal by default (ink, one red accent, no filled boxes) with ten themes, hand-drawn or clean. Use when asked for an Excalidraw drawing, a sketch-style flow, or a hand-drawn diagram.
---

# Sketch diagram

Hand-drawn Excalidraw diagrams with swappable themes. The default theme, `paper`, is the minimal one: ink on cream, one red accent, plain handwriting, almost no boxes.

## Themes
`Sketch(theme="paper")` is the default. Two families share one set of drawings.

Hand-drawn (wobbly strokes, handwriting font): `paper` (warm cream, charcoal ink, crimson accent; the minimal one), `color` (blue titles, slate text, amber accent, light blue boxes), `dark`, `blueprint` (pale ink on deep blue, yellow accent), `botanical` (near-black, gold titles, dusty pink accent) and `neon` (navy, cyan titles, magenta accent).

Clean (straight strokes, other fonts, sharp or filled shapes): `terminal` (GitHub dark, mono font, green accent), `swiss` (white, black, one red, Helvetica, sharp corners), `notebook` (cream page, Helvetica, rounded boxes in rotating pastel fills) and `voltage` (electric blue, white, neon yellow, Helvetica).

Code uses three roles (`INK` for text and lines, `RED` for the one accent, `GREY` for side notes) and the theme remaps them, so any drawing can be re-skinned by changing one argument. A theme sets canvas background, title colour, roughness, and optionally `font`, `round` (rounded corners), `tint` (one box fill) and `cards` (fills used in turn). To add a theme, add an entry to `THEMES` in `scripts/sketch.py`.


## Look (paper theme)
- Ink for everything. Red (crimson in this theme) for the one thing that matters. Grey for side notes. No other colours.
- No filled boxes. Steps are plain text joined by thin arrows. Use a box only for a callout, dashed red for "in progress" or "exception".
- Headings get an underline stroke, not a box. Subtitles are small and grey.
- Bars and areas use hachure fill (diagonal hatch). A bar not yet reached is a dashed red outline, empty.
- Roughness 2, stroke width 1–2, font Excalifont (`fontFamily: 5`). For a looser look use Virgil (`fontFamily: 1`).
- Text 18–24, titles 32. Left-align lists. Space steps about 90 px apart. Keep the canvas near 1000 x 700.
- No emoji. Plain words. One idea per drawing.

## How
1. Import the helper: `sys.path.insert(0, "<skill dir>/scripts"); from sketch import Sketch, RED, GREY`.
2. Build with `title`, `text`, `arrow`, `line`, `box`. Coordinates are canvas pixels, y grows down.
3. Save with `save_obsidian("Name.excalidraw.md")` or `save_excalidraw("Name.excalidraw")`. One drawing, one file: reuse the same name and never make `v2`/`copy` files. `save_*` overwrites by default; `save_obsidian` checks the vault's `workspace.json` and refuses (prints "OPEN in Obsidian, skipped") while the drawing is open; ask the user to close the tab, then re-run. This matters because an open drawing gets merged into the rewrite and the old and new scenes land on top of each other. Pass `overwrite=False` to skip files that already exist. Never copy a header from a drawing the plugin has already saved.
4. Run Python with `-I`.

## Layouts
Beyond flows and charts, `Sketch` has layout pieces borrowed from slide design: `panel` (solid block), `pill` (tag), `stat` (big-number card), `timeline`, `split` (title left, panel right) and `tabs` (page with index tabs). `examples/make_examples.py` shows each one: stats, timeline, split, tabs and cover.

## Examples
`examples/make_examples.py <examples folder>` writes eleven generic drawings (a flow, a bar chart, a comparison, a workflow, a checklist, a summary, stat cards, a timeline, a split panel, notebook tabs and a cover) into one folder per theme mixing Chinese and English, with made-up numbers. Copy their layout. CJK text needs no special font; Excalidraw falls back to the system font. CJK characters count as one em wide for spacing.

## Slide layouts
`crumb`, `subtitle`, `checklist`, `rows` (label left, answer right, thin underline, last row red) and `closing` (one red underlined line) build text slides in the same look. Use one red element per slide.

## Obsidian notes
- File name must end `.excalidraw.md`. The plugin may rewrite plain JSON as compressed JSON on first save when its compress setting is on. That is harmless. Never hand-edit compressed data.
- Open it with `obsidian://open?vault=<vault>&file=<path without .md>`.
- Arrows are not bound to shapes, so they do not follow when a shape moves. Check the drawing visually; text width is estimated, so nudge if it looks off.

## Credit
Element schema and Obsidian file template follow the MIT-licensed excalidraw-diagram skill by Axton Liu (github.com/axtonliu/axton-obsidian-visual-skills).
