import tkinter as tk

GRID_SIZE = 37  # 37x37 grid
BUTTON_SIZE = 2  # Button grid size

# Split categories into two columns
COLUMN_1 = ['P', 'B', 'D']
COLUMN_2 = ['R', 'Q', 'E', 'Y']
NUM_BUTTONS = 5  # Each category has 5 buttons (e.g., P1..P5)

def toggle_color(btn):
    """Toggle button color between grey and green."""
    current_color = btn.cget("bg")
    btn.config(bg="green" if current_color == "grey" else "grey")

def update_counter(label, delta):
    """Increment or decrement the counter value."""
    value = int(label.cget("text"))
    value = max(0, value + delta)  # Prevent negative values
    label.config(text=str(value))

def on_button_click(event, label):
    """Handle left/right click events on increment buttons."""
    if event.num == 1:  # Left click
        update_counter(label, +1)
    elif event.num == 3:  # Right click
        update_counter(label, -1)

# Main window
root = tk.Tk()
root.title("Grid with Counters")

# Create main container
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Left frame for 37x37 grid
grid_frame = tk.Frame(main_frame)
grid_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Create grid of buttons
buttons = []
for row in range(GRID_SIZE):
    row_buttons = []
    for col in range(GRID_SIZE):
        if (row < 9 and col < 9) or (row > 27 and col > 27):
              btn = tk.Button(
                grid_frame,
                width=BUTTON_SIZE,
                height=1,
                bg="black"
            )
        elif (row == 18 and (col == 4 or col == 32)) or (col == 18 and (row == 4 or row == 32)) or (row == 4 and col == 32):
             btn = tk.Button(
                grid_frame,
                width=BUTTON_SIZE,
                height=1,
                bg="red"
            )
        elif (col == 18 and row == 18):
                btn = tk.Button(
                grid_frame,
                width=BUTTON_SIZE,
                height=1,
                bg="yellow"
            )
        elif (row == 18 and (col > 4 and col < 33)):
                 btn = tk.Button(
                grid_frame,
                width=BUTTON_SIZE,
                height=1,
                bg="blue"
            )
        elif (col == 18 and (row > 4 and row < 33)):
                 btn = tk.Button(
                grid_frame,
                width=BUTTON_SIZE,
                height=1,
                bg="blue"
            )
        else: 
            btn = tk.Button(
                grid_frame,
                width=BUTTON_SIZE,
                height=1,
                bg="grey"
            )
        btn.grid(row=row, column=col, padx=1, pady=1)
        btn.config(command=lambda b=btn: toggle_color(b))
        row_buttons.append(btn)
    buttons.append(row_buttons)

# Right frame for counters
right_frame = tk.Frame(main_frame)
right_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor="n")

def add_category_column(parent_frame, categories):
    for category in categories:
        cat_label = tk.Label(parent_frame, text=category, font=("Arial", 12, "bold"))
        cat_label.pack(anchor="w", pady=(10, 2))

        for i in range(1, NUM_BUTTONS + 1):
            row_frame = tk.Frame(parent_frame)
            row_frame.pack(anchor="w", pady=2)

            btn = tk.Button(row_frame, text=f"{category}{i}", width=4)
            btn.pack(side=tk.LEFT)

            counter_label = tk.Label(row_frame, text="0", width=3, relief="solid")
            counter_label.pack(side=tk.LEFT, padx=5)

            # Bind left and right click
            btn.bind("<Button-1>", lambda e, l=counter_label: on_button_click(e, l))
            btn.bind("<Button-3>", lambda e, l=counter_label: on_button_click(e, l))

# Create two columns inside right_frame
col1 = tk.Frame(right_frame)
col1.pack(side=tk.LEFT, padx=5, anchor="n")

col2 = tk.Frame(right_frame)
col2.pack(side=tk.LEFT, padx=5, anchor="n")

# Populate both columns
add_category_column(col1, COLUMN_1)
add_category_column(col2, COLUMN_2)

root.mainloop()
