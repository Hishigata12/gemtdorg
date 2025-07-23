import tkinter as tk

GRID_SIZE = 37  # 37x37 grid
BUTTON_SIZE = 2  # Button grid size

# Split categories into two columns
COLUMN_1 = ['P', 'B', 'D']
COLUMN_2 = ['R', 'Q', 'E', 'Y']
NUM_BUTTONS = 6  # Each category has 5 buttons (e.g., P1..P5)

def toggle_color(btn):
    """Toggle button color between grey and green."""
    current_color = btn.cget("bg")
    btn.config(bg="green" if current_color == "grey" else "grey")

def update_counter(label, delta):
    """Increment or decrement the counter value."""
    value = int(label.cget("text"))
    value = max(0, value + delta)  # Prevent negative values
    if value > 0:
         label.config(bg="green")
         label.config(fg="white")
    else: 
         label.config(bg="#F0F0F0")
         label.config(fg="black")
    label.config(text=str(value))

# def on_button_click(event, label):
#     """Handle left/right click events on increment buttons."""
#     if event.num == 1:  # Left click
#         update_counter(label, +1)
#     elif event.num == 3:  # Right click
#         update_counter(label, -1)

def on_button_click(event, label, button_name=None):
    """Handle left/right click events."""
    delta = 1 if event.num == 1 else -1  # Left = +1, Right = -1
    update_counter(label, delta)

    # If this button affects right-side buttons, update them too
    if button_name and button_name in LEFT_TO_RIGHT_MAPPING:
        for target in LEFT_TO_RIGHT_MAPPING[button_name]:
            if target in right_counters:
                update_counter(right_counters[target], delta)

# Main window
root = tk.Tk()
root.title("Grid with Counters")

right_counters = {}  # To reference right buttons by name

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
            name = f"{category}{i}"

            row_frame = tk.Frame(parent_frame)
            row_frame.pack(anchor="w", pady=2)

            btn = tk.Button(row_frame, text=f"{category}{i}", width=4)
            btn.pack(side=tk.LEFT)

            counter_label = tk.Label(row_frame, text="0", width=3, relief="solid")
            counter_label.pack(side=tk.LEFT, padx=5)

            # Bind left and right click
            right_counters[name] = counter_label
            btn.bind("<Button-1>", lambda e, l=counter_label: on_button_click(e, l))
            btn.bind("<Button-3>", lambda e, l=counter_label: on_button_click(e, l))

# Left column items
# LEFT_ITEMS = [f"Item {i+1}" for i in range(38)]
LEFT_ITEMS = ['Silver', 'Siver Knight', 'Pink Diamond', 'Huge Pink Diamond', 'Koh-i-noor Diamond',
              'Malachite', 'Vivid Malachite', 'Uranium 238', 'Uranium 235', 'Depleted Kyparium',
               'Asteriated Ruby','Volcano','Bloodstone','Antque Bloodstone', 'The Crown Prince',
                'Jade','Gray Jade', 'Monkey King Jade', 'Diamond Cullinan', 'Quartz', 'Lucky Chinese Jade',
                 'Charming Lazurite', 'Golden Jubilee', 'Gold', 'Egypt Gold', 'Dark Emerald', 'Emerald Golem',
                  'Paraiba Tourmaline','Elaborate Carve Tourm', 'Sapphire Star Adam', 'Deep Sea Pearl', 'Chrysoberyl Cat Eye',
                   'Natural Zumurud','Red Coral', 'Carmen Lucia', 'Yellow Sapphire', 'Northern Saber Eye', 'Star Sapphire' ]

# Example mapping: which right-side buttons to affect when a left button is clicked
# (This can be customized per your requirements)
LEFT_TO_RIGHT_MAPPING = {
    "Silver": ["B1", "D1", "Y1"] ,
    "Slver Knight": ["R3", "Q2", "B1", "D1", "Y1"],
    "Pink Diamond": ["D5", "D4", "Y3"],
    "Huge Pink Diamond": ["B1","D1","Y1","Q2","R3","D5","D3","Y3"],
    "Koh-i-noor Diamond": [],
    "Malachite": [],
    "Vivid Malachite": [],
    "Uranium 238": [],
    "Uranium 235": [],
    "Depleted Kyparium": [],
    "": [],
    "": [],
    "": [],
    "": [],
    "": [],
    "": [],
    "": [],
    "": [],
    "": []
    # ... add more mappings as needed
}

# Left column frame
left_frame = tk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor="n")

# Create 38 left-side buttons with counters
left_counters = {}
for item in LEFT_ITEMS:
    row_frame = tk.Frame(left_frame)
    row_frame.pack(anchor="w", pady=2)

    btn = tk.Button(row_frame, text=item, width=20, height=1, font=("Arial", 7))
    btn.pack(side=tk.LEFT)

    counter_label = tk.Label(row_frame, text="0", width=3, relief="solid")
    counter_label.pack(side=tk.LEFT, padx=5)

    left_counters[item] = counter_label
    btn.bind("<Button-1>", lambda e, l=counter_label, n=item: on_button_click(e, l, n))
    btn.bind("<Button-3>", lambda e, l=counter_label, n=item: on_button_click(e, l, n))

# Create two columns inside right_frame
col1 = tk.Frame(right_frame)
col1.pack(side=tk.LEFT, padx=5, anchor="n")

col2 = tk.Frame(right_frame)
col2.pack(side=tk.LEFT, padx=5, anchor="n")

# Populate both columns
add_category_column(col1, COLUMN_1)
add_category_column(col2, COLUMN_2)

root.mainloop()
