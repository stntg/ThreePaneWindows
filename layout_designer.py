"""
GUI Layout Designer for DynamicDockableGrid

A visual tool to design pane layouts with precise expansion control.
"""

import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Any, Dict, List, Optional

from threepanewindows.dynamic import DynamicDockableGrid
from threepanewindows.enhanced_dockable import PaneConfig


class PaneCell:
    """Represents a single pane cell in the designer."""

    def __init__(self, name: str = "", row: int = 0, col: int = 0):
        self.name = name
        self.row = row
        self.col = col

        # Expansion properties
        self.expand_up = 0  # How many rows up it can expand
        self.expand_down = 0  # How many rows down it can expand
        self.expand_left = 0  # How many cols left it can expand
        self.expand_right = 0  # How many cols right it can expand

        # Initial span
        self.initial_rowspan = 1
        self.initial_colspan = 1

        # Detached space filling
        self.fill_detached_space = False
        self.expansion_priority = 0
        self.max_rowspan = None
        self.max_colspan = None

        # Visual properties
        self.color = "#4a90e2"
        self.icon = "📄"
        self.detachable = True


class LayoutDesigner:
    """Main layout designer application."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DynamicDockableGrid Layout Designer")
        self.root.geometry("1400x900")

        # Layout properties
        self.rows = 3
        self.cols = 3
        self.cells: Dict[tuple, PaneCell] = {}
        self.selected_cell = None

        # UI components
        self.grid_frame = None
        self.cell_buttons = {}
        self.preview_window = None

        self.setup_ui()
        self.create_initial_layout()

    def setup_ui(self):
        """Setup the main UI."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left panel - Grid designer
        left_frame = ttk.LabelFrame(main_frame, text="Layout Designer", padding=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Grid size controls
        size_frame = ttk.Frame(left_frame)
        size_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(size_frame, text="Grid Size:").pack(side="left")

        ttk.Label(size_frame, text="Rows:").pack(side="left", padx=(10, 0))
        self.rows_var = tk.StringVar(value=str(self.rows))
        rows_spin = ttk.Spinbox(
            size_frame,
            from_=1,
            to=10,
            width=5,
            textvariable=self.rows_var,
            command=self.update_grid_size,
        )
        rows_spin.pack(side="left", padx=(5, 10))

        ttk.Label(size_frame, text="Cols:").pack(side="left")
        self.cols_var = tk.StringVar(value=str(self.cols))
        cols_spin = ttk.Spinbox(
            size_frame,
            from_=1,
            to=10,
            width=5,
            textvariable=self.cols_var,
            command=self.update_grid_size,
        )
        cols_spin.pack(side="left", padx=(5, 10))

        # Action buttons
        action_frame = ttk.Frame(size_frame)
        action_frame.pack(side="right")

        ttk.Button(
            action_frame, text="Preview Layout", command=self.preview_layout
        ).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Export Config", command=self.export_config).pack(
            side="left", padx=5
        )
        ttk.Button(action_frame, text="Import Config", command=self.import_config).pack(
            side="left", padx=5
        )

        # Grid container
        self.grid_container = ttk.Frame(left_frame)
        self.grid_container.pack(fill="both", expand=True)

        # Right panel - Cell properties
        right_frame = ttk.LabelFrame(main_frame, text="Cell Properties", padding=10)
        right_frame.pack(side="right", fill="y", ipadx=20)

        self.setup_properties_panel(right_frame)

    def setup_properties_panel(self, parent):
        """Setup the cell properties panel."""
        # Cell info
        info_frame = ttk.LabelFrame(parent, text="Cell Info", padding=5)
        info_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(info_frame, text="Name:").grid(
            row=0, column=0, sticky="w", padx=(0, 5)
        )
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(info_frame, textvariable=self.name_var, width=15)
        self.name_entry.grid(row=0, column=1, sticky="ew")
        self.name_var.trace("w", self.update_selected_cell)

        ttk.Label(info_frame, text="Icon:").grid(
            row=1, column=0, sticky="w", padx=(0, 5)
        )
        self.icon_var = tk.StringVar(value="📄")
        self.icon_entry = ttk.Entry(info_frame, textvariable=self.icon_var, width=15)
        self.icon_entry.grid(row=1, column=1, sticky="ew")
        self.icon_var.trace("w", self.update_selected_cell)

        ttk.Label(info_frame, text="Color:").grid(
            row=2, column=0, sticky="w", padx=(0, 5)
        )
        self.color_var = tk.StringVar(value="#4a90e2")
        self.color_entry = ttk.Entry(info_frame, textvariable=self.color_var, width=15)
        self.color_entry.grid(row=2, column=1, sticky="ew")
        self.color_var.trace("w", self.update_selected_cell)

        info_frame.columnconfigure(1, weight=1)

        # Initial span
        span_frame = ttk.LabelFrame(parent, text="Initial Span", padding=5)
        span_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(span_frame, text="Rowspan:").grid(row=0, column=0, sticky="w")
        self.rowspan_var = tk.StringVar(value="1")
        ttk.Spinbox(
            span_frame,
            from_=1,
            to=10,
            width=8,
            textvariable=self.rowspan_var,
            command=self.update_selected_cell,
        ).grid(row=0, column=1, sticky="ew")

        ttk.Label(span_frame, text="Colspan:").grid(row=1, column=0, sticky="w")
        self.colspan_var = tk.StringVar(value="1")
        ttk.Spinbox(
            span_frame,
            from_=1,
            to=10,
            width=8,
            textvariable=self.colspan_var,
            command=self.update_selected_cell,
        ).grid(row=1, column=1, sticky="ew")

        span_frame.columnconfigure(1, weight=1)

        # Expansion limits
        expansion_frame = ttk.LabelFrame(parent, text="Expansion Limits", padding=5)
        expansion_frame.pack(fill="x", pady=(0, 10))

        directions = [
            ("Up", "expand_up"),
            ("Down", "expand_down"),
            ("Left", "expand_left"),
            ("Right", "expand_right"),
        ]

        self.expansion_vars = {}
        for i, (label, attr) in enumerate(directions):
            ttk.Label(expansion_frame, text=f"{label}:").grid(
                row=i, column=0, sticky="w"
            )
            var = tk.StringVar(value="0")
            self.expansion_vars[attr] = var
            ttk.Spinbox(
                expansion_frame,
                from_=0,
                to=10,
                width=8,
                textvariable=var,
                command=self.update_selected_cell,
            ).grid(row=i, column=1, sticky="ew")

        expansion_frame.columnconfigure(1, weight=1)

        # Detached space filling
        detached_frame = ttk.LabelFrame(
            parent, text="Detached Space Filling", padding=5
        )
        detached_frame.pack(fill="x", pady=(0, 10))

        self.fill_detached_var = tk.BooleanVar()
        ttk.Checkbutton(
            detached_frame,
            text="Fill detached space",
            variable=self.fill_detached_var,
            command=self.update_selected_cell,
        ).pack(anchor="w")

        ttk.Label(detached_frame, text="Priority:").pack(anchor="w")
        self.priority_var = tk.StringVar(value="0")
        ttk.Spinbox(
            detached_frame,
            from_=0,
            to=10,
            width=8,
            textvariable=self.priority_var,
            command=self.update_selected_cell,
        ).pack(fill="x")

        # Max span limits
        limits_frame = ttk.LabelFrame(parent, text="Maximum Span Limits", padding=5)
        limits_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(limits_frame, text="Max Rowspan:").grid(row=0, column=0, sticky="w")
        self.max_rowspan_var = tk.StringVar(value="")
        ttk.Entry(limits_frame, textvariable=self.max_rowspan_var, width=8).grid(
            row=0, column=1, sticky="ew"
        )
        self.max_rowspan_var.trace("w", self.update_selected_cell)

        ttk.Label(limits_frame, text="Max Colspan:").grid(row=1, column=0, sticky="w")
        self.max_colspan_var = tk.StringVar(value="")
        ttk.Entry(limits_frame, textvariable=self.max_colspan_var, width=8).grid(
            row=1, column=1, sticky="ew"
        )
        self.max_colspan_var.trace("w", self.update_selected_cell)

        limits_frame.columnconfigure(1, weight=1)

        # Other properties
        other_frame = ttk.LabelFrame(parent, text="Other Properties", padding=5)
        other_frame.pack(fill="x", pady=(0, 10))

        self.detachable_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            other_frame,
            text="Detachable",
            variable=self.detachable_var,
            command=self.update_selected_cell,
        ).pack(anchor="w")

        # Instructions
        instructions = ttk.Label(
            parent,
            text="Instructions:\n\n"
            "1. Click cells to select them\n"
            "2. Set cell properties on the right\n"
            "3. Expansion limits control how far\n"
            "   a pane can expand in each direction\n"
            "4. Use 'Preview Layout' to test\n"
            "5. Export config when done",
            justify="left",
            font=("Segoe UI", 8),
        )
        instructions.pack(side="bottom", fill="x", pady=(20, 0))

    def create_initial_layout(self):
        """Create the initial grid layout."""
        self.update_grid_display()

        # Create some default panes
        default_panes = [
            ("left1", 0, 0, "📑", "#2a2a2a"),
            ("center", 0, 1, "🖥️", "#1a1a40"),
            ("right1", 0, 2, "⚙️", "#403a1a"),
            ("left2", 1, 0, "📂", "#3a3a3a"),
            ("right2", 1, 2, "🔧", "#504a1a"),
            ("left3", 2, 0, "🗄️", "#4a4a4a"),
        ]

        for name, row, col, icon, color in default_panes:
            if (row, col) not in self.cells:
                cell = PaneCell(name, row, col)
                cell.icon = icon
                cell.color = color
                # Set some default expansion properties
                if "left" in name:
                    cell.expand_right = 2  # Can expand 2 columns right
                    cell.fill_detached_space = True
                elif "right" in name:
                    cell.expand_left = 2  # Can expand 2 columns left
                    cell.fill_detached_space = True
                elif name == "center":
                    cell.initial_rowspan = 3  # Spans 3 rows initially
                    cell.expand_left = 1
                    cell.expand_right = 1
                    cell.fill_detached_space = True

                self.cells[(row, col)] = cell

        self.update_grid_display()

    def update_grid_size(self):
        """Update grid size when spinbox values change."""
        try:
            new_rows = int(self.rows_var.get())
            new_cols = int(self.cols_var.get())

            if new_rows != self.rows or new_cols != self.cols:
                self.rows = new_rows
                self.cols = new_cols
                self.update_grid_display()
        except ValueError:
            pass

    def update_grid_display(self):
        """Update the visual grid display."""
        # Clear existing grid
        if self.grid_frame:
            self.grid_frame.destroy()

        self.grid_frame = ttk.Frame(self.grid_container)
        self.grid_frame.pack(fill="both", expand=True)

        self.cell_buttons = {}

        # Create grid buttons
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.cells.get((row, col))

                if cell and cell.name:
                    text = f"{cell.icon}\n{cell.name}"
                    bg_color = cell.color
                    fg_color = "white"
                else:
                    text = f"({row},{col})\nEmpty"
                    bg_color = "#f0f0f0"
                    fg_color = "black"

                btn = tk.Button(
                    self.grid_frame,
                    text=text,
                    bg=bg_color,
                    fg=fg_color,
                    font=("Segoe UI", 9, "bold"),
                    width=12,
                    height=4,
                    command=lambda r=row, c=col: self.select_cell(r, c),
                )
                btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
                self.cell_buttons[(row, col)] = btn

        # Configure grid weights
        for row in range(self.rows):
            self.grid_frame.grid_rowconfigure(row, weight=1)
        for col in range(self.cols):
            self.grid_frame.grid_columnconfigure(col, weight=1)

    def select_cell(self, row: int, col: int):
        """Select a cell and update properties panel."""
        self.selected_cell = (row, col)

        # Update button appearance
        for (r, c), btn in self.cell_buttons.items():
            if (r, c) == (row, col):
                btn.configure(relief="sunken", bd=3)
            else:
                btn.configure(relief="raised", bd=1)

        # Get or create cell
        if (row, col) not in self.cells:
            self.cells[(row, col)] = PaneCell(f"pane_{row}_{col}", row, col)

        cell = self.cells[(row, col)]

        # Update properties panel
        self.name_var.set(cell.name)
        self.icon_var.set(cell.icon)
        self.color_var.set(cell.color)
        self.rowspan_var.set(str(cell.initial_rowspan))
        self.colspan_var.set(str(cell.initial_colspan))

        self.expansion_vars["expand_up"].set(str(cell.expand_up))
        self.expansion_vars["expand_down"].set(str(cell.expand_down))
        self.expansion_vars["expand_left"].set(str(cell.expand_left))
        self.expansion_vars["expand_right"].set(str(cell.expand_right))

        self.fill_detached_var.set(cell.fill_detached_space)
        self.priority_var.set(str(cell.expansion_priority))

        self.max_rowspan_var.set(str(cell.max_rowspan) if cell.max_rowspan else "")
        self.max_colspan_var.set(str(cell.max_colspan) if cell.max_colspan else "")

        self.detachable_var.set(cell.detachable)

    def update_selected_cell(self, *args):
        """Update the selected cell with current property values."""
        if not self.selected_cell:
            return

        cell = self.cells.get(self.selected_cell)
        if not cell:
            return

        try:
            cell.name = self.name_var.get()
            cell.icon = self.icon_var.get()
            cell.color = self.color_var.get()
            cell.initial_rowspan = int(self.rowspan_var.get())
            cell.initial_colspan = int(self.colspan_var.get())

            cell.expand_up = int(self.expansion_vars["expand_up"].get())
            cell.expand_down = int(self.expansion_vars["expand_down"].get())
            cell.expand_left = int(self.expansion_vars["expand_left"].get())
            cell.expand_right = int(self.expansion_vars["expand_right"].get())

            cell.fill_detached_space = self.fill_detached_var.get()
            cell.expansion_priority = int(self.priority_var.get())

            max_rowspan_str = self.max_rowspan_var.get().strip()
            cell.max_rowspan = int(max_rowspan_str) if max_rowspan_str else None

            max_colspan_str = self.max_colspan_var.get().strip()
            cell.max_colspan = int(max_colspan_str) if max_colspan_str else None

            cell.detachable = self.detachable_var.get()

            # Update grid display
            self.update_grid_display()
            if self.selected_cell:
                self.select_cell(*self.selected_cell)

        except ValueError:
            pass  # Ignore invalid values during typing

    def preview_layout(self):
        """Preview the layout in a separate window."""
        if self.preview_window:
            self.preview_window.destroy()

        self.preview_window = tk.Toplevel(self.root)
        self.preview_window.title("Layout Preview")
        self.preview_window.geometry("800x600")

        try:
            # Generate layout configuration
            panes, builders, layout_grid = self.generate_layout_config()

            # Create the grid
            grid = DynamicDockableGrid(
                master=self.preview_window,
                panes=panes,
                builders=builders,
                layout_grid=layout_grid,
                theme="light",
                show_toolbar=True,
                show_status_bar=True,
            )
            grid.pack(fill="both", expand=True)

            # Print spans for debugging
            spans = grid._calculate_spans()
            print("\n=== PREVIEW LAYOUT SPANS ===")
            for pane_name, (row, col, rowspan, colspan) in spans.items():
                print(
                    f"  {pane_name}: row={row}, col={col}, rowspan={rowspan}, colspan={colspan}"
                )

        except Exception as e:
            messagebox.showerror("Preview Error", f"Error creating preview:\n{str(e)}")

    def generate_layout_config(self):
        """Generate the configuration for DynamicDockableGrid."""
        panes = {}
        builders = {}
        layout_grid = []

        # Create layout grid
        for row in range(self.rows):
            layout_row = []
            for col in range(self.cols):
                cell = self.cells.get((row, col))
                if cell and cell.name:
                    layout_row.append(cell.name)
                else:
                    layout_row.append(None)
            layout_grid.append(layout_row)

        # Create pane configs and builders
        for (row, col), cell in self.cells.items():
            if not cell.name:
                continue

            # Create PaneConfig
            panes[cell.name] = PaneConfig(
                title=cell.name,
                icon=cell.icon,
                detachable=cell.detachable,
                expand_vertical=(cell.initial_rowspan > 1),
                expand_horizontal=(cell.initial_colspan > 1),
                fill_detached_space=cell.fill_detached_space,
                expand_left=(cell.expand_left > 0),
                expand_right=(cell.expand_right > 0),
                expand_up=(cell.expand_up > 0),
                expand_down=(cell.expand_down > 0),
                max_rowspan=cell.max_rowspan,
                max_colspan=cell.max_colspan,
                expansion_priority=cell.expansion_priority,
            )

            # Create builder
            def make_builder(name, color):
                def builder(parent):
                    lbl = tk.Label(
                        parent,
                        text=f"{name}\n\nExpansion:\n"
                        f"↑{cell.expand_up} ↓{cell.expand_down}\n"
                        f"←{cell.expand_left} →{cell.expand_right}",
                        bg=color,
                        fg="white",
                        font=("Segoe UI", 10, "bold"),
                        justify="center",
                    )
                    lbl.pack(fill="both", expand=True)
                    parent.configure(relief="solid", bd=2)

                return builder

            builders[cell.name] = make_builder(cell.name, cell.color)

        return panes, builders, layout_grid

    def export_config(self):
        """Export the layout configuration to a JSON file."""
        try:
            config = {"grid_size": {"rows": self.rows, "cols": self.cols}, "cells": {}}

            for (row, col), cell in self.cells.items():
                if cell.name:
                    config["cells"][f"{row},{col}"] = {
                        "name": cell.name,
                        "icon": cell.icon,
                        "color": cell.color,
                        "initial_rowspan": cell.initial_rowspan,
                        "initial_colspan": cell.initial_colspan,
                        "expand_up": cell.expand_up,
                        "expand_down": cell.expand_down,
                        "expand_left": cell.expand_left,
                        "expand_right": cell.expand_right,
                        "fill_detached_space": cell.fill_detached_space,
                        "expansion_priority": cell.expansion_priority,
                        "max_rowspan": cell.max_rowspan,
                        "max_colspan": cell.max_colspan,
                        "detachable": cell.detachable,
                    }

            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            )

            if filename:
                with open(filename, "w") as f:
                    json.dump(config, f, indent=2)
                messagebox.showinfo(
                    "Export Success", f"Configuration exported to {filename}"
                )

        except Exception as e:
            messagebox.showerror(
                "Export Error", f"Error exporting configuration:\n{str(e)}"
            )

    def import_config(self):
        """Import a layout configuration from a JSON file."""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )

            if not filename:
                return

            with open(filename, "r") as f:
                config = json.load(f)

            # Update grid size
            grid_size = config.get("grid_size", {})
            self.rows = grid_size.get("rows", 3)
            self.cols = grid_size.get("cols", 3)
            self.rows_var.set(str(self.rows))
            self.cols_var.set(str(self.cols))

            # Clear existing cells
            self.cells.clear()

            # Load cells
            for pos_str, cell_data in config.get("cells", {}).items():
                row, col = map(int, pos_str.split(","))
                cell = PaneCell(cell_data["name"], row, col)

                cell.icon = cell_data.get("icon", "📄")
                cell.color = cell_data.get("color", "#4a90e2")
                cell.initial_rowspan = cell_data.get("initial_rowspan", 1)
                cell.initial_colspan = cell_data.get("initial_colspan", 1)
                cell.expand_up = cell_data.get("expand_up", 0)
                cell.expand_down = cell_data.get("expand_down", 0)
                cell.expand_left = cell_data.get("expand_left", 0)
                cell.expand_right = cell_data.get("expand_right", 0)
                cell.fill_detached_space = cell_data.get("fill_detached_space", False)
                cell.expansion_priority = cell_data.get("expansion_priority", 0)
                cell.max_rowspan = cell_data.get("max_rowspan")
                cell.max_colspan = cell_data.get("max_colspan")
                cell.detachable = cell_data.get("detachable", True)

                self.cells[(row, col)] = cell

            self.update_grid_display()
            messagebox.showinfo(
                "Import Success", f"Configuration imported from {filename}"
            )

        except Exception as e:
            messagebox.showerror(
                "Import Error", f"Error importing configuration:\n{str(e)}"
            )

    def run(self):
        """Run the designer application."""
        self.root.mainloop()


if __name__ == "__main__":
    designer = LayoutDesigner()
    designer.run()
