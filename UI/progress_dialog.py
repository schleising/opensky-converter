"""Creates a progress dialog for the user to see the progress of the conversion.
"""

import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import _setup_dialog # type: ignore

class ProgressDialog:
    def __init__(self, parent: tk.Tk) -> None:
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
        # _setup_dialog(self.dialog)

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

    def update(self, value: int) -> None:
        """Updates the progress bar.

        Args:
            value (int): The value to set the progress bar to.
        """
        # self.progress_bar['value'] = value
        pass

    def cancel(self) -> None:
        """Cancels the conversion."""
        # Destroy the dialog
        self.destroy()

    def destroy(self) -> None:
        """Destroys the dialog."""
        # Release the dialog
        self.dialog.grab_release()

        # Destroy the dialog
        self.dialog.destroy()
