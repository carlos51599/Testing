import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def draw_header(ax):
    ax.axis("off")

    x_start = 0.02
    total_width = 0.96  # margin of 0.02 left/right
    row_height = 0.04
    y_start = 0.95
    font_kwargs = dict(va="center", ha="left", fontsize=9)

    # Top 3 rows — 3 equal-width columns
    top_labels = [
        ["Project Name:", "Client:", "Date:"],
        ["Location:", "Contractor:", "Co-ords:"],
        ["Project No.:", "Crew Name:", "Drilling Equipment:"],
    ]
    top_values = [
        ["SESRO", "Thames Water", ""],
        ["Abingdon, Oxfordshire", "", "E443012.50 N195881.00"],
        ["303568-00", "", ""],
    ]

    col_widths = [total_width / 3] * 3

    for row in range(3):
        y = y_start - row * row_height
        x = x_start
        for col in range(3):
            w = col_widths[col]
            ax.add_patch(
                Rectangle(
                    (x, y - row_height),
                    w,
                    row_height,
                    edgecolor="black",
                    facecolor="none",
                    linewidth=1,
                )
            )
            ax.text(
                x + 0.005,
                y - row_height / 2 + 0.002,
                top_labels[row][col],
                **font_kwargs,
                fontweight="bold"
            )
            ax.text(
                x + 0.15,
                y - row_height / 2 + 0.002,
                top_values[row][col],
                **font_kwargs
            )
            x += w

    # Bottom row — 6 equal-width boxes (1/6 each)
    bottom_labels = [
        "Borehole Number",
        "Hole Type",
        "Level",
        "Logged By",
        "Scale",
        "Page Number",
    ]
    bottom_values = ["BH01", "CP+RC", "62.50m AoD", "", "1:50", "Sheet 4 of 5"]

    y = y_start - 3 * row_height
    col_width = total_width / 6
    x = x_start
    for i in range(6):
        ax.add_patch(
            Rectangle(
                (x, y - row_height),
                col_width,
                row_height,
                edgecolor="black",
                facecolor="none",
                linewidth=1,
            )
        )
        ax.text(
            x + 0.005,
            y - row_height / 2 + 0.002,
            bottom_labels[i],
            **font_kwargs,
            fontweight="bold"
        )
        ax.text(x + 0.11, y - row_height / 2 + 0.002, bottom_values[i], **font_kwargs)
        x += col_width


# Generate the figure with just the header
fig, ax = plt.subplots(figsize=(8.5, 2))  # Just enough height for header
draw_header(ax)
plt.tight_layout()
plt.show()
