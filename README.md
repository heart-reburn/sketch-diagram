# sketch-diagram

An agent skill that draws hand-drawn Excalidraw diagrams for Obsidian. The default look is minimal: charcoal ink on cream, one red accent, handwriting font, almost no filled boxes. Nine more themes re-skin the same drawings.

Output is `.excalidraw.md` (Obsidian Excalidraw plugin) or plain `.excalidraw`.

## What it draws

- Flows with underlined headings and dashed in-progress steps
- Bar charts with hachure bars
- Comparisons
- n8n-style node graphs (rounded nodes, labels outside, ports)
- Slide layouts: checklist, label-and-answer rows, closing line

## Themes

Ten themes in two families. The same drawings work in all of them.

**Hand-drawn** (wobbly strokes, handwriting font)

| Theme | Look |
|---|---|
| `paper` | Warm cream, charcoal ink, one crimson accent (default) |
| `color` | Blue titles, slate text, amber accent, light blue fill |
| `dark` | Light ink on near-black, soft red accent |
| `blueprint` | Pale ink on deep blue, yellow accent |
| `botanical` | Near-black, gold titles, dusty pink accent |
| `neon` | Navy, cyan titles, magenta accent |

**Clean** (straight strokes, other fonts, sharp or filled shapes)

| Theme | Look |
|---|---|
| `terminal` | GitHub dark, monospace font, green accent |
| `swiss` | White, black, one red, Helvetica, sharp corners |
| `notebook` | Cream page, Helvetica, rounded boxes in rotating pastel fills |
| `voltage` | Electric blue, white, neon yellow, Helvetica |

Ready-made files for every theme are in [`examples/`](examples/). Open any of them in Obsidian with the Excalidraw plugin.

```python
from sketch import Sketch
s = Sketch(theme="dark")
```

To add a theme, add an entry to `THEMES` in `skills/sketch-diagram/scripts/sketch.py`.

## Obsidian behavior

Obsidian keeps an open drawing in memory and writes it back, which undoes a file rewritten from outside. `save_obsidian` reads the vault's `.obsidian/workspace.json`, skips any drawing open in a tab, and tells you to close it and re-run. One drawing, one file; re-running overwrites.

## Install

Claude Code, as a plugin:

```
/plugin marketplace add heart-reburn/sketch-diagram
/plugin install sketch-diagram@sketch-diagram
```

Or copy `skills/sketch-diagram/` into `~/.claude/skills/`.

Regenerate the examples:

```
python3 -I skills/sketch-diagram/examples/make_examples.py examples
```

Python 3, standard library only.

## Credit

The Obsidian file format handling builds on [axtonliu/axton-obsidian-visual-skills](https://github.com/axtonliu/axton-obsidian-visual-skills) (MIT, Axton Liu).

## License

MIT. See [LICENSE](LICENSE).
