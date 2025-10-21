#########################
# Name: Austin
# This is the improved version of the GUI using
# PyQt6. (requires install)
#########################

# CURRENT ISSUES: Wierd Spacing, Button next to alarm doesn't actually work, No need for '-' button instead use it to cancel set, No need for 'check' button remove it

import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFrame, QScrollArea, QDialog,
                             QLineEdit, QGridLayout, QApplication)
from PyQt6.QtCore import Qt, QTimer, QTime
from PyQt6.QtGui import QFont
import alarm # Imports the alarm module
import math_questions as mq # Imports math_questions module (as mq)

# --- Values ---
# Font Constants for ease-of-change
font_name = "Arial"

# Color Constants for ease-of-change
fg_var="#4F925F"
hover_var="#6BC582"
dark_fg_var="#924F4F"
dark_hover_var="#BD6565"
bg = "#212121"

# --- Classes ---
class DigitalClock(QWidget):
    """
    Creates and sets up the digital clock
    """
    def __init__(self):
        super().__init__()
        self.time_label = QLabel(self)
        self.timer = QTimer(self)
        self.is_setting_alarm = False
        self.alarm_time = [1, 2, 0, 0] # Default alarm time: 12:00
        self.alarm_period = "AM"
        self.initUI()
    
    def initUI(self):

        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font = QFont(font_name, 150)
        self.time_label.setFont(font)

        self.setStyleSheet("background-color: #212121")

        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.update_time()

    def update_time(self):
        if self.is_setting_alarm:
            # Show alarm time being set
            alarm_display = f"{self.alarm_time[0]}{self.alarm_time[1]}:{self.alarm_time[2]}{self.alarm_time[3]}"
            self.time_label.setText(alarm_display)
        else:
            # Show current time    
            current_time = QTime.currentTime().toString("hh:mm AP")
            self.time_label.setText(current_time)
    
    def enter_alarm_mode(self):
        """Switch to alarm setting mode"""
        self.is_setting_alarm = True
        # Initilize with current time
        current = QTime.currentTime()
        hour = current.hour()
        minute = current.minute()

        # Convert to 12-hour format
        if hour == 0:
            hour = 12
            self.alarm_period = "AM"
        elif hour < 12:
            self.alarm_period = "AM"
        elif hour == 12:
            self.alarm_period = "PM"
        else:
            hour -= 12
            self.alarm_period = "PM"
        
        self.alarm_time = [hour // 10, hour % 10, minute // 10, minute % 10]
        self.update_time()
    
    def exit_alarm_mode(self):
        """Exits alarm setting mode"""
        self.is_setting_alarm = False
        self.update_time()
    
    def increment_digit(self, index):
        """Increment a specific digit of the alarm time"""
        if index == 0: # First hour digit (0-1)
            self.alarm_time[0] = (self.alarm_time[0] + 1) % 2
            if self.alarm_time[0] == 0 and self.alarm_time[1] == 0:
                self.alarm_time[1] = 1  # Can't have 00
        elif index == 1:  # Second hour digit
            max_val = 2 if self.alarm_time[0] == 1 else 9
            self.alarm_time[1] = (self.alarm_time[1] + 1)
            if self.alarm_time[1] > max_val:
                self.alarm_time[1] = 0 if self.alarm_time[0] == 1 else 1
            if self.alarm_time[0] == 0 and self.alarm_time[1] == 0:
                self.alarm_time[1] = 1  # Can't have 00
        elif index == 2:  # First minute digit (0-5)
            self.alarm_time[2] = (self.alarm_time[2] + 1) % 6
        elif index == 3:  # Second minute digit (0-9)
            self.alarm_time[3] = (self.alarm_time[3] + 1) % 10
        self.update_time()

    def decrement_digit(self, index):
        """Decrement a specific digit of the alarm time"""
        if index == 0:  # First hour digit (0-1)
            self.alarm_time[0] = (self.alarm_time[0] - 1) % 2
            if self.alarm_time[0] == 0 and self.alarm_time[1] == 0:
                self.alarm_time[1] = 1  # Can't have 00
        elif index == 1:  # Second hour digit
            max_val = 2 if self.alarm_time[0] == 1 else 9
            self.alarm_time[1] = (self.alarm_time[1] - 1)
            if self.alarm_time[1] < 0:
                self.alarm_time[1] = max_val
            if self.alarm_time[0] == 0 and self.alarm_time[1] == 0:
                self.alarm_time[1] = 9  # Wrap to 09
        elif index == 2:  # First minute digit (0-5)
            self.alarm_time[2] = (self.alarm_time[2] - 1) % 6
        elif index == 3:  # Second minute digit (0-9)
            self.alarm_time[3] = (self.alarm_time[3] - 1) % 10
        self.update_time()

    def get_alarm_time_string(self):
        """Get the alarm time in HH:MM format (24-hour)"""
        hour = self.alarm_time[0] * 10 + self.alarm_time[1]
        minute = self.alarm_time[2] * 10 + self.alarm_time[3]
        
        # Convert to 24-hour format
        if self.alarm_period == "PM" and hour != 12:
            hour += 12
        elif self.alarm_period == "AM" and hour == 12:
            hour = 0
        
        return f"{hour:02d}:{minute:02d}"

class UpDownButtons(QWidget):
    """
    Creates and sets up the Up and Down buttons for the GUI.
    The Up buttons cause the alarm digits to change by one (within normal 12-hour clock ranges).
    The Down buttons cause the alarm digits to change by one (within normal 12-hour clock ranges).
    """
    def __init__(self, layout_to_add_to, digital_clock):
        super().__init__()
        self.layout = layout_to_add_to
        self.digital_clock = digital_clock
        self.upBtns = []
        self.downBtns = []
        self.create_up_buttons()
    
    def create_up_buttons(self):
        """
        Creates a horizontal layout for the Up buttons above the digits
        """
        up_layout = QHBoxLayout()
        up_layout.setSpacing(10)
        up_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create 4 up buttons
        for i in range(4):
            upBtn = QPushButton(text="⮝", parent=self)
            upBtn.setFixedSize(100,30)
            upBtn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: transparent;
                    border: none;
                    font-size: 30px;
                }}
            """)
            # Connect to increment function
            upBtn.clicked.connect(lambda checked, idx=i: self.digital_clock.increment_digit(idx))
            self.upBtns.append(upBtn)
            up_layout.addWidget(upBtn)

        self.layout.addLayout(up_layout)
    
    def add_down_buttons(self):
        """
        Creates a horizontal layout for the Down buttons below the digits
        """
        down_layout = QHBoxLayout()
        down_layout.setSpacing(10)
        down_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Creates 4 down buttons
        for i in range(4):
            downBtn = QPushButton(text="⮟", parent=self)
            downBtn.setFixedSize(100,30)
            downBtn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: transparent;
                    border: none;
                    font-size: 30px;
                }}
            """)
            downBtn.clicked.connect(lambda checked, idx=i: self.digital_clock.decrement_digit(idx))
            self.downBtns.append(downBtn)
            down_layout.addWidget(downBtn)
        
        self.layout.addLayout(down_layout)

    def show_buttons(self):
        """
        Shows hidden Up and Down buttons (for when Set is pressed)
        """
        for btn in self.upBtns:
            btn.setEnabled(True)  # Enable clicking
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {fg_var};
                    color: #212121;
                    font-size: 30px;
                }}
                QPushButton:hover {{
                    background-color: {hover_var};
                }}
            """)        
        for btn in self.downBtns:
            btn.setEnabled(True)  # Enable clicking
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {fg_var};
                    color: #212121;
                    font-size: 30px;
                }}
                QPushButton:hover {{
                    background-color: {hover_var};
                }}
            """)
    
    def hide_buttons(self):
        """
        Hides shown Up and Down buttons (for when Set is unpressed)
        """
        for btn in self.upBtns:
            btn.setEnabled(False)  # Enable clicking
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: transparent;
                    border: none;
                    font-size: 30px;
                }}
            """)
        for btn in self.downBtns:
            btn.setEnabled(False)  # Disable clicking
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: transparent;
                    border: none;
                    font-size: 30px;
                }}
            """)


class SetCancelButtons(QWidget):
    """
    Creates and sets up the Set and Cancel buttons for the GUI.
    Set is used to set and alarm.
    Cancel is used to cancel setting the alarm.
    """
    def __init__(self, layout_to_add_to, up_down_buttons, digital_clock):
        super().__init__()
        self.layout = layout_to_add_to
        self.up_down_buttons = up_down_buttons
        self.digital_clock = digital_clock
        self.buttons_hidden = True # Initially sets that buttons are hidden
        self.alarms = []
        self.create_buttons()

    def create_buttons(self):
        """
        Creates and sets up the Set and Cancel buttons.
        """
        # Creates a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(0)

        self.setBtn = QPushButton(text="+", parent=self)
        self.setBtn.setFixedSize(100,60)
        self.setBtn.setStyleSheet(f"""
            QPushButton {{
                background-color: {fg_var}; 
                color: #212121; 
                font-size: 24px;
            }}
            QPushButton:hover {{
                background-color: {hover_var};
            }}
        """)

        self.cancelBtn = QPushButton(text="-", parent=self)
        self.cancelBtn.setFixedSize(100,60)
        self.cancelBtn.setEnabled(False)  # Disable initially
        self.cancelBtn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent; 
                color: transparent; 
                border: none;
                font-size: 24px;
            }}
        """)

        # Adds buttons to layout
        button_layout.addWidget(self.setBtn)
        button_layout.addWidget(self.cancelBtn)

        # Position set/cancel buttons
        button_container = QHBoxLayout()
        button_container.addLayout(button_layout)
        button_container.addStretch(3)

        self.layout.addLayout(button_container)

        # Connect setBtn's clicked signal to methods
        self.setBtn.clicked.connect(self.toggleBtns)
        self.cancelBtn.clicked.connect(self.cancelAlarm)

    def toggleBtns(self):
        if self.buttons_hidden:
            # Entering alarm set mode
            self.cancelBtn.setEnabled(True)  # Enable clicking
            self.cancelBtn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {dark_fg_var}; 
                    color: #212121; 
                    font-size: 24px;
                }}
                QPushButton:hover {{
                    background-color: {dark_hover_var};
                }}
            """)
            self.up_down_buttons.show_buttons()
            self.digital_clock.enter_alarm_mode()
            self.buttons_hidden = False
        else:
            # Confirming alarm
            alarm_time = self.digital_clock.get_alarm_time_string()
            self.alarms.append(alarm_time)
            print(f"Alarm set for: {alarm_time}") # Debug print

            #start the alarm
            alarm.start_alarm(alarm_time)

            # Exit alarm mode
            self.cancelBtn.setEnabled(False)  # Disable clicking
            self.cancelBtn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent; 
                    color: transparent; 
                    border: none;
                    font-size: 24px;
                }}
            """)
            self.up_down_buttons.hide_buttons()
            self.buttons_hidden = True

    def cancelAlarm(self):
        """Cancel setting the alarm"""
        self.cancelBtn.setEnabled(False)  # Disable clicking
        self.cancelBtn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent; 
                color: transparent; 
                border: none;
                font-size: 24px;
            }}
        """)
        self.up_down_buttons.hide_buttons()
        self.digital_clock.exit_alarm_mode()
        self.buttons_hidden = True

class MainWindow(QWidget):
    """
    Initilizes the Main Window and calls all the individual widgets to be ran
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Alarm Clock")
        self.setGeometry(600, 400, 800, 600)

        # Main horizontal layout for alarm panel and clock
        main_horizontal = QHBoxLayout()
        self.setLayout(main_horizontal)

        # Create alarm panel on the left
        self.alarm_panel = QFrame()
        self.alarm_panel.setFixedWidth(300)
        self.alarm_panel.setStyleSheet(f"background-color: #1a1a1a;")
        main_horizontal.addWidget(self.alarm_panel)

        # Create clock section to the right
        clock_widget = QWidget()
        self.main_layout = QVBoxLayout()
        clock_widget.setLayout(self.main_layout)
        clock_widget.setStyleSheet(f"background-color: {bg};")
        main_horizontal.addWidget(clock_widget)

        # Add spacing at the top
        self.main_layout.addSpacing(50)

        # Creates each piece of the GUI
        self.DigitalClock = DigitalClock()
        self.UpDownButtons = UpDownButtons(self.main_layout, self.DigitalClock)
        self.main_layout.addWidget(self.DigitalClock.time_label)
        self.UpDownButtons.add_down_buttons()

        self.main_layout.addSpacing(20)

        self.SetCancelButtons = SetCancelButtons(self.main_layout, self.UpDownButtons, self.DigitalClock)

# Runs only if the main file is run
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())