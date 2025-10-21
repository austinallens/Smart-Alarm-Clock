"""
Smart Alarm - Main Entry Point
Run this file to start the application
"""
from PyQt6.QtWidgets import QApplication
from GUI import MainWindow # Import the GUI module
import sys

if __name__ == "__main__":
    # Start the application
    print("Starting Smart Alarm...")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())