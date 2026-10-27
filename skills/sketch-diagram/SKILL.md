---
name: sketch-diagram
description: Draw minimalist, hand-drawn Excalidraw diagrams (flows, comparisons, simple charts) as Obsidian .excalidraw.md or plain .excalidraw files. Black ink, one red accent, no filled boxes. Use when asked for an Excalidraw drawing, a sketch-style flow, or a hand-drawn diagram.
---

# Sketch diagram

Hand-drawn Excalidraw diagrams with swappable themes. The default theme, `ink`, is the minimal one: ink on white, one red accent, plain handwriting, almost no boxes.

## Themes
`Sketch(theme="ink")` is the default. Others: `color` (blue titles, slate text, amber accent, light blue tint in boxes), `dark` (light ink on near-black, soft red accent), `blueprint` (pale ink on deep blue, yellow accent) and `pastel` (cream paper, violet titles, pink accent and tint). Code uses three roles (`INK` for text and lines, `RED` for the one accent, `GREY` for side notes) and the theme remaps them, so any drawing can be re-skinned by changing one argument. A theme also sets the canvas background, fill tint, title colour and roughness. To add a theme, add an entry to `THEMES` in `scripts/sketch.py`.


## Look (ink theme)
- Ink `#1e1e1e` for everything. Red `#c92a2a` for the one thing that matters. Grey `#868e96` for side notes. No other colours.
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

## Examples
`examples/make_examples.py <examples folder>` writes six generic drawings (a flow, a bar chart, a comparison, a workflow, a checklist and a summary) into one folder per theme mixing Chinese and English, with made-up numbers. Copy their layout. CJK text needs no special font; Excalidraw falls back to the system font. CJK characters count as one em wide for spacing.

## Slide layouts
`crumb`, `subtitle`, `checklist`, `rows` (label left, answer right, thin underline, last row red) and `closing` (one red underlined line) build text slides in the same look. Use one red element per slide.

## Obsidian notes
- File name must end `.excalidraw.md`. The plugin may rewrite plain JSON as compressed JSON on first save when its compress setting is on. That is harmless. Never hand-edit compressed data.
- Open it with `obsidian://open?vault=<vault>&file=<path without .md>`.
- Arrows are not bound to shapes, so they do not follow when a shape moves. Check the drawing visually; text width is estimated, so nudge if it looks off.

## Credit
Element schema and Obsidian file template follow the MIT-licensed excalidraw-diagram skill by Axton Liu (github.com/axtonliu/axton-obsidian-visual-skills).
