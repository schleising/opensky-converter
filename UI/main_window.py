"""Main window for the application.

This module contains the main window for the application.

Classes:
    MainWindow: The main window for the application.
"""

from pathlib import Path
import logging

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.simpledialog import _setup_dialog # type: ignore

from . import MappingDialog, ProgressDialog, ResetToDefaultsDialog

class MainWindow:
    def __init__(self, root: tk.Tk) -> None:
        """Creates the main window.

        Args:
            root (tk.Tk): The root window.
        """
        self.root = root

        # Set the window title
        self.root.title('Aircraft DB Converter')

        # Remove normal window decorations
        _setup_dialog(self.root)

        # Disable resizing the window
        self.root.resizable(False, False)

        # Create the main frame
        frame = ttk.Frame(self.root)
        frame.grid(column=0, row=0, padx=10, pady=10)

        # Create the labels
        current_file_label = ttk.Label(frame, text='Current File')
        current_file_label.grid(column=0, row=0, sticky=tk.W)

        new_file_label = ttk.Label(frame, text='New File')
        new_file_label.grid(column=0, row=1, sticky=tk.W)

        output_file_label = ttk.Label(frame, text='Output File')
        output_file_label.grid(column=0, row=2, sticky=tk.W)

        # Create the entry boxes
        self.current_file_text = tk.StringVar()
        self.current_file_path = Path()
        self.current_file_entry = ttk.Entry(frame, width=30, state='readonly', textvariable=self.current_file_text)
        self.current_file_entry.grid(column=1, row=0, sticky=tk.EW)

        self.new_file_text = tk.StringVar()
        self.new_file_path = Path()
        self.new_file_entry = ttk.Entry(frame, width=30, state='readonly', textvariable=self.new_file_text)
        self.new_file_entry.grid(column=1, row=1, sticky=tk.EW)

        self.output_file_text = tk.StringVar()
        self.output_file_path = Path()
        self.output_file_entry = ttk.Entry(frame, width=30, state='readonly', textvariable=self.output_file_text)
        self.output_file_entry.grid(column=1, row=2, sticky=tk.EW)

        # Create the buttons
        self.current_file_button = ttk.Button(frame, text='Select Filename', command=self.select_current_file)
        self.current_file_button.grid(column=2, row=0, sticky=tk.EW)

        self.new_file_button = ttk.Button(frame, text='Select Filename', command=self.select_new_file)
        self.new_file_button.grid(column=2, row=1, sticky=tk.EW)

        self.output_file_button = ttk.Button(frame, text='Select Filename', command=self.select_output_file, state=tk.DISABLED)
        self.output_file_button.grid(column=2, row=2, sticky=tk.EW)

        self.set_mappping_button = ttk.Button(frame, text='Set Mapping', state=tk.DISABLED, command=self.set_mapping)
        self.set_mappping_button.grid(column=2, row=3, sticky=tk.EW)

        self.convert_button = ttk.Button(frame, text='Convert', state=tk.DISABLED, command=self.convert)
        self.convert_button.grid(column=2, row=4, sticky=tk.EW)

        self.reset_to_defaults_button = ttk.Button(frame, text='Reset to Defaults', command=self.reset_to_defaults)
        self.reset_to_defaults_button.grid(column=0, columnspan=2, row=5, sticky='W')

        self.close_button = ttk.Button(frame, text='Close', command=self.root.destroy)
        self.close_button.grid(column=2, row=5, sticky=tk.EW)

        # Position the window
        self.root.geometry('+600+300')

        # Set the padding for all widgets
        for child in frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # Create the mapping dialog object
        self.mapping_dialog = MappingDialog(self.root)

        # Bind the mapping dialog events
        self.root.bind('<<MappingAccepted>>', self.mapping_accepted)
        self.root.bind('<<MappingRejected>>', self.mapping_rejected)

        # Log that the main window has been created
        logging.debug('Main window created')

    def check_enable_buttons(self) -> None:
        """Checks if the buttons should be enabled or disabled."""
        # Check if the current file and new file have been selected
        if self.current_file_path.is_file() and self.new_file_path.is_file():
            # Check if the current file and new file are the same
            if self.current_file_path != self.new_file_path:
                # Enable the output file button
                self.output_file_button.configure(state=tk.NORMAL)

                # Check if the output file has been selected
                if self.output_file_path.name:
                    # Check if the output file is the same as the current file or new file
                    if self.output_file_path != self.current_file_path and self.output_file_path != self.new_file_path:
                        # Enable the set mapping button
                        self.set_mappping_button.configure(state=tk.NORMAL)
                    else:
                        # Disable the set mapping button
                        self.set_mappping_button.configure(state=tk.DISABLED)
            else:
                # Disable the output file button
                self.output_file_button.configure(state=tk.DISABLED)

    def select_current_file(self) -> None:
        """Selects the current file."""
        # Get the filename
        filename = filedialog.askopenfilename()

        # Check if a filename was selected
        if filename:
            # Set the current file path
            self.current_file_path = Path(filename)

            # Set the current file text
            self.current_file_text.set(self.current_file_path.name)

            # Check if the buttons should be enabled or disabled
            self.check_enable_buttons()

    def select_new_file(self) -> None:
        """Selects the new file."""
        # Get the filename
        filename = filedialog.askopenfilename()

        # Check if a filename was selected
        if filename:
            # Set the new file path
            self.new_file_path = Path(filename)

            # Set the new file text
            self.new_file_text.set(self.new_file_path.name)

            # Check if the buttons should be enabled or disabled
            self.check_enable_buttons()

    def select_output_file(self) -> None:
        """Selects the output file."""
        # Get the filename
        filename = filedialog.asksaveasfilename(initialfile='IRCA.txt', defaultextension='.txt')

        # Check if a filename was selected
        if filename:
            # Set the output file path
            self.output_file_path = Path(filename)

            # Set the output file text
            self.output_file_text.set(self.output_file_path.name)

            # Check if the buttons should be enabled or disabled
            self.check_enable_buttons()

    def set_mapping(self) -> None:
        """Opens the set mapping dialog"""
        # Show the mapping dialog
        self.mapping_dialog.show(self.new_file_path)

    def mapping_accepted(self, _) -> None:
        """Enables the convert button when the mapping is accepted."""
        # Enable the convert button
        self.convert_button.configure(state=tk.NORMAL)

    def mapping_rejected(self, _) -> None:
        """Disables the convert button when the mapping is rejected."""
        # Disable the convert button
        self.convert_button.configure(state=tk.DISABLED)

    def convert(self) -> None:
        """Converts the current file to the new file."""
        if self.mapping_dialog.mapping is not None:
            ProgressDialog(self.root, self.current_file_path, self.new_file_path, self.output_file_path, self.mapping_dialog.mapping)
        else:
            messagebox.showerror('Error', 'No mapping has been set.')

    def reset_to_defaults(self) -> None:
        """Resets the current file and mapping to the defaults."""
        ResetToDefaultsDialog(self.root)
