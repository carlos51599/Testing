import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# Load the JSON file
with open("borehole_layout_page1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

table = data["tables"][0]
columns = table["columns"]
rows = table["rows"]

n_cols = len(columns)
n_rows = len(rows)

# A4 portrait size in inches
fig_w, fig_h = 8.3, 11.7
fig, ax = plt.subplots(figsize=(fig_w, fig_h))

# Margins and cell size
margin_x = 0.5
margin_y = 0.5
usable_w = fig_w - 2 * margin_x
usable_h = fig_h - 2 * margin_y
cell_w = usable_w / n_cols
cell_h = usable_h / n_rows

# Draw grid and text
for i, row in enumerate(rows):
    for j, cell in enumerate(row):
        x = margin_x + j * cell_w
        y = fig_h - margin_y - (i + 1) * cell_h
        # Draw cell border
        rect = patches.Rectangle(
            (x, y), cell_w, cell_h, linewidth=0.5, edgecolor="black", facecolor="none"
        )
        ax.add_patch(rect)
        # Get style
        style = cell.get("style", {})
        size = style.get("size", 10)
        weight = "bold" if style.get("bold") else "normal"
        italic = style.get("italic")
        fontstyle = "italic" if italic else "normal"
        align = style.get("alignment", "LEFT")
        ha = {"LEFT": "left", "CENTER": "center", "RIGHT": "right"}.get(align, "left")
        va = "center"
        # Text
        import re

        clean_text = re.sub(r"[^\x20-\x7E\n]", "", cell.get("text", ""))
        ax.text(
            x
            + (
                0.02
                if ha == "left"
                else 0.5 * cell_w if ha == "center" else cell_w - 0.02
            ),
            y + 0.5 * cell_h,
            clean_text,
            fontsize=size,
            fontweight=weight,
            fontstyle=fontstyle,
            ha=ha,
            va=va,
            wrap=True,
            clip_on=True,
            zorder=10,
        )

ax.set_xlim(0, fig_w)
ax.set_ylim(0, fig_h)
ax.axis("off")
plt.tight_layout()
plt.savefig("borehole_layout_page1_plot.png", dpi=300)
plt.show()
