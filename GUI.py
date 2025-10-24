"""
Name: Austin
This is the improved version of the GUI using
PyQt6. (requires install)
"""

import sys
from PyQt6.QtWidgets import (QComboBox, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFrame, QScrollArea, QDialog,
                             QLineEdit, QMenu, QApplication)
from PyQt6.QtCore import Qt, QTimer, QTime, pyqtSignal, QObject
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
class AlarmSignals(QObject):
    """Signal handler for thread-safe alarm triggering"""
    alarm_triggered = pyqtSignal(object, object)  # question_gen, callback

class AlarmPanel(QWidget):
    """
    Displays the list of set alarms in the left panel
    """
    def __init__(self):
        super().__init__()
        self.alarm_threads = {}
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title Label
        title = QLabel("Alarms")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont(font_name, 18, QFont.Weight.Bold))
        title.setStyleSheet("color: white; padding: 10px;")
        layout.addWidget(title)

        # Scroll area for alarms
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        # Container for alarm widgets
        self.alarm_container = QWidget()
        self.alarm_layout = QVBoxLayout()
        self.alarm_layout.setSpacing(10)
        self.alarm_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.alarm_container.setLayout(self.alarm_layout)

        scroll.setWidget(self.alarm_container)
        layout.addWidget(scroll)

    def add_alarm(self, alarm_time_24hr, alarm_time_display, alarm_thread):
        """
        Add a new alarm to the panel.
        alarm_time_24hr: HH:MM in 24-hour format (for backend).
        alarm_time_display: Formatted display string (e.g., "12:30 PM")
        """
        self.alarm_threads[alarm_time_24hr] = alarm_thread
        alarm_widget = QFrame()
        alarm_widget.alarm_time = alarm_time_24hr  # Add this line to identify widget
        alarm_widget.setStyleSheet(f"""
            QFrame {{
                background-color: #2a2a2a;
                border-radius: 5px;
                padding: 10px;      
            }}
        """)

        alarm_layout = QHBoxLayout()
        alarm_widget.setLayout(alarm_layout)

        # Time label
        time_label = QLabel(alarm_time_display)
        time_label.setFont(QFont(font_name, 16))
        time_label.setStyleSheet("color: white;")
        alarm_layout.addWidget(time_label)

        alarm_layout.addStretch()

        # Delete button
        delete_btn = QPushButton("✕")
        delete_btn.setFixedSize(30, 30)
        delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {dark_fg_var};
                color: white;
                border-radius: 10px;
                font-size: 20px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {dark_hover_var}
            }}
        """)
        delete_btn.clicked.connect(lambda: self.remove_alarm(alarm_widget, alarm_time_24hr))
        alarm_layout.addWidget(delete_btn)

        self.alarm_layout.addWidget(alarm_widget)
    
    def remove_alarm(self, alarm_widget, alarm_time):
        """Remove an alarm from the panel and stop the alarm thread"""
        self.alarm_layout.removeWidget(alarm_widget)
        alarm_widget.deleteLater()

        if alarm_time in self.alarm_threads:
            thread_info = self.alarm_threads[alarm_time]
            if 'stop_event' in thread_info:
                thread_info['stop_event'].set()
            del self.alarm_threads[alarm_time]

        print(f"Removed alarm: {alarm_time}") # Debug print

    def remove_alarm_by_time(self, alarm_time):
        """Remove an alarm by its time string (called after alarm completes)"""
        if alarm_time in self.alarm_threads:
            thread_info = self.alarm_threads[alarm_time]
            
            # Find and remove the widget
            for i in range(self.alarm_layout.count()):
                widget = self.alarm_layout.itemAt(i).widget()
                if widget:
                    # Check if this is the alarm widget for this time
                    # Store alarm_time in widget to identify it
                    if hasattr(widget, 'alarm_time') and widget.alarm_time == alarm_time:
                        self.alarm_layout.removeWidget(widget)
                        widget.deleteLater()
                        break
            
            # Stop the alarm by setting the stop event
            if 'stop_event' in thread_info:
                thread_info['stop_event'].set()
            
            del self.alarm_threads[alarm_time]
            print(f"Alarm completed and removed: {alarm_time}")

class SettingsPanel(QWidget):
    """
    Settings panel that overlays the main window
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.hide() # Initially hidden

    def initUI(self):
        from PyQt6.QtWidgets import QSizePolicy
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg};
                border-radius: 15px;
            }}
    """)
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Header with title and close button
        header = QHBoxLayout()

        title = QLabel("Settings")
        title.setFont(QFont(font_name, 24, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        header.addWidget(title)

        header.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(40, 40)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {dark_fg_var};
                color: white;
                border-radius: 20px;
                font-size: 20px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {dark_hover_var};
            }}
        """)
        close_btn.clicked.connect(self.hide)
        header.addWidget(close_btn)

        layout.addLayout(header)
        layout.addSpacing(20)

        # Add settings options here
        # Scroll area for settings
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        settings_container = QWidget()
        settings_layout = QVBoxLayout()
        settings_layout.setSpacing(20)
        settings_container.setLayout(settings_layout)

        # Add more color pickers here as needed
        # Example for future:
        # self.button_color_picker = ColorPicker(
        #   "Button Color",
        #   default_color="#FFFFFF",
        #   on_color_change=self.apply_BUTTON_color
        #)
        # settings_layout.addWidget(self.button_color_picker)

        # Clock Color Setting
        self.clock_color_picker = ColorPicker(
            "Clock Color",
            default_color="#FFFFFF",
            on_color_change=self.apply_clock_color
        )
        settings_layout.addWidget(self.clock_color_picker)

        # Cancel Button Color Setting
        self.cancel_color_picker = ColorPicker(
            "Cancel Color",
            default_color="#924F4F",
            on_color_change=self.apply_cancel_color
        )
        self.cancel_color_picker.color_combo.setCurrentText("Red")  # Set to Red by default
        settings_layout.addWidget(self.cancel_color_picker)

        settings_layout.addStretch()
        scroll.setWidget(settings_container)
        layout.addWidget(scroll)

    def lighten_color(self, hex_color, factor=1.2):
        """Lighten a hex color by a factor"""
        # Remove the '#' if present
        hex_color = hex_color.lstrip('#')

        # Convert to RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        # Lighten
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))

        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"

    def apply_clock_color(self, color):
        """Apply color to the clock display"""
        main_window = self.parent().parent()
        if hasattr(main_window, 'DigitalClock'):
            main_window.DigitalClock.time_label.setStyleSheet(f"color: {color};")

    def apply_cancel_color(self, color):
        """Apply color to the cancel button"""
        main_window = self.parent().parent()
        if hasattr(main_window, 'cancel_button_color'):
            main_window.cancel_button_color = color # Stores the color
            # Apply immediately if button is visible
            if hasattr(main_window, 'SetCancelButtons'):
                if main_window.SetCancelButtons.cancelBtn.isEnabled():
                    # Calculate lighter hover color
                    hover_color = self.lighten_color(color, 1.2)
                    main_window.SetCancelButtons.cancelBtn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {color};
                            color: #212121;
                            font-size: 24px;
                        }}
                        QPushButton:hover {{
                            background-color: {hover_color};
                            filter: brightness(1.2);
                        }}
                    """)

class ColorPicker(QWidget):
    """
    Reusable color picker widget with preset and custom hex options
    """
    def __init__(self, label_text, default_color="#FFFFFF", on_color_change=None):
        super().__init__()
        self.on_color_change = on_color_change
        self.current_color = default_color
        self.initUI(label_text)

    def initUI(self, label_text):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        self.setLayout(layout)

        # Label
        label = QLabel(label_text)
        label.setFont(QFont(font_name, 16, QFont.Weight.Bold))
        label.setStyleSheet("color: white;")
        layout.addWidget(label)

        # Color dropdown
        self.color_combo = QComboBox()
        self.color_combo.addItems(["White", "Green", "Red", "Blue", "Yellow", "Cyan", "Magenta", "Custom"])
        self.color_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: #2a2a2a;
                color: white;
                border: 2px solid {fg_var};
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 10px;
            }}
            QComboBox QAbstractItemView {{
                background-color: #2a2a2a;
                color: white;
                selection-background-color: {fg_var};
            }}
        """)
        self.color_combo.currentTextChanged.connect(self.on_combo_changed)
        layout.addWidget(self.color_combo)

        # Custom hex input (initially hidden)
        self.hex_input = QLineEdit()
        self.hex_input.setPlaceholderText("Enter hex color (e.g., #FF5733)")
        self.hex_input.setMaxLength(7)
        self.hex_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: #2a2a2a;
                color: white;
                border: 2px solid {fg_var};
                border-radius: 5px;
                padding: 8px;
                font-size: 16px;
            }}
        """)
        self.hex_input.hide()
        self.hex_input.textChanged.connect(self.validate_hex_input)
        layout.addWidget(self.hex_input)

        # Apply custom color button
        self.apply_btn = QPushButton("Apply Custom Color")
        self.apply_btn.setFixedHeight(35)
        self.apply_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {fg_var};
                color: #212121;
                font-size: 16 px;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {hover_var};
            }}
        """)
        self.apply_btn.hide()
        self.apply_btn.clicked.connect(self.apply_custom_color)
        layout.addWidget(self.apply_btn)

    def on_combo_changed(self, color_name):
        """Handle color selection change"""
        if color_name == "Custom":
            self.hex_input.show()
            self.apply_btn.show()
        else:
            self.hex_input.hide()
            self.apply_btn.hide()

            # Apply preset colors
            color_map = {
                "White": "#FFFFFF",
                "Green": "#4F925F",
                "Red": "#BD6565",
                "Blue": "#4A90E2",
                "Yellow": "#F4D03F",
                "Cyan": "#5DADE2",
                "Magenta": "#AF7AC5"
            }
            
            if color_name in color_map:
                self.set_color(color_map[color_name])
    
    def validate_hex_input(self, text):
        """Validate hex input as user types"""
        # Auto-add '#' if not present
        if text and not text.startswith('#'):
            self.hex_input.setText('#' + text)
            return

        # Check if valid hex (allow partial input)
        if len(text) > 1:
            try:
                int(text[1:], 16)
                self.hex_input.setStyleSheet(f"""
                    QLineEdit {{
                        background-color: #2a2a2a;
                        color: white;
                        border: 2px solid {fg_var};
                        border-radius: 5px;
                        padding: 8px;
                        font-size: 16px;
                    }}
                """)
            except ValueError:
                self.hex_input.setStyleSheet(f"""
                    QLineEdit {{
                        background-color: #2a2a2a;
                        color: white;
                        border: 2px solid {dark_fg_var};
                        border-radius: 5px;
                        padding: 8px;
                        font-size: 16px;
                    }}
                """)

    def apply_custom_color(self):
        """Apply custom hex color"""
        hex_color = self.hex_input.text()

        # Validate full hex code
        if len(hex_color) == 7 and hex_color.startswith('#'):
            try:
                int(hex_color[1:], 16)
                self.set_color(hex_color)
            except ValueError:
                pass

    def set_color(self, color):
        """Set the color and call the callback"""
        self.current_color = color
        if self.on_color_change:
            self.on_color_change(color)
    
    def get_color(self):
        """Get the current color"""
        return self.current_color

class QuestionDialog(QDialog):
    """
    Dialog that displays a question and requires correct answer to dismiss
    """
    def __init__(self, parent=None, question_generator=None):
        super().__init__(parent)
        self.question_generator = question_generator or mq.MathQuestionGenerator()
        self.correct_answer = None
        self.initUI()
        self.generate_new_question()

    def initUI(self):
        self.setWindowTitle("Alarm - Solve to Dismiss")
        self.setModal(True)
        self.setFixedSize(400, 250)
        self.setStyleSheet(f"background-color: {bg};")

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        title = QLabel("Solve this to turn off the Alarm!")
        title.setFont(QFont(font_name, 16, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(20)

        # Question Display
        self.question_label = QLabel()
        self.question_label.setFont(QFont(font_name, 32))
        self.question_label.setStyleSheet("color: white;")
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.question_label)

        layout.addSpacing(20)

        # Answer input
        self.answer_input = QLineEdit()
        self.answer_input.setFont(QFont(font_name, 24))
        self.answer_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.answer_input.setFixedHeight(70)
        self.answer_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: #2a2a2a;
                color: white;
                border: 2px solid {fg_var};
                border-radius: 5px;
                padding: 10px
            }}
        """)
        self.answer_input.returnPressed.connect(self.check_answer)
        layout.addWidget(self.answer_input)

        layout.addSpacing(10)

        # Feedback label
        self.feedback_label = QLabel()
        self.feedback_label.setFont(QFont(font_name, 14))
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.feedback_label)

        layout.addSpacing(10)

        # Submit button
        submit_btn = QPushButton("Submit")
        submit_btn.setFixedHeight(50)
        submit_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {fg_var};
                color: #212121;
                font-size: 18px;
                font-weight: bold;
                border-radius: 5px
            }}
            QPushButton:hover {{
                background-color: {hover_var}
            }}
        """)
        submit_btn.clicked.connect(self.check_answer)
        layout.addWidget(submit_btn)

    def generate_new_question(self):
        """Generate a new question using the question generator"""
        question, answer = self.question_generator.generate_question()
        self.question_label.setText(question)
        self.correct_answer = answer
        self.answer_input.clear()
        self.feedback_label.clear()
    
    def check_answer(self):
        """Check if the user's answer is correct"""
        user_answer = int(self.answer_input.text())
        
        # Try to convert to int if the correct answer is an int
        if isinstance(self.correct_answer, int):
            try:
                user_answer = int(user_answer)
            except ValueError:
                self.feedback_label.setStyleSheet("color: #BD6565;")
                self.feedback_label.setText("Please enter a number.")
                return

        if user_answer == self.correct_answer:
            self.feedback_label.setStyleSheet("color: #6BC582;")
            self.feedback_label.setText("✓ Correct! Alarm dismissed.")
            QTimer.singleShot(500, self.accept)  # Close after 0.5s
        else:
            self.feedback_label.setStyleSheet("color: #BD6565;")
            self.feedback_label.setText(f"✗ Wrong! Try again.")


    def closeEvent(self, event):
        """Prevent closing without correct answer"""
        event.ignore()

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
            if self.alarm_time[0] == 1 and self.alarm_time[1] > 2:
                self.alarm_time[1] = 0
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
            if self.alarm_time[0] == 1 and self.alarm_time[1] > 2:
                self.alarm_time [1] = 2
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
    
    def get_alarm_display_string(self):
        """Get the alarm time in 12-hour format for display"""
        hour = self.alarm_time[0] * 10 + self.alarm_time[1]
        minute = self.alarm_time[2] * 10 + self.alarm_time[3]
        return f"{hour:02d}:{minute:02d} {self.alarm_period}"

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
    def __init__(self, layout_to_add_to, up_down_buttons, digital_clock, alarm_panel, main_window):
        super().__init__()
        self.layout = layout_to_add_to
        self.up_down_buttons = up_down_buttons
        self.digital_clock = digital_clock
        self.alarm_panel = alarm_panel
        self.main_window = main_window
        self.buttons_hidden = True # Initially sets that buttons are hidden
        self.alarms = []
        self.create_buttons()
        # Signal handler for alarms
        self.alarm_signals = AlarmSignals()
        self.alarm_signals.alarm_triggered.connect(self.show_question_dialog)

    def create_buttons(self):
        """
        Creates and sets up the Set and Cancel buttons.
        """
        # Creates a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

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
            # Get the stored color from MainWindow
            if hasattr(self.main_window, 'cancel_button_color'):
                cancel_color = self.main_window.cancel_button_color
            else:
                cancel_color = dark_fg_var # Fallback to default
            
            # Calculate hover color
            hover_color = self.lighten_color(cancel_color, 1.2)

            self.cancelBtn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {cancel_color}; 
                    color: #212121; 
                    font-size: 24px;
                }}
                QPushButton:hover {{
                    background-color: {hover_color};
                    filter: brightness(1.2);
                }}
            """)
            self.up_down_buttons.show_buttons()
            self.digital_clock.enter_alarm_mode()
            self.buttons_hidden = False
        else:
            # Confirming alarm
            alarm_time_24hr = self.digital_clock.get_alarm_time_string()
            alarm_time_display = self.digital_clock.get_alarm_display_string()
            self.alarms.append(alarm_time_24hr)
            print(f"Alarm set for: {alarm_time_24hr}") # Debug print

            # Create question generator (can be customized later)
            question_gen = mq.MathQuestionGenerator()

            # Store alarm time for removal after completion
            alarm_time_to_remove = alarm_time_24hr

            # Create a thread-safe callback using signals
            def on_alarm():
                """Signal main thread to show question dialog"""
                import threading
                result_event = threading.Event()
                result_container = {'success': False}

                def callback(success):
                    result_container['success'] = success
                    result_event.set()

                # Emit signal to main thread
                self.alarm_signals.alarm_triggered.emit(question_gen, callback)

                # Wait for result
                result_event.wait()

                # Remove alarm from panel after correct answer
                if result_container['success']:
                    self.alarm_panel.remove_alarm_by_time(alarm_time_to_remove)

                return result_container['success']

            # Add alarm to the panel and start it
            alarm_thread = alarm.start_alarm(alarm_time_24hr, on_alarm_trigger=on_alarm)
            self.alarm_panel.add_alarm(alarm_time_24hr, alarm_time_display, alarm_thread)

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
            self.digital_clock.exit_alarm_mode()
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

    def show_question_dialog(self, question_gen, callback):
        """Show question dialog in main thread"""
        dialog = QuestionDialog(None, question_gen)
        result = dialog.exec() == QDialog.DialogCode.Accepted
        callback(result)

    def lighten_color(self, hex_color, factor=1.2):
        """Lighten a hex color by a factor"""
        # Remove the '#' if present
        hex_color = hex_color.lstrip('#')
    
        # Convert to RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    
        # Lighten
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
    
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"

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
        self.alarm_panel = AlarmPanel()
        alarm_panel_frame = QFrame()
        alarm_panel_frame.setFixedWidth(300)
        alarm_panel_frame.setStyleSheet(f"background-color: #1a1a1a; border-radius: 15px;")
        alarm_panel_layout = QVBoxLayout()
        alarm_panel_frame.setLayout(alarm_panel_layout)
        alarm_panel_layout.addWidget(self.alarm_panel)
        main_horizontal.addWidget(alarm_panel_frame)

        # Create clock section to the right
        clock_widget = QWidget()
        self.main_layout = QVBoxLayout()
        clock_widget.setLayout(self.main_layout)
        clock_widget.setStyleSheet(f"background-color: {bg}; border-radius: 15px;")
        main_horizontal.addWidget(clock_widget)

        # Create settings panel (initially hidden, overlays clock widget)
        self.settings_panel = SettingsPanel(clock_widget)

        # Add settings button in top right
        settings_layout = QHBoxLayout()
        settings_layout.addStretch()
        
        settings_btn = QPushButton("⋮")
        settings_btn.setFixedSize(50, 50)
        settings_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: #888888;
                font-size: 30px;
                border: none;
            }}
            QPushButton:hover {{
                color: {fg_var};
            }}
        """)
        settings_layout.addWidget(settings_btn)
        settings_btn.clicked.connect(self.open_settings)

        self.main_layout.addLayout(settings_layout)

        # Add spacing at the top
        self.main_layout.addSpacing(50)

        # Creates each piece of the GUI
        self.DigitalClock = DigitalClock()
        self.UpDownButtons = UpDownButtons(self.main_layout, self.DigitalClock)
        self.main_layout.addWidget(self.DigitalClock.time_label)
        self.UpDownButtons.add_down_buttons()

        self.main_layout.addSpacing(20)

        self.SetCancelButtons = SetCancelButtons(self.main_layout, self.UpDownButtons, 
                                                 self.DigitalClock, self.alarm_panel, self)
    
        self.cancel_button_color = dark_fg_var  # Store default color
    
    def open_settings(self):
        """Show the settings panel"""
        # Get the parent (clock_widget) size
        parent = self.settings_panel.parent()
        self.settings_panel.setGeometry(0, 0, parent.width(), parent.height())
        self.settings_panel.show()
        self.settings_panel.raise_()  # Bring to front

    def resizeEvent(self, event):
        """Handle window resize to update settings panel size"""
        super().resizeEvent(event)
        if hasattr(self, 'settings_panel') and self.settings_panel.isVisible():
            parent = self.settings_panel.parent()
            self.settings_panel.setGeometry(0, 0, parent.width(), parent.height())

# Runs only if the main file is run
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())