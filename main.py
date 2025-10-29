"""
Smart Alarm - Main Entry Point
Run this file to start the application
Requires 'pip install PyQt6'
Requires 'pip install pygame' (for beeps)
"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

from GUI import MainWindow # Import the GUI module


if __name__ == "__main__":
    # Start the application
    print("Starting Smart Alarm...")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())