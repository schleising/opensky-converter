"""Creates a progress dialog for the user to see the progress of the conversion.
"""

from pathlib import Path
from typing import Dict

import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import _setup_dialog # type: ignore

from Converter import Converter

class ProgressDialog:
    def __init__(self, parent: tk.Tk, current_file_path: Path, new_file_path: Path, output_file_path: Path, mapping: Dict[str, str]) -> None:
        """Creates the progress dialog.

        Args:
            parent (tk.Tk): The parent window.
        """
        # Store the parent window
        self.parent = parent

        # Create the dialog
        self.dialog = tk.Toplevel(self.parent)

        # Set the title
        self.dialog.title('Converting...')

        # Remove normal window decorations
        _setup_dialog(self.dialog)

        # Disable resizing the window
        self.dialog.resizable(False, False)

        # Create a frame to hold the widgets
        frame = ttk.Frame(self.dialog)
        frame.grid(column=0, row=0, padx=10, pady=10)

        # Create the labels
        label = ttk.Label(frame, text='Reading Current File')
        label.grid(column=0, row=0, sticky=tk.W)

        label = ttk.Label(frame, text='Merging New File')
        label.grid(column=0, row=1, sticky=tk.W)

        label = ttk.Label(frame, text='Writing Output File')
        label.grid(column=0, row=2, sticky=tk.W)

        # Create the progress bars
        self.current_file_progress_bar = ttk.Progressbar(frame, orient='horizontal', length=300, mode='determinate')
        self.current_file_progress_bar.grid(column=1, row=0, sticky=tk.EW)

        self.new_file_progress_bar = ttk.Progressbar(frame, orient='horizontal', length=300, mode='determinate')
        self.new_file_progress_bar.grid(column=1, row=1, sticky=tk.EW)

        self.output_file_progress_bar = ttk.Progressbar(frame, orient='horizontal', length=300, mode='determinate')
        self.output_file_progress_bar.grid(column=1, row=2, sticky=tk.EW)

        # Create the cancel button
        self.cancel_button = ttk.Button(frame, text='Cancel', command=self.cancel)
        self.cancel_button.grid(column=1, row=3, sticky=tk.E)

        # Add padding to the widgets
        for child in frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # Set the main window to be transient
        self.dialog.transient(self.parent)

        # Wait for the dialog to be visible
        self.dialog.wait_visibility()

        # Set the dialog to be modal
        self.dialog.grab_set()

        # Initialise conversion cancelled to False
        self.conversion_cancelled = False

        # Create the converter
        self.converter = Converter(current_file_path, new_file_path, output_file_path, mapping)

        # Initialise the current file
        self.converter.initialise_current_file()

        # Start reading the current file
        self.read_current_file()

    def read_current_file(self) -> None:
        """Reads the current file."""
        # Check if the conversion has been cancelled
        if not self.conversion_cancelled:
            # Read the current file
            percentage_read, still_reading = self.converter.read_current_file()

            print(f'Current File: {percentage_read:3.2f}%')

            # Update the progress bar
            self.current_file_progress_bar['value'] = percentage_read

            if still_reading:
                # Continue reading the current file
                self.parent.after(1, self.read_current_file)

    def cancel(self) -> None:
        """Cancels the conversion."""
        # Close the files
        self.converter.conversion_cancelled()

        # Set conversion cancelled to True
        self.conversion_cancelled = True

        # Destroy the dialog
        self.destroy()

    def destroy(self) -> None:
        """Destroys the dialog."""
        # Release the dialog
        self.dialog.grab_release()

        # Destroy the dialog
        self.dialog.destroy()
