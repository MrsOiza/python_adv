# main.py

"""
Entry point for the Facebook Post Scheduler application.

This script initializes the CustomTkinter root window and launches the GUI
defined in `gui.py` using the `FacebookSchedulerApp` class.

Make sure all required dependencies and modules (e.g., customtkinter, gui.py)
are properly installed and available in your environment.

Author: [Group 14]
Date: [11th July 2025]
"""

import customtkinter as ctk  # Custom Tkinter module for modern UI widgets
from gui import FacebookSchedulerApp  # Import the GUI application class

# Only run the application if this script is the main program being executed
if __name__ == "__main__":
    root = ctk.CTk()  # Create a custom root window
    app = FacebookSchedulerApp(root)  # Initialize the GUI app with the root window
    root.mainloop()  # Start the GUI event loop
