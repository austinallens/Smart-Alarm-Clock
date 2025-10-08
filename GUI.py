#########################
# Name: Austin
# This is the simple version of the GUI using
# Custom Tkinter. (requires install)
#########################

import customtkinter as ctk
import alarm # Imports the alarm module

# Default dark mode cause only weirdos use light mode
ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.geometry("1000x800")
root.title("Smart Alarm")

# --- Values ---
values = [0, 0, 0, 0]
up_buttons = []
down_buttons = []
active_alarms = []
alarm_labels = []
math_dialog = None # Stores reference to math dialog
correct_solution = False
current_alarm_remove_func = None

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
    if index == 2:
        values[index] = (values[index] - 1) % 6
    else:
        values[index] = (values[index] - 1) % 10
    labels[index].configure(text=str(values[index]))
    print(values)

def show_clock_buttons():
    # Grid all the up/down buttons and labels
    for i in range(4):
        up_buttons[i].grid()
        labels[i].grid()
        down_buttons[i].grid()
    colon.grid()
    close_button.grid(row=0, column=1, padx=(5,0))
    # Set button sets alarm on the second click
    set_button.configure(command=set_new_alarm)

def hide_clock_buttons():
    for i in range(4):
        up_buttons[i].grid_remove()
#        labels[i].grid_remove()
        down_buttons[i].grid_remove()
#    colon.grid_remove()

    close_button.grid_remove()
    set_button.configure(command=show_clock_buttons)

def show_math_dialog_with_remove(remove_func):
    # Remove function before showing dialog
    global current_alarm_remove_func
    current_alarm_remove_func = remove_func
    show_math_dialog()

def show_math_dialog():
    # Displays math problem dialog when alarm goes off
    global math_dialog, correct_solution, current_alarm_remove_func
    correct_solution = False

    math_dialog = ctk.CTkToplevel(root)
    math_dialog.title("WAKE UP!")
    math_dialog.geometry("400x200")
    math_dialog.attributes('-topmost', True)

    ctk.CTkLabel(math_dialog, text="Solve to stop alarm!", font=(font_name, 20, "bold")).pack(pady=20)
    ctk.CTkLabel(math_dialog, text=f"{alarm.mathProblem} = ?", font=(font_name, 24)).pack(pady=10)

    answer_entry = ctk.CTkEntry(math_dialog, width=200, font=(font_name, 18))
    answer_entry.pack(pady=10)
    answer_entry.focus()

    result_label = ctk.CTkLabel(math_dialog, text="", text_color=fg_var)
    result_label.pack()

    def check_answer():
        global correct_solution
        if answer_entry.get() == alarm.solution:
            correct_solution = True
            math_dialog.destroy()

            if current_alarm_remove_func:
                current_alarm_remove_func()
        else:
            result_label.configure(text="Wrong! Try again!")
            answer_entry.delete(0, 'end')

    submit_btn = ctk.CTkButton(math_dialog, text="Submit", command=check_answer)
    submit_btn.pack(pady=10)

    answer_entry.bind('<Return>', lambda e: check_answer())

def check_if_solved():
    # Sends back to alarm.py if problem is inputted correctly
    return correct_solution

def set_new_alarm():
    # Creates and starts a new alarm
    global correct_solution

    alarm_time = f"{values[0]}{values[1]}:{values[2]}{values[3]}"

    for i in range(4):
        values[i] = 0
        labels[i].configure(text="0")

    # Creates the alarm numbers
    alarm_frame = ctk.CTkFrame(alarm_list_frame, fg_color=fg_var)
    alarm_frame.grid(row=len(alarm_labels) + 1, column=0, pady=5, sticky="ew", padx=10)

    alarm_text = ctk.CTkLabel(alarm_frame, text=f"{alarm_time}", font=(font_name, 18))
    alarm_text.pack(side="left", padx=10, pady=5)

    def remove_alarm():
        if alarm_frame in alarm_labels:
            alarm_labels.remove(alarm_frame)
        alarm_frame.destroy()
        reposition_alarms()

    delete_btn = ctk.CTkButton(alarm_frame, text="🗙", width=30, height=30,
                               fg_color=dark_fg_var, hover_color=dark_hover_var,
                               command=remove_alarm)
    delete_btn.pack(side="right", padx=5, pady=5)

    alarm_labels.append(alarm_frame)

    # Starts alarm using imported alarm module
    correct_solution = False
    alarm_thread = alarm.start_alarm(
        alarm_time, on_alarm_trigger=lambda: show_math_dialog_with_remove(remove_alarm),
        check_solution=check_if_solved()
    )
    active_alarms.append(alarm_thread, remove_alarm)

    # Hide clock after setting
    hide_clock_buttons()

def reposition_alarms():
    # Moves alarm labels after deletion
    for idx, label in enumerate(alarm_labels):
        label.grid(row=idx + 1, column=0, pady=5, sticky="ew", padx=10)

def remove_last_alarm():
    # Removes most recently created alarm from the list
    if alarm_labels:
        last_alarm = alarm_labels.pop()
        last_alarm.destroy()
        reposition_alarms()

# Font Constants for ease-of-change
font_size = 60
font_name = "Helvetica"

# Color Constants for ease-of-change
fg_var="#4F925F"
hover_var="#6BC582"
dark_fg_var="#924F4F"
dark_hover_var="#BD6565"

# --- Frame Setup ---
container = ctk.CTkFrame(root, fg_color="transparent")
container.pack(expand=True, fill="both", padx=40, pady=40)

# Left Side - Alarm list
alarm_list_frame = ctk.CTkFrame(container, fg_color="transparent")
alarm_list_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))

ctk.CTkLabel(alarm_list_frame, text="Active Alarms", 
             font=(font_name, 24, "bold")).grid(row=0, column=0, pady=(0,20), sticky="w", padx=10)

# Right Side - Clock Setter
right_container = ctk.CTkFrame(container, fg_color="transparent")
right_container.pack(side="right", fill="both", expand=True)

main_frame = ctk.CTkFrame(container, fg_color="transparent")
main_frame.pack(expand=True)

alarm_button_frame = ctk.CTkFrame(root, fg_color="transparent")
alarm_button_frame.pack(pady=20)

for i in [0, 1, 3, 4]:
    main_frame.grid_columnconfigure(i, weight=1, uniform="col")
main_frame.grid_columnconfigure(2, weight=0) # For colon


# --- Buttons ---
labels = []

set_button = ctk.CTkButton(alarm_button_frame, text="+", width=120, height=50, 
                           fg_color=fg_var, hover_color=hover_var,
                           command=show_clock_buttons)
set_button.grid(row=0, column=0, sticky="w")

remove_button = ctk.CTkButton(alarm_button_frame, text="-", width=120, height=50, 
                              fg_color=dark_fg_var, hover_color=dark_hover_var,
                              command=remove_last_alarm)
remove_button.grid(row=1, column=0, pady=(5,0), sticky="w")


close_button = ctk.CTkButton(alarm_button_frame, text="🗙", width=60, height=40, 
                             fg_color=dark_fg_var, hover_color=dark_hover_var,
                             command=hide_clock_buttons)

for i in range(4):
    
    col = i if i < 2 else i + 1 # Skips column 2 for the colon

    # Up Buttons
    up_btn = ctk.CTkButton(main_frame, text="⮝", width=60, height=40, fg_color=fg_var, hover_color=hover_var, command=lambda i=i: increase(i))
    up_btn.grid(row=0, column=col, padx=5, pady=(10, 5), )
    up_buttons.append(up_btn)

    # Num. Labels
    lbl = ctk.CTkLabel(main_frame, text=str(values[i]), font=(font_name, font_size, "bold"))
    lbl.grid(row=1, column=col, padx=2, pady=5)
    labels.append(lbl)

    # Down Buttons
    down_btn = ctk.CTkButton(main_frame, text="⮟", width=60, height=40, fg_color=fg_var, hover_color=hover_var, command=lambda i=i: decrease(i))
    down_btn.grid(row=2, column=col, padx=5, pady=(5, 10))
    down_buttons.append(down_btn)

# Colon label between hours and minutes
colon = ctk.CTkLabel(main_frame, text=":", font=(font_name, font_size, "bold"))
colon.grid(row=1, column=2, padx=0)

for i in range(4):
    up_buttons[i].grid_remove()
#    labels[i].grid_remove()
    down_buttons[i].grid_remove()
#colon.grid_remove()

#set_button.configure(command=show_clock_buttons)
#close_button.configure(command=hide_clock_buttons)

root.mainloop()