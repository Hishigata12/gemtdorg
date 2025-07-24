import tkinter as tk

GRID_SIZE = 37  # 37x37 grid
BUTTON_SIZE = 2  # Button grid size

# Split categories into two columns
COLUMN_1 = ['P', 'B', 'D', 'G']
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

# def on_button_click(event, label, button_name=None):
#     """Handle left/right click events."""
#     delta = 1 if event.num == 1 else -1  # Left = +1, Right = -1
#     update_counter(label, delta)

#     # If this button affects right-side buttons, update them too
#     if button_name and button_name in LEFT_TO_RIGHT_MAPPING:
#         for target in LEFT_TO_RIGHT_MAPPING[button_name]:
#             if target in right_counters:
#                 update_counter(right_counters[target], delta)

#     if button_name and button_name in TOWER_UPGRADE_MAPPING:
#         for target in TOWER_UPGRADE_MAPPING[button_name]:
#             if target in right_counters:
#                 update_counter(right_counters[target], delta)
#             if target in left_counters:
#                 update_counter(left_counters[target], delta)
#                 propagate_update(left_counters[target], target)

# def propagate_update(target, delta):
#     """Handle cascading updates without re-triggering click events."""
#     if target in LEFT_TO_RIGHT_MAPPING:
#         for t in LEFT_TO_RIGHT_MAPPING[target]:
#             if t in right_counters:
#                 update_counter(right_counters[t], delta)

def on_button_click(event, label, button_name=None):
    """Handle left/right click events for counters."""
    delta = 1 if event.num == 1 else -1  # Left-click = +1, Right-click = -1

    # Update the clicked button's counter
    update_counter(label, delta)

    # Update any right-side counters linked to this button
    if button_name and button_name in LEFT_TO_RIGHT_MAPPING:
        for target in LEFT_TO_RIGHT_MAPPING[button_name]:
            if target in right_counters:
                update_counter(right_counters[target], delta)

    # Update any additional linked counters from tower upgrades
    if button_name and button_name in TOWER_UPGRADE_MAPPING:
        for target in TOWER_UPGRADE_MAPPING[button_name]:
            # if target in right_counters:
            #     update_counter(right_counters[target], delta)
            if target in left_counters:
                update_counter(left_counters[target], delta)
                # Instead of calling on_button_click again,
                # we directly update linked counters to avoid recursion
                # if target in LEFT_TO_RIGHT_MAPPING:
                #     for sub_target in LEFT_TO_RIGHT_MAPPING[target]:
                        # if sub_target in right_counters:
                        #     update_counter(right_counters[sub_target], delta)
                if target in TOWER_UPGRADE_MAPPING:
                    for sub_target in TOWER_UPGRADE_MAPPING[target]:
                        # if sub_target in right_counters:
                        #     update_counter(right_counters[sub_target], delta)
                        if sub_target in left_counters:
                            update_counter(left_counters[sub_target], delta)
                            if sub_target in TOWER_UPGRADE_MAPPING:
                                for sub_sub_target in TOWER_UPGRADE_MAPPING[sub_target]:
                                    # if sub_sub_target in right_counters:
                                    #     update_counter(right_counters[sub_sub_target], delta)
                                    if sub_sub_target in left_counters:
                                        update_counter(left_counters[sub_sub_target], delta)




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
               'Asteriated Ruby','Volcano','Bloodstone','Antique Bloodstone', 'The Crown Prince',
                'Jade','Gray Jade', 'Monkey King Jade', 'Diamond Cullinan', 'Quartz', 'Lucky Chinese Jade',
                 'Charming Lazurite', 'Golden Jubilee', 'Gold', 'Egypt Gold', 'Dark Emerald', 'Emerald Golem',
                  'Paraiba Tourmaline','Elaborate Carve Tourm', 'Sapphire Star Adam', 'Deep Sea Pearl', 'Chrysoberyl Cat Eye',
                   'Natural Zumurud','Red Coral', 'Carmen Lucia', 'Yellow Sapphire', 'Northern Saber Eye', 'Star Sapphire' ]

TIER_1 = ['Silver', 'Malachite', 'Asteriated Ruby', 'Jade', 'Gold']
TIER_2 = ['Silver Knight', 'Vivid Malachite', 'Volcano', 'Gray Jade','Egypt Gold']
TIER_3 = ['Pink Diamond', 'Uranium 238', 'Bloodstone', 'Quartz', 'Dark Emerald', 'Paraiba Tourmaline',
           'Deep Sea Pearl', 'Chrysoberyl Cat Eye', 'Yellow Sapphire', ]
TIER_4 = ['Huge Pink Diamond', 'Uranium 235', 'Antique Bloodstone', 'Monkey King Jade', 'Charming Lazurite',
            'Emerald Golem', 'Elaborate Carve Tourm', 'Natural Zumurud', 'Red Coral', 'Northern Saber Eye']
TIER_5 = ['Koh-i-noor Diamond', 'Depleted Kyparium', 'The Crown Prince', 'Diamond Cullinan',
           'Golden Jubilee', 'Sapphire Star Adam', 'Carmen Lucia', 'Star Sapphire']

# Example mapping: which right-side buttons to affect when a left button is clicked
# (This can be customized per your requirements)
LEFT_TO_RIGHT_MAPPING = {
    "Silver": ["B1", "D1", "Y1"] ,
    "Silver Knight": ["R3", "Q2", "B1", "D1", "Y1"],
    "Pink Diamond": ["D5", "D4", "Y3"],
    "Huge Pink Diamond": ["B1","D1","Y1","Q2","R3","D5","D3","Y3", "B1", "D1", "Y1"],
    "Koh-i-noor Diamond": ["B1","D1","Y1","Q2","R3","D5","D3","Y3", "P6", "D6", "B1", "D1", "Y1"],
    "Malachite": ["E1", "G1", "Q1"],
    "Vivid Malachite": ["E1", "G1", "Q1", "D2", "Y3"],
    "Uranium 238": ["Y5", "B3", "E2"],
    "Uranium 235": ["E1", "G1", "Q1", "D2", "Y3","Y5", "B3", "E2", "E1", "G1", "Q1"],
    "Depleted Kyparium": ["E1", "G1", "Q1", "D2", "Y3","Y5", "B3", "E2", "Q6", "Y6", "E1", "G1", "Q1"],
    "Asteriated Ruby": ["R2", "R1", "P1"],
    "Volcano": ["R2", "R1", "P1", "R4", "P3"],
    "Bloodstone": ["R5","Q4", "P3"],
    "Antique Bloodstone": ["R5","Q4", "P3", "R2", "R1", "P1", "R4", "P3", "R2"],
    "The Crown Prince": ["R5","Q4", "P3", "R2", "R1", "P1", "R4", "P3", "R2", "R6", "G6"],
    "Jade": ["G3", "E3", "B2"],
    "Gray Jade": ["B4", "Q3", "G3", "E3", "B2"],
    "Monkey King Jade": ["G4", "P2", "B4", "Q3", "G3", "E3", "B2" ],
    "Diamond Cullinan": ["G4", "P2", "B4", "Q3", "G3", "E3", "B2", "D6", "B6"],
    "Quartz": ["G4", "R3", "P2"],
    "Lucky Chinese Jade": ["G4", "R3", "P2", "G3", "E3", "B2"],
    "Charming Lazurite": ["G4", "R3", "P2", "P4", "Y2"],
    "Golden Jubilee": ["G4", "R3", "P2", "G3", "E3", "B2", "P4", "Y2", "Y6", "R6"],
    "Gold": ["P5", "P4", "D2"],
    "Egypt Gold": ["P5", "P4", "D2", "P5", "Q2"],
    "Dark Emerald": ["G5", "B4", "Y2"],
    "Emerald Golem": ["P5", "P4", "D2", "G5", "B4", "Y2", "D3"],
    "Paraiba Tourmaline": ["Q5", "E4", "G2"],
    "Elaborate Carve Tourm": ["G2", "P5", "P4", "D2", "Q5", "E4", "G2"],
    "Sapphire Star Adam": ["G6", "P6", "G2", "P5", "P4", "D2", "Q5", "E4", "G2"],
    "Deep Sea Pearl": ["Q4", "D4", "E2"],
    "Chrysoberyl Cat Eye": ["E5", "D4", "Q3"],
    "Natural Zumurud": ["G5", "D3", "Q4", "D4", "E2"],
    "Red Coral": ["E5", "D4", "Q3", "Q4", "D4", "E2", "E4"],
    "Carmen Lucia": ["E5", "D4", "Q3", "Q4", "D4", "E2", "E4", "E6", "Q6"],
    "Yellow Sapphire": ["B5", "Y4", "R4"],
    "Northern Saber Eye": ["B5", "B5", "Y4", "R4", "R5","Q4", "P3"],
    "Star Sapphire": ["B5", "Y4", "R4", "B6", "E6"]
    # ... add more mappings as needed
}

TOWER_UPGRADE_MAPPING = {
    "Silver": ["B1", "D1", "Y1"] ,
    "Silver Knight": ["R3", "Q2", "Silver"],
    "Pink Diamond": ["D5", "D4", "Y3"],
    "Huge Pink Diamond": ["Pink Diamond", 'Silver Knight', 'Silver'],
    "Koh-i-noor Diamond": ["Huge Pink Diamond", "P6", "D6"],
    "Malachite": ["E1", "G1", "Q1"],
    "Vivid Malachite": ["Malachite", "D2", "Y3"],
    "Uranium 238": ["Y5", "B3", "E2"],
    "Uranium 235": ["Uranium 238", 'Malachite', 'Vivid Malachite'],
    "Depleted Kyparium": ["Uranium 235", "Q6", "Y6"],
    "Asteriated Ruby": ["R2", "R1", "P1"],
    "Volcano": ["Asteriated Ruby", "R4", "P3"],
    "Bloodstone": ["R5","Q4", "P3"],
    "Antique Bloodstone": ["Bloodstone", "Volcano", "R2"],
    "The Crown Prince": ["Antique Bloodstone", "R6", "G6"],
    "Jade": ["G3", "E3", "B2"],
    "Gray Jade": ["B4", "Q3", "Jade"],
    "Monkey King Jade": ["G4", "P2", 'Gray Jade'],
    "Diamond Cullinan": ["Monkey King Jade", "D6", "B6"],
    "Quartz": ["G4", "R3", "P2"],
    "Lucky Chinese Jade": ["Jade", "Quartz", "G3"],
    "Charming Lazurite": ["Quartz", "P4", "Y2"],
    "Golden Jubilee": ["Charming Lazurite", "Y6", "R6"],
    "Gold": ["P5", "P4", "D2"],
    "Egypt Gold": ["Gold", "P5", "Q2"],
    "Dark Emerald": ["G5", "B4", "Y2"],
    "Emerald Golem": ["Gold", "Dark Emerald", "D3"],
    "Paraiba Tourmaline": ["Q5", "E4", "G2"],
    "Elaborate Carve Tourm": ["Paraiba Tourmaline", 'Dark Emerald', "G2"],
    "Sapphire Star Adam": ["G6", "P6", "Elaborate Carve Tourm"],
    "Deep Sea Pearl": ["Q4", "D4", "E2"],
    "Chrysoberyl Cat Eye": ["E5", "D4", "Q3"],
    "Natural Zumurud": ["G5", "D3", "Deep Sea Pearl"],
    "Red Coral": ["Chrysoberyl Cat Eye", 'Deep Sea Pearl', "E4"],
    "Carmen Lucia": ["Red Coral", "E6", "Q6"],
    "Yellow Sapphire": ["B5", "Y4", "R4"],
    "Northern Saber Eye": ["B5", "Yellow Sapphire", "Bloodstone"],
    "Star Sapphire": ["Yellow Sapphire", "B6", "E6"]
    # ... add more mappings as needed
}

# Left column frame
left_frame = tk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor="n")
basic_frame = tk.Frame(main_frame)
basic_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor="n")
next_frame = tk.Frame(main_frame)
next_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor="n")
final_frame = tk.Frame(main_frame)
final_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor="n")



# Create 38 left-side buttons with counters
left_counters = {}

def add_towers(parent_frame, towers):
    for tower in towers:
        row_frame = tk.Frame(parent_frame)
        row_frame.pack(anchor="w", pady=2)

        btn = tk.Button(row_frame, text=tower, width=20, height=1, font=("Arial", 7))
        btn.pack(side=tk.LEFT)

        counter_label = tk.Label(row_frame, text="0", width=3, relief="solid")
        counter_label.pack(side=tk.LEFT, padx=5)

        left_counters[tower] = counter_label
        btn.bind("<Button-1>", lambda e, l=counter_label, n=tower: on_button_click(e, l, n))
        btn.bind("<Button-3>", lambda e, l=counter_label, n=tower: on_button_click(e, l, n))

# for item in LEFT_ITEMS:
#     row_frame = tk.Frame(left_frame)
#     row_frame.pack(anchor="w", pady=2)

#     btn = tk.Button(row_frame, text=item, width=20, height=1, font=("Arial", 7))
#     btn.pack(side=tk.LEFT)

#     counter_label = tk.Label(row_frame, text="0", width=3, relief="solid")
#     counter_label.pack(side=tk.LEFT, padx=5)

#     left_counters[item] = counter_label
#     btn.bind("<Button-1>", lambda e, l=counter_label, n=item: on_button_click(e, l, n))
#     btn.bind("<Button-3>", lambda e, l=counter_label, n=item: on_button_click(e, l, n))

# Create two columns inside right_frame
col1 = tk.Frame(right_frame)
col1.pack(side=tk.LEFT, padx=5, anchor="n")

col2 = tk.Frame(right_frame)
col2.pack(side=tk.LEFT, padx=5, anchor="n")

# Populate both columns
add_category_column(col1, COLUMN_1)
add_category_column(col2, COLUMN_2)
add_towers(basic_frame, TIER_1)
add_towers(basic_frame, TIER_3)
add_towers(next_frame, TIER_2)
add_towers(next_frame, TIER_4)
add_towers(final_frame, TIER_5)

root.mainloop()
