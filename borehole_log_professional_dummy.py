"""
Dummy version of professional borehole log plotting for testing with dummy lithology data.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd

# Dummy lithology data based on AGS file codes
DUMMY_BOREHOLE_DATA = pd.DataFrame(
    {
        "Depth_Top": [0.0, 0.5, 2.0, 4.5, 7.0, 10.0],
        "Depth_Base": [0.5, 2.0, 4.5, 7.0, 10.0, 15.0],
        "Geology_Code": [
            "101",  # TOPSOIL
            "102",  # MADE GROUND
            "201",  # CLAY
            "401",  # SAND
            "504",  # Sandy GRAVEL
            "801",  # MUDSTONE
        ],
        "Description": [
            "Dark brown silty TOPSOIL with roots",
            "Brown MADE GROUND with brick fragments",
            "Firm brown CLAY, slightly silty",
            "Medium dense fine SAND, some gravel",
            "Dense sandy GRAVEL, occasional cobbles",
            "Weathered MUDSTONE, grey, fissured",
        ],
    }
)


# Header drawing function from Borehole Log header.py
def draw_header(ax):
    ax.axis("off")

    # For a 4-inch wide log, use a grid that fills the axes from 0 to 1 in x
    x_start = 0.0
    total_width = 1.0
    row_height = 0.16  # Slightly shorter for top rows
    bottom_row_height = 0.24  # Taller bottom row
    y_start = 1.0
    font_kwargs = dict(fontsize=8)

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

    renderer = ax.figure.canvas.get_renderer()
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
            # Draw title
            title_text = top_labels[row][col]
            title_obj = ax.text(
                x + 0.01,
                y - row_height / 2,
                title_text,
                va="center",
                ha="left",
                **font_kwargs,
                fontweight="bold",
            )
            # Draw value left-aligned, just after the title
            ax.figure.canvas.draw()
            bbox = title_obj.get_window_extent(renderer=renderer)
            inv = ax.transData.inverted()
            bbox_data = inv.transform([(bbox.x1, bbox.y0)])
            value_x = bbox_data[0][0] + 0.01
            ax.text(
                value_x,
                y - row_height / 2,
                top_values[row][col],
                va="center",
                ha="left",
                fontsize=8,
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
                (x, y - bottom_row_height),
                col_width,
                bottom_row_height,
                edgecolor="black",
                facecolor="none",
                linewidth=1,
            )
        )
        # Draw title (top half)
        title_text = bottom_labels[i]
        title_obj = ax.text(
            x + col_width / 2,
            y - bottom_row_height * 0.40,
            title_text,
            va="top",
            ha="center",
            fontsize=7,
            fontweight="bold",
        )
        # Draw value (centered horizontally, below title)
        ax.text(
            x + col_width / 2,
            y - bottom_row_height * 0.80,
            bottom_values[i],
            va="top",
            ha="center",
            fontsize=7,
        )
        x += col_width


def plot_dummy_borehole_log():
    # Set header and log heights in inches
    header_height_in = 1.5
    log_height_per_meter = 0.5  # inches per meter of log
    log_depth = DUMMY_BOREHOLE_DATA["Depth_Base"].max()
    log_height_in = log_depth * log_height_per_meter
    fig_width_in = 6  # Increased width for better text fit
    fig_height_in = header_height_in + log_height_in

    fig = plt.figure(figsize=(fig_width_in, fig_height_in))

    # Axes placement: [left, bottom, width, height] in 0-1 figure coordinates
    header_ax = fig.add_axes(
        [
            0.08,
            1 - header_height_in / fig_height_in,
            0.84,
            header_height_in / fig_height_in,
        ]
    )
    draw_header(header_ax)

    log_ax = fig.add_axes(
        [
            0.08,
            0.08,
            0.84,
            (fig_height_in - header_height_in - 0.08 * fig_height_in) / fig_height_in,
        ]
    )

    for i, row in DUMMY_BOREHOLE_DATA.iterrows():
        log_ax.barh(
            y=(row["Depth_Top"] + row["Depth_Base"]) / 2,
            width=0.8,
            height=row["Depth_Base"] - row["Depth_Top"],
            left=0.1,
            color="#b0c4de",
            edgecolor="black",
            label=row["Geology_Code"] if i == 0 else "",
        )
        log_ax.text(
            0.5,
            (row["Depth_Top"] + row["Depth_Base"]) / 2,
            f"{row['Geology_Code']}",
            va="center",
            ha="center",
            fontsize=8,
            color="black",
            fontweight="bold",
        )
        log_ax.text(
            1.0,
            (row["Depth_Top"] + row["Depth_Base"]) / 2,
            row["Description"],
            va="center",
            ha="left",
            fontsize=7,
            color="black",
        )
    log_ax.set_ylim(DUMMY_BOREHOLE_DATA["Depth_Base"].max(), 0)
    log_ax.set_xlim(0, 3)
    log_ax.set_xlabel("")
    log_ax.set_ylabel("Depth (m)")
    log_ax.set_yticks(
        DUMMY_BOREHOLE_DATA["Depth_Top"].tolist()
        + [DUMMY_BOREHOLE_DATA["Depth_Base"].iloc[-1]]
    )
    log_ax.set_yticklabels(
        [f"{d:.2f}" for d in DUMMY_BOREHOLE_DATA["Depth_Top"].tolist()]
        + [f"{DUMMY_BOREHOLE_DATA['Depth_Base'].iloc[-1]:.2f}"]
    )
    log_ax.set_xticks([])
    log_ax.set_title("Dummy Borehole Log")

    plt.show()


if __name__ == "__main__":
    plot_dummy_borehole_log()
