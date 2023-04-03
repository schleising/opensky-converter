"""Contains the mapping dialog class.

This module contains the mapping dialog class, which is used to map the fields in the new file to the fields in the IRCA file.

Classes:
    MappingDialog: The mapping dialog class.
"""


import csv
import json
from pathlib import Path
from typing import Dict

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from .constants import ORIGINAL_IRCA_MAPPING

class MappingDialog():
    def __init__(self, parent: tk.Tk):
        """Creates the mapping dialog.

        Args:
            parent (tk.Tk): The parent window.
        """
        # Store the parent window
        self.parent = parent

        # Set the path to the default mapping file
        self.default_mapping_path = Path('defaults/default_mapping.json')

        # Initailise the mapping dictionary to None
        self.mapping: Dict[str, str] | None = None

    def show(self, new_file_path: Path) -> None:
        """Shows the mapping dialog.

        Args:
            new_file_path (Path): The path to the new file.
        """

        # Create the dialog
        self.dialog = tk.Toplevel(self.parent)

        # Set the title
        self.dialog.title('Map Fields')

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

            # Iniialise the last row counter
            last_row = 0

            # Read the default mapping file, using the original mapping if the file doesn't exist
            if self.default_mapping_path.is_file():
                with self.default_mapping_path.open('r', encoding='utf8') as default_mapping_file:
                    self.irca_mapping = json.load(default_mapping_file)
            else:
                self.irca_mapping = ORIGINAL_IRCA_MAPPING

            # Create the labels and comboboxes
            for i, (field, mapping) in enumerate(self.irca_mapping.items()):
                # Calculate the label column
                label_column = (i % 2) * 2

                # Create the label
                label = ttk.Label(frame, text=field)
                label.grid(row=i // 2, column=label_column, sticky=tk.W)

                # Calculate the combobox column
                combobox_column = ((i % 2) * 2) + 1

                # Create the combobox
                self.combobox_dict[field] = tk.StringVar(value=mapping)
                combobox = ttk.Combobox(frame, values=fieldnames, state='readonly', textvariable=self.combobox_dict[field])
                combobox.grid(row=i // 2, column=combobox_column, sticky=tk.EW)
                combobox.bind('<<ComboboxSelected>>', lambda event: event.widget.selection_clear())

                # Update the last row counter
                last_row = i // 2

            # Create the buttons
            save_as_default_button = ttk.Button(frame, text='Save as Default', command=self.save_as_default)
            save_as_default_button.grid(row=last_row + 1, column=3, sticky=tk.EW)

            accept_mapping_button = ttk.Button(frame, text='Accept Mapping', command=self.mapping_accepted)
            accept_mapping_button.grid(row=last_row + 2, column=3, sticky=tk.EW)

            cancel_button = ttk.Button(frame, text='Cancel', command=self.mapping_rejected)
            cancel_button.grid(row=last_row + 3, column=3, sticky=tk.EW)

            # Apply padding to all children
            for child in frame.winfo_children():
                child.grid_configure(padx=5, pady=5)

            # Set the dialog to be transient
            self.dialog.transient(self.parent)

            # Set the dialog to be modal
            self.dialog.grab_set()

        else:
            # If there are no fieldnames, show an error message
            messagebox.showerror('Error', 'No fields found in new file')

    def save_as_default(self):
        """Handles the save as default button being clicked.
        """
        # Get the new mapping
        new_mapping = {field: mapping.get() for field, mapping in self.combobox_dict.items()}

        # Create the defaults directory if it doesn't exist
        self.default_mapping_path.parent.mkdir(parents=True, exist_ok=True)

        # Save the new mapping
        with self.default_mapping_path.open('w', encoding='utf8') as default_mapping_file:
            json.dump(new_mapping, default_mapping_file, indent=2)

        # Show a success message
        messagebox.showinfo('Success', 'Default mapping saved')

    def mapping_accepted(self):
        """Handles the mapping being accepted.
        """
        # Get the new mapping
        self.mapping = {field: mapping.get() for field, mapping in self.combobox_dict.items()}

        # Generate the mapping accepted event
        self.parent.event_generate('<<MappingAccepted>>', when='tail')

        # Close the dialog
        self.close_dialog()

    def mapping_rejected(self):
        """Handles the mapping being rejected.
        """
        # Generate the mapping rejected event
        self.parent.event_generate('<<MappingRejected>>', when='tail')

        # Close the dialog
        self.close_dialog()

    def close_dialog(self):
        """Closes the dialog.
        """
        # Release the parent window
        self.dialog.grab_release()

        # Destroy the dialog
        self.dialog.destroy()
