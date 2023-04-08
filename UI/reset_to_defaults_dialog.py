"""Dialog to reset the settings to defaults."""

import json
import logging
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.simpledialog import _setup_dialog # type: ignore

from .constants import ORIGINAL_IRCA_MAPPING, DEFAULT_MAPPING_PATH

class ResetToDefaultsDialog:
    def __init__(self, parent: tk.Tk) -> None:
        """Creates the reset to default dialog."""
        # Store the parent window
        self.parent = parent

        # Create the dialog
        self.dialog = tk.Toplevel(self.parent)
              
        # Set the title
        self.dialog.title('Reset to Defaults')
        
        # Remove normal window decorations
        _setup_dialog(self.dialog)

        # Disable resizing the window
        self.dialog.resizable(False, False)

        # Create a frame to hold the widgets
        frame = ttk.Frame(self.dialog)
        frame.grid(column=0, row=0, padx=10, pady=10)

        # Create the checkboxes
        self.current_file_checkbox_var = tk.BooleanVar(value=False)
        current_file_checkbox = ttk.Checkbutton(frame, text='Reset Current File', variable=self.current_file_checkbox_var, command=self.enable_reset_button)
        current_file_checkbox.grid(column=0, columnspan=2, row=0, sticky=tk.W)

        self.mapping_checkbox_var = tk.BooleanVar(value=False)
        mapping_checkbox = ttk.Checkbutton(frame, text='Reset Mapping', variable=self.mapping_checkbox_var, command=self.enable_reset_button)
        mapping_checkbox.grid(column=0, columnspan=2, row=1, sticky=tk.W)

        # Create the buttons
        cancel_button = ttk.Button(frame, text='Cancel', command=self.cancel)
        cancel_button.grid(column=0, row=2, sticky=tk.EW)

        self.reset_button = ttk.Button(frame, text='Reset', command=self.reset)
        self.reset_button.grid(column=1, row=2, sticky=tk.EW)
        self.reset_button.configure(state=tk.DISABLED)

        # Add padding to the children
        for child in frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # Set the main window to be transient
        self.dialog.transient(self.parent)

        # Wait for the dialog to be visible
        self.dialog.wait_visibility()

        # Set the dialog to be modal
        self.dialog.grab_set()

        # Log the creation of the dialog
        logging.debug('Created reset to default dialog')

    def enable_reset_button(self) -> None:
        """Enables the reset button if at least one checkbox is checked."""
        if self.current_file_checkbox_var.get() or self.mapping_checkbox_var.get():
            self.reset_button.configure(state=tk.NORMAL)
        else:
            self.reset_button.configure(state=tk.DISABLED)

    def cancel(self) -> None:
        """Closes the dialog."""
        logging.debug('Closing reset to default dialog')

        # Release the dialog
        self.dialog.grab_release()

        # Destroy the dialog
        self.dialog.destroy()

    def reset(self) -> None:
        """Resets the settings."""
        # Reset the current file
        if self.current_file_checkbox_var.get():
            # Log that the current file has been reset
            logging.info('Resetting current file')

        # Reset the mapping
        if self.mapping_checkbox_var.get():
            # Log that the mapping has been reset
            logging.info('Resetting mapping')

            # Create the defaults directory if it doesn't exist
            DEFAULT_MAPPING_PATH.parent.mkdir(parents=True, exist_ok=True)

            # Save the new mapping
            with DEFAULT_MAPPING_PATH.open('w', encoding='utf8') as default_mapping_file:
                json.dump(ORIGINAL_IRCA_MAPPING, default_mapping_file, indent=2)

            # Show a success message
            messagebox.showinfo('Success', 'Default mapping reset')

        # Release the dialog
        self.dialog.grab_release()

        # Destroy the dialog
        self.dialog.destroy()
