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

    x = x_start
    import matplotlib as mpl

    # Header content
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
    bottom_labels = [
        "Borehole Number",
        "Hole Type",
        "Level",
        "Logged By",
        "Scale",
        "Page Number",
    ]
    bottom_values = ["BH01", "CP+RC", "62.50m AoD", "", "1:50", "Sheet 4 of 5"]

    # Use a temporary figure to measure text widths
    tmp_fig = plt.figure(figsize=(8, 2))
    tmp_ax = tmp_fig.add_subplot(111)
    renderer = tmp_fig.canvas.get_renderer()
    fontprops = mpl.font_manager.FontProperties(size=8)
    cell_padd = 12  # pixels, padding left and right

    # Top 3 rows
    max_top_widths = []
    for row in range(3):
        for col in range(3):
            title = top_labels[row][col]
            value = top_values[row][col]
            t_width = tmp_ax.figure.canvas.get_renderer().get_text_width_height_descent(
                title, fontprops, ismath=False
            )[0]
            v_width = tmp_ax.figure.canvas.get_renderer().get_text_width_height_descent(
                value, fontprops, ismath=False
            )[0]
            max_top_widths.append(t_width + v_width + cell_padd)

    # Bottom row
    max_bottom_widths = []
    for i in range(6):
        title = bottom_labels[i]
        value = bottom_values[i]
        t_width = tmp_ax.figure.canvas.get_renderer().get_text_width_height_descent(
            title, fontprops, ismath=False
        )[0]
        v_width = tmp_ax.figure.canvas.get_renderer().get_text_width_height_descent(
            value, fontprops, ismath=False
        )[0]
        max_bottom_widths.append(max(t_width, v_width) + cell_padd)

    # For the top 3 rows (3 columns), find max width for each column
    top_col_widths_px = [
        max(
            max_top_widths[i],
            max_top_widths[i + 3],
            max_top_widths[i + 6],
        )
        for i in range(3)
    ]
    # For the bottom row (6 columns), use its own widths
    bottom_col_widths_px = max_bottom_widths
    # For a simple fix, set total width as sum of bottom row widths (since that's the widest)
    col_widths_px = bottom_col_widths_px
    total_width_px = sum(col_widths_px)
    dpi = tmp_fig.dpi
    fig_width_in = total_width_px / dpi
    plt.close(tmp_fig)

    # Draw the complete header grid on the provided axes
    # Top 3 rows (3 columns each)
    top_row_height = 0.2  # Each of the 3 top rows takes 20% of axes height (reduced to make room for new row)

    # Draw top 3 rows
    for row in range(3):
        y_pos = 1.0 - (row * top_row_height)  # Start from top
        for col in range(3):
            col_width = 1.0 / 3.0  # Equal width for 3 columns
            x_pos = col * col_width

            # Draw cell rectangle
            ax.add_patch(
                Rectangle(
                    (x_pos, y_pos - top_row_height),
                    col_width,
                    top_row_height,
                    edgecolor="black",
                    facecolor="none",
                    linewidth=1,
                )
            )

            # Draw label and value
            label = top_labels[row][col]
            value = top_values[row][col]

            # Label (bold, upper part of cell)
            if label:
                ax.text(
                    x_pos + col_width * 0.05,
                    y_pos - top_row_height * 0.2,
                    label,
                    va="top",
                    ha="left",
                    fontsize=8,  # Increased font size
                    fontweight="bold",
                )

            # Value (normal, lower part of cell)
            if value:
                ax.text(
                    x_pos + col_width * 0.05,
                    y_pos - top_row_height * 0.6,
                    value,
                    va="top",
                    ha="left",
                    fontsize=8,  # Increased font size
                )

    # Draw bottom row rectangles and text
    # We'll use axes coordinates (0-1) for x/y, and scale col_widths_px to axes width
    total_col_width_px = sum(col_widths_px)
    axes_width = 1.0  # ax spans 0-1 in x
    px_to_axes = axes_width / total_col_width_px
    x = 0.0
    bottom_row_height = (
        0.2  # fraction of axes height for bottom row (reduced to make room for new row)
    )
    for i in range(6):
        col_width = col_widths_px[i] * px_to_axes
        ax.add_patch(
            Rectangle(
                (x, 0.2),  # Bottom row at y=0.2 to make room for new row below
                col_width,
                bottom_row_height,
                edgecolor="black",
                facecolor="none",
                linewidth=1,
            )
        )
        # Draw title (near top of cell)
        title_text = bottom_labels[i]
        ax.text(
            x + col_width / 2,
            0.2 + bottom_row_height * 0.85,
            title_text,
            va="top",
            ha="center",
            fontsize=8,  # Increased font size
            fontweight="bold",
        )
        # Draw value (centered horizontally, lower in cell)
        ax.text(
            x + col_width / 2,
            0.2 + bottom_row_height * 0.35,
            bottom_values[i],
            va="top",
            ha="center",
            fontsize=8,  # Increased font size
        )
        x += col_width

    # Draw new additional row at the bottom
    new_row_height = 0.2  # fraction of axes height for new row

    # Define column widths for the new row (adjusted for better text fitting)
    # Increased proportions to accommodate longer text while maintaining relationships
    new_col_widths = [0.08, 0.12, 0.08, 0.12, 0.08, 0.08, 0.08, 0.32, 0.04]
    # Well, Depth, Type, Results, Depth, Level, Legend, Stratum, Empty
    new_col_labels = [
        "Well",
        "Depth (m)",
        "Type",
        "Results",
        "Depth\n(m)",
        "Level\n(m)",
        "Legend",
        "Stratum Description",
        "",
    ]

    x = 0.0
    for i, (col_width, label) in enumerate(zip(new_col_widths, new_col_labels)):
        # Draw cell rectangle
        ax.add_patch(
            Rectangle(
                (x, 0),  # New row at very bottom (y=0)
                col_width,
                new_row_height,
                edgecolor="black",
                facecolor="none",
                linewidth=1,
            )
        )

        # Special handling for "Sample and In Situ Testing" merged header
        if i == 1:  # First sub-column of the merged section
            # Draw the merged header text spanning columns 1, 2, 3
            merged_width = new_col_widths[1] + new_col_widths[2] + new_col_widths[3]
            ax.text(
                x + merged_width / 2,
                new_row_height * 0.9,
                "Sample and In Situ Testing",
                va="top",
                ha="center",
                fontsize=8,  # Increased font size
                fontweight="bold",
            )
            # Draw horizontal line to separate merged header from sub-headers
            ax.plot(
                [x, x + merged_width],
                [new_row_height * 0.6, new_row_height * 0.6],
                "k-",
                linewidth=1,
            )

        # Draw sub-column labels
        if i in [1, 2, 3]:  # Sub-columns under "Sample and In Situ Testing"
            ax.text(
                x + col_width / 2,
                new_row_height * 0.4,
                label,
                va="top",
                ha="center",
                fontsize=7,  # Increased font size
                fontweight="bold",
            )
        elif label:  # Other column labels
            ax.text(
                x + col_width / 2,
                new_row_height / 2,
                label,
                va="center",
                ha="center",
                fontsize=8,  # Increased font size
                fontweight="bold",
            )

        x += col_width


def plot_dummy_borehole_log():
    # Calculate required width based on text content for A4 layout
    # A4 width is 8.27 inches, minus margins (0.5" each side) = 7.27" usable
    a4_usable_width = 7.27

    # Set header and log heights in inches
    header_height_in = 2.0  # Increased to accommodate better text fitting
    log_height_per_meter = 0.5  # inches per meter of log
    log_depth = DUMMY_BOREHOLE_DATA["Depth_Base"].max()
    log_height_in = log_depth * log_height_per_meter

    # Use A4 usable width for the figure
    fig_width_in = a4_usable_width
    fig_height_in = header_height_in + log_height_in + 0.5  # Add bottom margin

    fig = plt.figure(figsize=(fig_width_in, fig_height_in))

    # Use two perfectly aligned axes: one for header, one for log
    margin = 0.02  # 2% margin on each side
    axes_left = margin
    axes_width = 1 - 2 * margin
    header_height_frac = header_height_in / fig_height_in
    log_height_frac = 1 - header_height_frac - margin
    # Header axes (top)
    header_ax = fig.add_axes(
        [
            axes_left,
            1 - header_height_frac,
            axes_width,
            header_height_frac - margin / 2,
        ]
    )
    draw_header(header_ax)
    header_ax.set_xlim(0, 1)
    header_ax.set_ylim(0, 1)
    header_ax.axis("off")
    # Log axes (bottom)
    log_ax = fig.add_axes(
        [
            axes_left,
            margin,
            axes_width,
            log_height_frac,
        ]
    )
    from matplotlib.patches import Rectangle as MplRectangle

    log_ax.add_patch(
        MplRectangle((0, 0), 1, 1, fill=False, edgecolor="red", linewidth=1, zorder=10)
    )
    log_ax.set_xlim(0, 1)
    log_ax.set_ylim(0, 1)
    log_ax.axis("off")
    # Now plot the lithology bars and text in the log area, using the same normalized coordinates
    col_props = [0.08, 0.12, 0.08, 0.12, 0.08, 0.08, 0.08, 0.32, 0.04]
    col_x = [0]
    for w in col_props:
        col_x.append(col_x[-1] + w)
    bar_left = col_x[7]
    bar_width = col_props[7]
    desc_x = bar_left + 0.01
    code_x = bar_left + bar_width * 0.15
    log_depth = DUMMY_BOREHOLE_DATA["Depth_Base"].max()

    def depth_to_y(depth):
        return 1 - depth / log_depth

    for i, row in DUMMY_BOREHOLE_DATA.iterrows():
        y_top = depth_to_y(row["Depth_Top"])
        y_base = depth_to_y(row["Depth_Base"])
        y_center = (y_top + y_base) / 2
        log_ax.add_patch(
            MplRectangle(
                (bar_left + bar_width * 0.025, y_base),
                bar_width * 0.95,
                y_top - y_base,
                facecolor="#b0c4de",
                edgecolor="black",
                linewidth=1,
                zorder=2,
            )
        )
        log_ax.text(
            code_x,
            y_center,
            f"{row['Geology_Code']}",
            va="center",
            ha="left",
            fontsize=8,
            color="black",
            fontweight="bold",
            zorder=3,
        )
        log_ax.text(
            desc_x + bar_width * 0.18,
            y_center,
            row["Description"],
            va="center",
            ha="left",
            fontsize=7,
            color="black",
            zorder=3,
        )

    plt.show()
    plt.close(fig)


if __name__ == "__main__":
    plot_dummy_borehole_log()
