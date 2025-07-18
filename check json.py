import json

with open("rich_layout_tables.json", "r") as f:
    data = json.load(f)

# 1. Check top-level structure
if not isinstance(data, list) or not data:
    print("JSON is not a list or is empty.")
else:
    print(f"Number of tables: {len(data)}")

    for t_idx, table in enumerate(data):
        rows = table.get("rows", [])
        print(f"Table {t_idx}: {len(rows)} rows")
        for r_idx, row in enumerate(rows[:3]):  # Show only first 3 rows for brevity
            print(f"  Row {r_idx}: {len(row)} cells")
            for c_idx, cell in enumerate(row[:3]):  # Show only first 3 cells
                width = cell.get("width")
                grid_span = cell.get("gridSpan")
                content = cell.get("content", [])
                # Try to get first text
                text = ""
                for para in content:
                    for run in para:
                        if "text" in run:
                            text = run["text"]
                            break
                    if text:
                        break
                print(
                    f"    Cell {c_idx}: width={width}, gridSpan={grid_span}, text='{text}'"
                )
        print("-" * 40)
