"""
Dummy version of professional borehole log plotting for testing with dummy lithology data.
"""

import matplotlib.pyplot as plt
import numpy as np
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
    fontprops = mpl.font_manager.FontProperties(family="Arial", size=8)
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
    # For the bottom row (6 columns), use its own widths, but make each cell half the width of the cells above
    # Calculate the average width of the top row columns
    avg_top_col_width = sum(top_col_widths_px) / 3
    # Each bottom cell is half the width of a top cell
    bottom_col_widths_px = [avg_top_col_width / 2] * 6
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
                    fontsize=8,
                    fontweight="bold",
                    fontname="Arial",
                )

            # Value (normal, lower part of cell)
            if value:
                ax.text(
                    x_pos + col_width * 0.05,
                    y_pos - top_row_height * 0.6,
                    value,
                    va="top",
                    ha="left",
                    fontsize=8,
                    fontname="Arial",
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
            fontsize=8,
            fontweight="bold",
            fontname="Arial",
        )
        # Draw value (centered horizontally, lower in cell)
        ax.text(
            x + col_width / 2,
            0.2 + bottom_row_height * 0.35,
            bottom_values[i],
            va="top",
            ha="center",
            fontsize=8,
            fontname="Arial",
        )
        x += col_width

    # Draw new additional row at the bottom
    new_row_height = 0.2  # fraction of axes height for new row

    # Define column widths for the new row (adjusted for better text fitting)
    # Increased proportions to accommodate longer text while maintaining relationships
    new_col_widths = [0.05, 0.10, 0.06, 0.12, 0.08, 0.08, 0.10, 0.37, 0.04]
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
                fontsize=8,
                fontweight="bold",
                fontname="Arial",
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
                fontsize=7,
                fontweight="bold",
                fontname="Arial",
            )
        elif label:  # Other column labels
            ax.text(
                x + col_width / 2,
                new_row_height / 2,
                label,
                va="center",
                ha="center",
                fontsize=8,
                fontweight="bold",
                fontname="Arial",
            )

        x += col_width


def plot_dummy_borehole_log():
    # --- MULTI-PAGE LOG IMPLEMENTATION ---
    # A4 width is 8.27 inches, minus margins (0.5" each side) = 7.27" usable
    a4_width_in = 8.27
    a4_height_in = 11.69
    a4_usable_width = a4_width_in - 0.5 * 2  # 0.5" left/right margins
    # Define all vertical elements in inches
    top_margin_in = 0.3
    header_height_in = 2.0
    bottom_margin_in = 0.3
    # Log area is the rest of the page
    log_area_in = a4_height_in - (top_margin_in + header_height_in + bottom_margin_in)
    # Determine the maximum depth and number of pages
    log_depth = float(DUMMY_BOREHOLE_DATA["Depth_Base"].max())
    last_borehole_page = int(np.ceil(log_depth / 10.0))

    for page_num in range(1, last_borehole_page + 1):
        page_top = (page_num - 1) * 10
        page_bot = page_num * 10
        # Always use full A4 page size for every page
        fig_width_in = a4_usable_width
        fig_height_in = a4_height_in
        # Horizontal margins as fraction of width
        margin_frac = 0.5 / a4_width_in
        axes_left = margin_frac
        axes_width = 1 - 2 * margin_frac
        # Vertical positions as fraction of height
        top_margin_frac = top_margin_in / a4_height_in
        header_height_frac = header_height_in / a4_height_in
        log_height_frac = log_area_in / a4_height_in
        bottom_margin_frac = bottom_margin_in / a4_height_in
        fig = plt.figure(figsize=(fig_width_in, fig_height_in))
        # Header axes: start below top margin
        header_ax = fig.add_axes(
            [
                axes_left,
                1 - top_margin_frac - header_height_frac,
                axes_width,
                header_height_frac,
            ]
        )
        draw_header(header_ax)
        header_ax.set_xlim(0, 1)
        header_ax.set_ylim(0, 1)
        header_ax.axis("off")
        # Log axes: start below header, above bottom margin
        log_ax = fig.add_axes(
            [
                axes_left,
                bottom_margin_frac,
                axes_width,
                log_height_frac,
            ]
        )
        from matplotlib.patches import Rectangle as MplRectangle

        log_ax.add_patch(
            MplRectangle(
                (0, 0), 1, 1, fill=False, edgecolor="black", linewidth=1, zorder=10
            )
        )
        log_ax.set_xlim(0, 1)
        log_ax.set_ylim(0, 1)
        log_ax.axis("off")

        # Column setup
        log_col_widths = [0.05, 0.10, 0.06, 0.12, 0.08, 0.08, 0.10, 0.37, 0.04]
        log_col_x = [0]
        for w in log_col_widths:
            log_col_x.append(log_col_x[-1] + w)
        for idx, x_val in enumerate(log_col_x[1:-1], start=1):
            log_ax.plot([x_val, x_val], [0, 1], color="black", linewidth=1, zorder=20)
        log_ax.plot([0, 1], [1, 1], color="black", linewidth=1, zorder=20)

        legend_left = log_col_x[6]
        legend_width = log_col_widths[6]
        desc_left = log_col_x[7]
        desc_width = log_col_widths[7]
        bottom_line_y = 0.025

        def depth_to_y(depth):
            # Map depth to y coordinate based on fixed 10m page scale
            # The page always represents exactly 10m of depth (0-10, 10-20, etc.)
            page_depth_range = 10.0  # Always 10m per page regardless of borehole length
            return 1 - (1 - bottom_line_y) * ((depth - page_top) / page_depth_range)

        ground_level = 62.5  # Top of borehole (Level AoD)

        # Find all intervals that overlap this page, splitting if needed
        intervals = []
        for i, row in DUMMY_BOREHOLE_DATA.iterrows():
            d1 = row["Depth_Top"]
            d2 = row["Depth_Base"]
            # If the interval is entirely above or below this page, skip
            if d2 <= page_top or d1 >= page_bot:
                continue
            # Clamp to page boundaries
            seg_top = max(d1, page_top)
            seg_base = min(d2, page_bot)
            intervals.append(
                {
                    "orig_idx": i,
                    "Depth_Top": seg_top,
                    "Depth_Base": seg_base,
                    "Geology_Code": row["Geology_Code"],
                    "Description": row["Description"],
                    "orig_Depth_Top": d1,
                    "orig_Depth_Base": d2,
                }
            )

        # Draw each interval
        for j, seg in enumerate(intervals):
            y_top = depth_to_y(seg["Depth_Top"])
            y_base = depth_to_y(seg["Depth_Base"])
            # Clip the lithology/description bars at the horizontal line if borehole ends before page bottom
            borehole_end_depth = min(log_depth, page_top + 10)
            borehole_end_y = depth_to_y(borehole_end_depth)
            # Only draw down to the lesser of y_base and borehole_end_y
            y_base_clipped = max(y_base, borehole_end_y)
            # Only draw if the clipped bar has positive height
            if y_top > y_base_clipped:
                log_ax.add_patch(
                    MplRectangle(
                        (legend_left, y_base_clipped),
                        legend_width,
                        y_top - y_base_clipped,
                        facecolor="#b0c4de",
                        edgecolor="black",
                        linewidth=1,
                        zorder=2,
                    )
                )
                # Draw geology code and description at the center of the visible bar
                y_center = (y_top + y_base_clipped) / 2
                log_ax.text(
                    legend_left + legend_width / 2,
                    y_center,
                    f"{seg['Geology_Code']}",
                    va="center",
                    ha="center",
                    fontsize=8,
                    color="black",
                    fontweight="bold",
                    fontname="Arial",
                    zorder=3,
                )
                log_ax.text(
                    desc_left + desc_width * 0.02,
                    y_center,
                    seg["Description"],
                    va="center",
                    ha="left",
                    fontsize=8,
                    color="black",
                    fontname="Arial",
                    zorder=3,
                    wrap=True,
                )
            # Depth and level columns (index 4 and 5)
            depth_left = log_col_x[4]
            depth_width = log_col_widths[4]
            level_left = log_col_x[5]
            level_width = log_col_widths[5]
            # Show top value only if it's the actual start of the stratum (not a page split)
            show_top = abs(seg["Depth_Top"] - seg["orig_Depth_Top"]) < 1e-6
            if show_top and seg["Depth_Top"] > 0:
                log_ax.text(
                    depth_left + depth_width / 2,
                    y_top,
                    f"{seg['Depth_Top']:.2f}",
                    va="bottom",
                    ha="center",
                    fontsize=8,
                    color="black",
                    fontname="Arial",
                    zorder=3,
                )
                log_ax.text(
                    level_left + level_width / 2,
                    y_top,
                    f"{ground_level - seg['Depth_Top']:.2f}",
                    va="bottom",
                    ha="center",
                    fontsize=8,
                    color="black",
                    fontname="Arial",
                    zorder=3,
                )
            # Show base value only if it's the actual end of the stratum (not a page split)
            show_base = abs(seg["Depth_Base"] - seg["orig_Depth_Base"]) < 1e-6
            if show_base:
                base_va = "top"
                base_y = y_base
                # If this is the actual end of the borehole (not just the end of a stratum),
                # align the value with the end of the borehole, not the page bottom.
                is_borehole_end = abs(seg["Depth_Base"] - log_depth) < 1e-6
                if is_borehole_end:
                    # Place at the actual end of the borehole
                    base_va = "top"
                    base_y = y_base
                log_ax.text(
                    depth_left + depth_width / 2,
                    base_y,
                    f"{seg['Depth_Base']:.2f}",
                    va=base_va,
                    ha="center",
                    fontsize=8,
                    color="black",
                    fontname="Arial",
                    zorder=3,
                )
                log_ax.text(
                    level_left + level_width / 2,
                    base_y,
                    f"{ground_level - seg['Depth_Base']:.2f}",
                    va=base_va,
                    ha="center",
                    fontsize=8,
                    color="black",
                    fontname="Arial",
                    zorder=3,
                )
            # Draw horizontal divider if not at page top
            if j > 0:
                log_ax.plot(
                    [legend_left, desc_left + desc_width],
                    [y_top, y_top],
                    color="black",
                    linewidth=1,
                    zorder=15,
                )

        # --- Add horizontal line at bottom of log if borehole ends before page bottom ---
        borehole_end_depth = min(
            log_depth, page_top + 10
        )  # End of borehole on this page
        if borehole_end_depth < page_top + 10:  # Borehole ends before page bottom
            borehole_end_y = depth_to_y(borehole_end_depth)
            log_ax.plot(
                [legend_left, desc_left + desc_width],
                [borehole_end_y, borehole_end_y],
                color="black",
                linewidth=1,
                zorder=16,
            )
        else:
            # --- Add horizontal line just above the bottom through legend and description columns ---
            log_ax.plot(
                [legend_left, desc_left + desc_width],
                [bottom_line_y, bottom_line_y],
                color="black",
                linewidth=1,
                zorder=16,
            )

        # --- Add ruler axis with 10m markers (0-10, 10-20, etc.) in the rightmost column, always full height ---
        ruler_left = log_col_x[8]
        ruler_width = log_col_widths[8]
        ruler_x = ruler_left
        log_ax.plot([ruler_x, ruler_x], [0, 1], color="black", linewidth=1.2, zorder=30)
        main_tick_length = ruler_width * 0.5
        sub_tick_length = ruler_width * 0.25

        # Determine the marker range for this page (always 0-10, 10-20, ... for the plot area)
        marker_start = (page_num - 1) * 10
        marker_end = page_num * 10

        # Draw main markers and labels (always 0-10, 10-20, etc. for the page)
        for marker in range(marker_start, marker_end + 1):
            y_marker = 1 - (1 - bottom_line_y) * ((marker - marker_start) / 10)
            log_ax.plot(
                [ruler_x, ruler_x + main_tick_length],
                [y_marker, y_marker],
                color="black",
                linewidth=1.1,
                zorder=31,
            )
            log_ax.text(
                ruler_x + main_tick_length + ruler_width * 0.1,
                y_marker,
                f"{marker}",
                va="center",
                ha="left",
                fontsize=8,
                color="black",
                fontname="Arial",
                zorder=32,
            )

        # Decimal subticks (0.1 to 0.9 between each main marker)
        for i in range(10):
            for sub in range(1, 10):
                y_subtick = 1 - (1 - bottom_line_y) * ((i + sub / 10) / 10)
                log_ax.plot(
                    [ruler_x, ruler_x + sub_tick_length],
                    [y_subtick, y_subtick],
                    color="black",
                    linewidth=0.7,
                    zorder=30,
                )

        # Save as A4-sized PNG image with 300 DPI (always full page)
        fig.savefig(
            f"borehole_log_output_page{page_num}.png", dpi=300, bbox_inches=None
        )
        plt.close(fig)


if __name__ == "__main__":
    plot_dummy_borehole_log()
