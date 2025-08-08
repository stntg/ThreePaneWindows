# Dynamic Pane Expansion Features

## Overview

The `DynamicDockableGrid` now supports sophisticated pane expansion preferences that control how panes behave when other panes are detached. This provides maximum flexibility for creating adaptive layouts.

## New PaneConfig Properties

### `expand_vertical: bool = True`
- Controls whether a pane can expand vertically into originally `None` cells
- When `True`, the pane will span multiple rows if there are `None` cells below it
- When `False`, the pane stays in its original row only

### `expand_horizontal: bool = False`
- Controls whether a pane can expand horizontally into originally `None` cells
- When `True`, the pane will span multiple columns if there are `None` cells to the right
- When `False`, the pane stays in its original column only

### `fill_detached_space: bool = False`
- Controls whether a pane should expand to fill space left by detached panes
- When `True`, the pane will dynamically expand when adjacent panes are detached
- When `False`, the pane ignores detached space and maintains its original size

## How It Works

### 1. Basic Span Calculation
- Panes first calculate their spans based on `expand_vertical` and `expand_horizontal`
- Only expands into cells that were originally `None` in the layout
- Does not expand into space occupied by detached panes during this phase

### 2. Detached Space Filling
- After basic spans are calculated, the algorithm handles detached space filling
- For each detached pane, calculates what its original span would have been
- Tries to expand adjacent panes with `fill_detached_space=True` into that space
- Expansion priority: left → up → right → down

### 3. Dynamic Recalculation
- When panes are detached or reattached, the layout is automatically recalculated
- All attached panes are repositioned with updated spans
- Space is efficiently filled by appropriate adjacent panes

## Example Configurations

### Sidebar Panes (Left Column)
```python
PaneConfig(
    title="Sidebar",
    expand_vertical=False,      # Don't expand into None cells
    expand_horizontal=False,    # Stay in original column
    fill_detached_space=True    # Expand when adjacent panes detach
)
```

### Main Content Pane (Center)
```python
PaneConfig(
    title="Main View",
    expand_vertical=True,       # Expand down into None cells
    expand_horizontal=False,    # Don't expand horizontally
    fill_detached_space=False   # Don't fill detached space
)
```

### Tool Panes (Right Column)
```python
PaneConfig(
    title="Tools",
    expand_vertical=True,       # Expand down into None cells
    expand_horizontal=False,    # Stay in original column
    fill_detached_space=True    # Expand when adjacent panes detach
)
```

## Layout Example

Original layout:
```
["left1",  "center", "right1"]
["left2",     None,  "right2"]
["left3",     None,     None]
```

Initial spans (with expansion preferences):
- `left1`: (0,0,1,1) - no expansion
- `left2`: (1,0,1,1) - no expansion
- `left3`: (2,0,1,1) - no expansion
- `center`: (0,1,3,1) - expands vertically into None cells
- `right1`: (0,2,1,1) - no expansion
- `right2`: (1,2,2,1) - expands vertically into None cell

After detaching center pane:
- `left1`: (0,0,1,2) - fills detached space horizontally
- `left2`: (1,0,1,2) - fills detached space horizontally
- `left3`: (2,0,1,2) - fills detached space horizontally
- `right1`: (0,2,1,1) - unchanged
- `right2`: (1,2,2,1) - unchanged

## Benefits

1. **Flexible Layout Control**: Each pane can have different expansion behaviors
2. **Dynamic Space Utilization**: Detached space is automatically filled by appropriate panes
3. **Predictable Behavior**: Clear rules for how panes expand and fill space
4. **Backward Compatible**: Default values maintain existing behavior
5. **Real-time Updates**: Layout recalculates automatically on detach/reattach

## Testing

Run the demo files to see the expansion features in action:

- `pane_layout2.py` - Main demo with expansion preferences
- `test_expansion_preferences.py` - Detailed test with visual indicators
- `debug_detached.py` - Debug output showing span calculations

Try detaching different panes to see how the remaining panes expand to fill the space!
