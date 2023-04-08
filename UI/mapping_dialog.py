"""Contains the mapping dialog class.

This module contains the mapping dialog class, which is used to map the fields in the new file to the fields in the IRCA file.

Classes:
    MappingDialog: The mapping dialog class.
"""


import csv
import json
from pathlib import Path
from typing import Dict, Union
import logging

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import _setup_dialog # type: ignore

from .constants import ORIGINAL_IRCA_MAPPING, DEFAULT_MAPPING_PATH, NO_MAPPING_STRING, MODE_S_ADDRESS_KEY

class MappingDialog:
    def __init__(self, parent: tk.Tk) -> None:
        """Creates the mapping dialog.

        Args:
            parent (tk.Tk): The parent window.
        """
        # Store the parent window
        self.parent = parent

        # Initailise the mapping dictionary to None
        self.mapping: Union[Dict[str, str], None] = None

    def show(self, new_file_path: Path) -> None:
        """Shows the mapping dialog.

        Args:
            new_file_path (Path): The path to the new file.
        """

        # Create the dialog
        self.dialog = tk.Toplevel(self.parent)

        # Set the title
        self.dialog.title('Map Fields')

        # Remove normal window decorations
        _setup_dialog(self.dialog)

        # Create an empty dictionary to store the combobox variables
        self.combobox_dict: Dict[str, tk.StringVar] = {}

        # Read the fieldnames from the new file
        with new_file_path.open('r', encoding='utf8', newline='') as new_file:
            reader = csv.DictReader(new_file)

            self.fieldnames = reader.fieldnames

        # If there are fieldnames, create the dialog
        if self.fieldnames:
            # Create the main frame
            frame = ttk.Frame(self.dialog)
            frame.grid(column=0, row=0, padx=10, pady=10)

            # Get the fieldnames as a list
            fieldnames = list(self.fieldnames)

            # Add Do not Map to the start of the list
            fieldnames.insert(0, NO_MAPPING_STRING)

            # Iniialise the last row counter
            last_row = 0

            # Read the default mapping file, using the original mapping if the file doesn't exist
            if DEFAULT_MAPPING_PATH.is_file():
                with DEFAULT_MAPPING_PATH.open('r', encoding='utf8') as default_mapping_file:
                    self.irca_mapping = json.load(default_mapping_file)
            else:
                self.irca_mapping = ORIGINAL_IRCA_MAPPING

            # Create the labels and comboboxes
            for i, (field, mapping) in enumerate(self.irca_mapping.items()):
                # Calculate the label column
                label_column = (i % 3) * 2

                # Create the label
                label = ttk.Label(frame, text=field)
                label.grid(row=i // 3, column=label_column, sticky=tk.W)

                # Calculate the combobox column
                combobox_column = ((i % 3) * 2) + 1

                # Create the combobox
                self.combobox_dict[field] = tk.StringVar(value=mapping)
                combobox = ttk.Combobox(frame, values=fieldnames, state='readonly', textvariable=self.combobox_dict[field])
                combobox.grid(row=i // 3, column=combobox_column, sticky=tk.EW)
                combobox.bind('<<ComboboxSelected>>', lambda event: event.widget.selection_clear())

                # Update the last row counter
                last_row = i // 2

            # Create the buttons
            accept_mapping_button = ttk.Button(frame, text='Accept Mapping', command=self.mapping_accepted)
            accept_mapping_button.grid(row=last_row + 1, column=5, sticky=tk.EW)

            save_as_default_button = ttk.Button(frame, text='Save as Default', command=self.save_as_default)
            save_as_default_button.grid(row=last_row + 2, column=0, columnspan=2, sticky=tk.W)

            cancel_button = ttk.Button(frame, text='Cancel', command=self.mapping_rejected)
            cancel_button.grid(row=last_row + 2, column=5, sticky=tk.EW)

            # Apply padding to all children
            for child in frame.winfo_children():
                child.grid_configure(padx=5, pady=5)

            # Set the dialog to be transient
            self.dialog.transient(self.parent)

            # Wait for the dialog to be visible
            self.dialog.wait_visibility()

            # Set the dialog to be modal
            self.dialog.grab_set()

            # Disable the parent window
            self.dialog.wait_window(self.dialog)

            # Log the dialog being shown
            logging.debug('Mapping dialog shown')

        else:
            # If there are no fieldnames, show an error message
            messagebox.showerror('Error', 'No fields found in new file')

            # Log the error
            logging.error(f'No fields found in new file {new_file_path.name}')

    def save_as_default(self) -> None:
        """Handles the save as default button being clicked.
        """
        # Check if the mapping is valid
        if self.check_mode_s_mapped():
            # Get the new mapping
            new_mapping = {field: mapping.get() for field, mapping in self.combobox_dict.items()}

            # Create the defaults directory if it doesn't exist
            DEFAULT_MAPPING_PATH.parent.mkdir(parents=True, exist_ok=True)

            # Save the new mapping
            with DEFAULT_MAPPING_PATH.open('w', encoding='utf8') as default_mapping_file:
                json.dump(new_mapping, default_mapping_file, indent=2)

            # Show a success message
            messagebox.showinfo('Success', 'Default mapping saved')

    def mapping_accepted(self) -> None:
        """Handles the mapping being accepted.
        """
        # Check if the mapping is valid
        if self.check_mode_s_mapped():
            # Get the new mapping
            self.mapping = {field: mapping.get() for field, mapping in self.combobox_dict.items()}

            # Generate the mapping accepted event
            self.parent.event_generate('<<MappingAccepted>>', when='tail')

            # Close the dialog
            self.close_dialog()

    def check_mode_s_mapped(self) -> bool:
        """Checks if the mapping is valid.

        Returns:
            bool: True if the mapping is valid, False otherwise.
        """
        # Check if the Mode S field is mapped
        if self.combobox_dict[MODE_S_ADDRESS_KEY].get() == NO_MAPPING_STRING:
            # If it isn't, show an error message
            messagebox.showerror('Error', 'ModeSCode field must be mapped')

            # Log the error
            logging.error('ModeSCode field must be mapped')

            # Return False
            return False

        # Return True
        return True

    def mapping_rejected(self) -> None:
        """Handles the mapping being rejected.
        """
        # Generate the mapping rejected event
        self.parent.event_generate('<<MappingRejected>>', when='tail')

        # Close the dialog
        self.close_dialog()

    def close_dialog(self) -> None:
        """Closes the dialog.
        """
        # Release the parent window
        self.dialog.grab_release()

        # Destroy the dialog
        self.dialog.destroy()
