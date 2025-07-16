# gui.py

"""
GUI module for Facebook Post Scheduler Application.

This module provides a graphical interface using `customtkinter` for users to:
- Compose a Facebook post.
- Choose between text, image, or video formats.
- Select a file for media posts.
- Input a specific time to schedule the post.
- Toggle between light and dark themes.

It interacts with the `scheduler_service.schedule_post` function to handle post scheduling.

Dependencies:
- customtkinter
- tkinter (filedialog, messagebox)
- scheduler_service (custom service module)
- datetime (for input validation)

Author: [Group 14]
Date: [11th July, 2025]
"""
import tkinter as ctk
from tkinter import filedialog, messagebox
from typing import Optional
from scheduler_service import schedule_post
from datetime import datetime

class FacebookSchedulerApp:
                                                                                                                                            """
                                                                                                                                            A GUI application for scheduling Facebook posts.

                                                                                                                                            Attributes:
                                                                                                                                                root (ctk.CTk): The main application window.
                                                                                                                                                media_path (Optional[str]): Path to the selected media file (image/video).
                                                                                                                                                media_type (ctk.StringVar): Type of the media (text, image, or video).
                                                                                                                                            """
                                                                                                                                            # Defined an Init constructor
                                                                                                                                            def __init__(self, root: ctk.CTk) -> None:
                                                                                                                                                """
                                                                                                                                                Initializes the FacebookSchedulerApp GUI components.

                                                                                                                                                Args:
                                                                                                                                                    root (ctk.CTk): The root window of the application.
                                                                                                                                                """
                                                                                                                                                self.root = root
                                                                                                                                                self.root.title("Facebook Post Scheduler")
                                                                                                                                                self.root.geometry("600x500")

                                                                                                                                                # Set appearance and color theme
                                                                                                                                                ctk.set_appearance_mode("System")
                                                                                                                                                ctk.set_default_color_theme("blue")

                                                                                                                                                self.media_path: Optional[str] = None  # Will store selected media file path
                                                                                                                                                self.media_type: ctk.StringVar = ctk.StringVar(value="text")  # Default to "text"

                                                                                                                                                self.build_interface()  # Build the GUI components

                                                                                                                                            def build_interface(self) -> None:
                                                                                                                                                """
                                                                                                                                                Constructs and arranges all GUI components.
                                                                                                                                                """
                                                                                                                                                # Title label
                                                                                                                                                self.title_label = ctk.CTkLabel(
                                                                                                                                                    self.root, text="Schedule Facebook Post", font=("Arial", 20, "bold")
                                                                                                                                                )
                                                                                                                                                self.title_label.pack(pady=10)

                                                                                                                                                # Textbox for the post message
                                                                                                                                                self.message_entry = ctk.CTkTextbox(self.root, width=500, height=100)
                                                                                                                                                self.message_entry.pack(pady=10)
                                                                                                                                                self.message_entry.insert("0.0", "")

                                                                                                                                                # Media selection options
                                                                                                                                                self.media_frame = ctk.CTkFrame(self.root)
                                                                                                                                                self.media_frame.pack(pady=10)

                                                                                                                                                # Radio buttons for media type
                                                                                                                                                ctk.CTkRadioButton(self.media_frame, text="Text", variable=self.media_type, value="text").pack(side="left", padx=10)
                                                                                                                                                ctk.CTkRadioButton(self.media_frame, text="Image", variable=self.media_type, value="image").pack(side="left", padx=10)
                                                                                                                                                ctk.CTkRadioButton(self.media_frame, text="Video", variable=self.media_type, value="video").pack(side="left", padx=10)

                                                                                                                                                # Button to browse for media files
                                                                                                                                                self.browse_button = ctk.CTkButton(self.root, text="Browse Media", command=self.browse_file)
                                                                                                                                                self.browse_button.pack(pady=5)

                                                                                                                                                # Label to show selected file name
                                                                                                                                                self.file_label = ctk.CTkLabel(self.root, text="No file selected", text_color="gray")
                                                                                                                                                self.file_label.pack()

                                                                                                                                                # Entry field for scheduled time
                                                                                                                                                self.time_entry = ctk.CTkEntry(self.root, placeholder_text="Enter time (HH:MM, 24h)")
                                                                                                                                                self.time_entry.pack(pady=10)

                                                                                                                                                # Submit button to schedule the post
                                                                                                                                                self.submit_button = ctk.CTkButton(self.root, text="📤 Schedule Post", command=self.submit)
                                                                                                                                                self.submit_button.pack(pady=15)

                                                                                                                                                # Theme toggle switch
                                                                                                                                                self.theme_switch = ctk.CTkSwitch(self.root, text="Light Mode", command=self.toggle_theme)
                                                                                                                                                self.theme_switch.pack(pady=10)

                                                                                                                                            def browse_file(self) -> None:
                                                                                                                                                """
                                                                                                                                                Opens a file dialog for the user to select a media file.
                                                                                                                                                Updates the media_path and the UI label accordingly.
                                                                                                                                                """
                                                                                                                                                file_path = filedialog.askopenfilename()  # Open file dialog
                                                                                                                                                if file_path:
                                                                                                                                                    self.media_path = file_path
                                                                                                                                                    # Show just the file name in the label
                                                                                                                                                    self.file_label.configure(text=f"Selected: {file_path.split('/')[-1]}", text_color="green")

                                                                                                                                            def submit(self) -> None:
                                                                                                                                                """
                                                                                                                                                Validates inputs and schedules the Facebook post using the scheduler service.
                                                                                                                                                Shows appropriate success or error messages.
                                                                                                                                                """
                                                                                                                                                # Retrieve input values
                                                                                                                                                message = self.message_entry.get("0.0", "end").strip()
                                                                                                                                                time_str = self.time_entry.get().strip()
                                                                                                                                                media_type = self.media_type.get()

                                                                                                                                                # Basic validation for text posts
                                                                                                                                                if not message and media_type == "text":
                                                                                                                                                    messagebox.showerror("Error", "Message cannot be empty for a text post.")
                                                                                                                                                    return

                                                                                                                                                # Validate time format
                                                                                                                                                try:
                                                                                                                                                    datetime.strptime(time_str, "%H:%M")
                                                                                                                                                except ValueError:
                                                                                                                                                    messagebox.showerror("Error", "Invalid time format. Use HH:MM (24h).")
                                                                                                                                                    return

                                                                                                                                                # Schedule the post using external service
                                                                                                                                                schedule_post(time_str, message, self.media_path, media_type)

                                                                                                                                                # Show confirmation
                                                                                                                                                messagebox.showinfo("Success", f"Your {media_type} post has been scheduled for {time_str}!")

                                                                                                                                            def toggle_theme(self) -> None:
                                                                                                                                                """
                                                                                                                                                Toggles between dark and light appearance modes.
                                                                                                                                                """
                                                                                                                                                current = ctk.get_appearance_mode()
                                                                                                                                                new_mode = "Light" if current == "Dark" else "Dark"
                                                                                                                                                ctk.set_appearance_mode(new_mode)
