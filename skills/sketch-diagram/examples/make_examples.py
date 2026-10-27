"""Writes generic example drawings (mixed Chinese and English), one folder per theme. All numbers are made up.
Run: python3 -I make_examples.py <examples dir>   (writes <examples dir>/<theme>/...; close open drawings first)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from sketch import Sketch, RED, GREY, INK, THEMES


def build(theme, out):
    os.makedirs(out, exist_ok=True)
    # 1. Flow
    s = Sketch(theme=theme)
    s.text("流程 · Process", 60, 30, 18, GREY)
    s.line(60, 60, 1000, 60, GREY, 1)
    s.title("上线流程 Launch flow", 60, 90, 30)
    s.text("四步，出错就回到开发 · four steps, bugs go back to build", 60, 150, 18, GREY)
    y = 230
    for t in ["写需求 Write the spec", "开发 Build", "测试 Test"]:
        s.text(t, 100, y, 24)
        s.arrow(130, y + 36, 130, y + 76)
        y += 84
    s.text("发布 Ship it", 100, y, 24, RED)
    s.line(100, y + 36, 280, y + 36, RED, 2)
    s.text("测试没过 Tests fail", 400, 400, 22, RED)
    s.arrow(390, 420, 260, 330, RED, "dashed")
    s.save_obsidian(os.path.join(out, "Example flow.excalidraw.md"))

    # 2. Bar chart
    c = Sketch(theme=theme)
    c.title("月度注册 Monthly sign-ups", 60, 30, 30)
    c.text("示例数据 · made-up numbers; red dashed = in progress", 60, 90, 18, GREY)
    base = 520
    c.line(60, base, 780, base, INK, 2)
    for x, h, lab, v in [(100, 0, "5月", "0"), (220, 0, "6月", "0"), (340, 50, "7月", "230"),
                         (460, 110, "8月", "460"), (580, 260, "9月", "1,560")]:
        if h:
            c.box(x, base - h, 90, h, INK, hatch=True)
        c.text(v, x + 45 - len(v) * 6, base - h - 34, 22)
        c.text(lab, x + 45 - 20, base + 14, 20)
    c.box(700, base - 380, 90, 380, RED, "dashed")
    c.text("2,500", 700 + 45 - 28, base - 380 - 34, 22, RED)
    c.text("10月 now", 700 + 45 - 38, base + 14, 20, RED)
    c.arrow(900, base - 190, 820, base - 190, RED)
    c.text("在做 in progress", 905, base - 204, 18, RED)
    c.save_obsidian(os.path.join(out, "Example bar chart.excalidraw.md"))

    # 3. Two-column slide
    d = Sketch(theme=theme)
    d.text("对比 · Comparison", 60, 30, 18, GREY)
    d.line(60, 60, 1000, 60, GREY, 1)
    d.text("示例数据 · made-up numbers", 60, 90, 18, GREY)
    d.title("但把时间拆开，画面完全变了 Split by time", 60, 130, 28)
    d.text("在退潮 Fading", 60, 240, 24)
    d.line(60, 276, 240, 276, INK, 2)
    for i, r in enumerate(["Tool A  37.5 → 28.3  ↓", "Tool B  38.1 → 29.1  ↓", "Tool C  25.0 → 16.1  ↓"]):
        d.text(r, 60, 300 + i * 44, 20)
    d.text("在起飞 Rising", 560, 240, 24, RED)
    d.line(560, 276, 740, 276, RED, 2)
    for i, r in enumerate(["Tool X  19.8 → 30.8  ↑", "Tool Y  16.9 → 25.5  ↑", "Tool Z   4.9 → 11.5  ↑"]):
        d.text(r, 560, 300 + i * 44, 20, RED)
    d.text("从「串工具」→「造一个能自己干活的东西」", 60, 500, 24, RED)
    d.line(60, 536, 600, 536, RED, 2)
    d.save_obsidian(os.path.join(out, "Example comparison.excalidraw.md"))

    # 4. Workflow (n8n-style, sketched): one main row, side exits go straight up. 
    def workflow(name):
        w = Sketch(theme=theme)
        w.title("线索处理 Lead workflow", 60, 20, 30)
        w.text("示例 · generic automation, hand-sketched", 60, 80, 18, GREY)
        Y, TOP = 370, 200
        xs = [60, 300, 540, 780, 1020, 1260]
        w.node(xs[0], Y, "Validate Lead", "检查 rules", "if")
        w.node(xs[1], Y, "Search by Email", "search: contact")
        w.ellipse(xs[1] + 22, Y + 22, 30, 30); w.line(xs[1] + 48, Y + 48, xs[1] + 66, Y + 66, INK, 3)
        w.node(xs[2], Y, "Is Duplicate?", "", "=?")
        w.node(xs[3], Y, "Score Lead\n(LLM)", "打分 model", "AI", RED)
        w.node(xs[4], Y, "Parse Score", "", "{ }")
        w.node(xs[5], Y, "Apply Rules\nFloor", "", "{ }")
        w.node(xs[0], TOP, "Log Incomplete", "append: sheet", "≡", above=True)
        w.node(xs[2], TOP, "Log Duplicate", "append: sheet", "≡", above=True)
        for a, b in zip(xs, xs[1:]):
            w.arrow(a + 100, Y + 45, b - 10, Y + 45)
        w.arrow(xs[0] + 45, Y - 10, xs[0] + 45, TOP + 98)
        w.arrow(xs[2] + 45, Y - 10, xs[2] + 45, TOP + 98)
        w.text("缺邮箱 missing", xs[0] + 60, Y - 52, 16, GREY)
        w.text("true", xs[2] + 60, Y - 52, 16, GREY)
        w.text("valid", xs[0] + 112, Y + 12, 16, GREY)
        w.text("false", xs[2] + 112, Y + 12, 16, GREY)
        w.save_obsidian(os.path.join(out, name))


    workflow("Example workflow.excalidraw.md")

    # 5. Checklist slide
    c = Sketch(theme=theme)
    c.crumb("清单 · Checklist")
    c.title("上线当天 Launch day", 40, 80, 32)
    c.subtitle("提交一条测试数据，看它自己走完 · send one test record and watch it go through")
    c.checklist(["数据进来 Record arrives", "校验通过 Validation passes", "分数出来 Score appears",
                 "联系人建好 Contact created", "Slack 提醒到 Alert lands"], y=240)
    c.closing("跑起来给他看，他心里就有底了。 Show it running.", 40, 660)
    c.save_obsidian(os.path.join(out, "Example checklist.excalidraw.md"))

    # 6. Label-and-answer slide
    r = Sketch(theme=theme)
    r.crumb("总结 · Summary")
    r.title("一页说清 The brief in four lines", 40, 80, 32)
    r.subtitle("先想清楚，一次说完 · think first, say it once")
    r.rows([("要什么结果 Goal", "一张流程图，一屏能看完 · one diagram that fits one screen"),
            ("背景 Context", "小团队，客户从网站表单进来 · small team, leads arrive from a web form"),
            ("限制 Limits", "只画图，不接账号 · draw only, connect no accounts"),
            ("怎么才算做完 Done when", "每一步都有对应的框 · every step has a box")], y=240)
    r.closing("最后一段最容易漏。 The last line is the one people skip.", 40, 700)
    r.save_obsidian(os.path.join(out, "Example summary.excalidraw.md"))


root = sys.argv[1]
for name in THEMES:
    build(name, os.path.join(root, name))
print("wrote", list(THEMES), "to", root)
