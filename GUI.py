#########################
# Name: Austin
# This is the simple version of the GUI using
# Custom Tkinter. (requires install)
#########################

import customtkinter as ctk

# Default dark mode cause only weirdos use light mode
ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.geometry("1000x800")
root.title("Smart Alarm")

# --- Values ---
values = [0, 0, 0, 0]
up_buttons = []
down_buttons = []

# --- Functions ---
def increase(index):
    # Loops at 5 to prevent wonky minutes
    if index == 2:
        values[index] = (values[index] + 1) % 6
    else:
        values[index] = (values[index] + 1) % 10
    labels[index].configure(text=str(values[index]))
    print(values)

def decrease(index):
    values[index] = (values[index] - 1) % 10
    labels[index].configure(text=str(values[index]))
    print(values)

def show_clock_buttons():
    # grid all the up/down buttons and labels
    for i in range(4):
        up_buttons[i].grid()
        labels[i].grid()
        down_buttons[i].grid()
    colon.grid()

    close_button.grid(row=0, column=1, padx=(5,0))

def hide_clock_buttons():
    for i in range(4):
        up_buttons[i].grid_remove()
#        labels[i].grid_remove()
        down_buttons[i].grid_remove()
#    colon.grid_remove()

    close_button.grid_remove()

# --- Frame Setup ---
container = ctk.CTkFrame(root, fg_color="transparent")
container.pack(expand=True, fill="both", padx=40, pady=40)

main_frame = ctk.CTkFrame(container, fg_color="transparent")
main_frame.place(relx=0.5, rely=0.5, anchor="center")

alarm_button_frame = ctk.CTkFrame(root, fg_color="transparent")
alarm_button_frame.pack(side="left", padx=10, pady=20)

for i in [0, 1, 3, 4]:
    main_frame.grid_columnconfigure(i, weight=1, uniform="col")
main_frame.grid_columnconfigure(2, weight=0) # For colon


# --- Buttons ---
labels = []

# Font Constants for ease-of-change
font = "Helvetica"
font_size = 60

# Button Colors for ease-of-change
fg_color="#4F925F"
hover_color="#6BC582"
dark_fg_color="#924F4F"
dark_hover_color="#BD6565"

set_button = ctk.CTkButton(alarm_button_frame, text="+", width=120, height=50, 
                           fg_color=fg_color, hover_color=hover_color)
set_button.grid(row=0, column=0, sticky="w")

remove_button = ctk.CTkButton(alarm_button_frame, text="-", width=120, height=50, 
                              fg_color=dark_fg_color, hover_color=dark_hover_color)
remove_button.grid(row=1, column=0, pady=(5,0), sticky="w")


close_button = ctk.CTkButton(alarm_button_frame, text="🗙", width=60, height=40, 
                             fg_color=dark_fg_color, hover_color=dark_hover_color)

for i in range(4):
    
    col = i if i < 2 else i + 1 # Skips column 2 for the colon

    # Up Buttons
    up_btn = ctk.CTkButton(main_frame, text="⮝", width=60, height=40, fg_color=fg_color, hover_color=hover_color, command=lambda i=i: increase(i))
    up_btn.grid(row=0, column=col, padx=5, pady=(10, 5), )
    up_buttons.append(up_btn)

    # Num. Labels
    lbl = ctk.CTkLabel(main_frame, text=str(values[i]), font=(font, font_size, "bold"))
    lbl.grid(row=1, column=col, padx=2, pady=5)
    labels.append(lbl)

    # Down Buttons
    down_btn = ctk.CTkButton(main_frame, text="⮟", width=60, height=40, fg_color=fg_color, hover_color=hover_color, command=lambda i=i: decrease(i))
    down_btn.grid(row=2, column=col, padx=5, pady=(5, 10))
    down_buttons.append(down_btn)

# Colon label between hours and minutes
colon = ctk.CTkLabel(main_frame, text=":", font=(font, font_size, "bold"))
colon.grid(row=1, column=2, padx=0)

for i in range(4):
    up_buttons[i].grid_remove()
#    labels[i].grid_remove()
    down_buttons[i].grid_remove()
#colon.grid_remove()

set_button.configure(command=show_clock_buttons)
close_button.configure(command=hide_clock_buttons)

root.mainloop()