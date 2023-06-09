"""Creates a progress dialog for the user to see the progress of the conversion.
"""

import logging
from pathlib import Path
from tkinter import messagebox
from typing import Dict

import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import _setup_dialog # type: ignore

from Converter import Converter

import constants

class ProgressDialog:
    """Creates the progress dialog.

    Args:
        parent (tk.Tk): The parent window.
        current_file_path (Path): The path to the current file.
        current_file_delimiter (str): The delimiter of the current file.
        new_file_path (Path): The path to the new file.
        new_file_delimiter (str): The delimiter of the new file.
        output_file_path (Path): The path to the output file.
        mapping (Dict[str, str]): The mapping of the fields.
    """
    def __init__(
            self, parent: tk.Tk,
            current_file_path: Path,
            current_file_delimiter: str,
            new_file_path: Path,
            new_file_delimiter: str,
            output_file_path: Path,
            mapping: Dict[str, str]
        ) -> None:
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
        self.current_file_progress_bar = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.current_file_progress_bar.grid(column=1, row=0, sticky=tk.EW)

        self.new_file_progress_bar = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.new_file_progress_bar.grid(column=1, row=1, sticky=tk.EW)

        self.output_file_progress_bar = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
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
        self.converter = Converter(
            current_file_path,
            current_file_delimiter,
            new_file_path,
            new_file_delimiter,
            output_file_path,
            mapping
        )

        # Initialise the current file
        self.converter.initialise_current_file()

        # Start reading the current file
        self.read_current_file()

        # Log the the progress dialog has been created
        logging.debug('Progress Dialog Created')

    def read_current_file(self) -> None:
        """Reads the current file."""
        # Check if the conversion has been cancelled
        if not self.conversion_cancelled:
            # Read the current file
            percentage_read, still_reading = self.converter.read_current_file()

            # Log the progress
            logging.debug(f'Current File: {percentage_read:3.2f}%, Still Reading: {still_reading}')

            # Update the progress bar
            self.current_file_progress_bar.configure(value=percentage_read)

            if still_reading:
                # Continue reading the current file
                self.parent.after(1, self.read_current_file)
            else:
                # Set the progress bar to 100%
                self.current_file_progress_bar.configure(value=100)

                # Initialise the new file
                self.converter.initialise_new_file()

                # Start merging the new file
                self.parent.after(1, self.merge_new_file)

    def merge_new_file(self) -> None:
        """Merges the new file."""
        # Check if the conversion has been cancelled
        if not self.conversion_cancelled:
            # Merge the new file
            percentage_merged, still_merging = self.converter.merge_new_file()

            # Log the progress
            logging.debug(f'New File: {percentage_merged:3.2f}%, Still Merging: {still_merging}')

            # Update the progress bar
            self.new_file_progress_bar.configure(value=percentage_merged)

            if still_merging:
                # Continue merging the new file
                self.parent.after(1, self.merge_new_file)
            else:
                # Set the progress bar to 100%
                self.new_file_progress_bar.configure(value=100)

                # Initialise the output file
                self.converter.initialise_output_file()

                # Start writing the output file
                self.parent.after(1, self.write_output_file)

    def write_output_file(self) -> None:
        """Writes the output file."""
        # Check if the conversion has been cancelled
        if not self.conversion_cancelled:
            # Write the output file
            percentage_written, still_writing = self.converter.write_output_file()

            # Log the progress
            logging.debug(f'Output File: {percentage_written:3.2f}%, Still Writing: {still_writing}')

            # Update the progress bar
            self.output_file_progress_bar.configure(value=percentage_written)

            if still_writing:
                # Continue writing the output file
                self.parent.after(1, self.write_output_file)
            else:
                # Emit the enable menu items event
                self.parent.event_generate(constants.ENABLE_MENU_ITEMS_EVENT)

                # Set the progress bar to 100%
                self.output_file_progress_bar.configure(value=100)

                # Change the cancel button to close
                self.cancel_button.configure(text='Close')

                # Show the conversion complete message
                messagebox.showinfo('Conversion Complete', 'The conversion has been completed successfully.')

    def cancel(self) -> None:
        """Cancels the conversion."""
        # Close the files
        self.converter.conversion_cancelled()

        # Set conversion cancelled to True
        self.conversion_cancelled = True

        # Emit the enable menu items event
        self.parent.event_generate(constants.ENABLE_MENU_ITEMS_EVENT)

        # Destroy the dialog
        self.destroy()

    def destroy(self) -> None:
        """Destroys the dialog."""
        # Release the dialog
        self.dialog.grab_release()

        # Destroy the dialog
        self.dialog.destroy()
