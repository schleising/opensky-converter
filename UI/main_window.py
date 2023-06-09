"""Main window for the application.

This module contains the main window for the application.

Classes:
    MainWindow: The main window for the application.
"""

import shutil
import csv
from pathlib import Path
import logging
import webbrowser

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.simpledialog import _setup_dialog # type: ignore

from . import MappingDialog, ProgressDialog, ResetToDefaultsDialog

import constants

class MainWindow:
    """Creates the main window.

    Args:
        root (tk.Tk): The root window.
    """
    def __init__(self, root: tk.Tk) -> None:
        # Store the root window
        self.root = root

        # Create the icon
        photoimage = tk.PhotoImage(file=constants.ICON_FILE_PATH)

        # Set the icon
        self.root.wm_iconphoto(True, photoimage)

        # Set the window title
        self.root.title(constants.APPLICATION_NAME)

        # Set up the menu bar
        self.setup_menu_bar()

        # Bind enable menu items event
        self.root.bind(constants.ENABLE_MENU_ITEMS_EVENT, self.enable_menu_items)

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
        self.current_file_button = ttk.Button(frame, text='Select Current File', command=self.select_current_file)
        self.current_file_button.grid(column=2, row=0, sticky=tk.EW)

        self.new_file_button = ttk.Button(frame, text='Select New File', command=self.select_new_file)
        self.new_file_button.grid(column=2, row=1, sticky=tk.EW)

        self.output_file_button = ttk.Button(frame, text='Set Output Filename', command=self.select_output_file, state=tk.DISABLED)
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
        self.root.bind(constants.MAPPING_ACCEPTED_EVENT, self.mapping_accepted)
        self.root.bind(constants.MAPPING_REJECTED_EVENT, self.mapping_rejected)

        # Log that the main window has been created
        logging.debug('Main window created')

        # Set the default delimiters
        self.current_file_delimiter = constants.DEFAULT_CURRENT_FILE_DELIMITER
        self.new_file_delimiter = constants.DEFAULT_NEW_FILE_DELIMITER

        # Copy the Original IRCA Input file to the database folder if it doesn't exist
        if not Path(constants.DATABASE_PATH, constants.ORIGINAL_IRCA_INPUT_FILENAME).exists():
            # Create the database folder if it doesn't exist
            if not Path(constants.DATABASE_PATH).exists():
                Path(constants.DATABASE_PATH).mkdir(parents=True, exist_ok=True)

            # Log that the Original IRCA Input file is being copied
            logging.info('Unzipping Original IRCA Input file to database folder')

            # Unzip and copy the file
            shutil.unpack_archive(constants.ORIGINAL_IRCA_INPUT_FILE_PATH, constants.DATABASE_PATH)

        # Copy the default mapping file to the Aircraft DB Converter folder if it doesn't exist
        if not Path(constants.DEFAULT_MAPPING_PATH).exists():
            # Create the defaults path if it doesn't exist
            if not Path(constants.DEFAULTS_PATH).exists():
                Path(constants.DEFAULTS_PATH).mkdir(parents=True, exist_ok=True)

            # Log that the default mapping file is being copied
            logging.info('Unzipping default mapping file to Aircraft DB Converter defaults folder')

            # Unzip and copy the file
            shutil.unpack_archive(constants.ORIGINAL_MAPPING_PATH, constants.DEFAULTS_PATH)

    def setup_menu_bar(self) -> None:
        """Sets up the menu bar."""
        # Create the menu bar
        self.menu_bar = tk.Menu(self.root)

        # The menus need to be set up differently on macOS, so first create the macOS menu
        if self.root.tk.call('tk', 'windowingsystem') == constants.MACOS_SYSTEM:
            # Create the Apple menu, this is actually the menu named for the application on macOS
            self.apple_menu = tk.Menu(self.menu_bar, name='apple', tearoff=0)
            self.apple_menu.add_command(label='About', command=self.show_about_dialog)
            self.apple_menu.add_command(label='Documentation', command=self.open_documentation)

            # Add the menu to the menu bar
            self.menu_bar.add_cascade(menu=self.apple_menu)
        else:
            # Create the file menu
            self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
            self.file_menu.add_command(label='Quit', command=self.root.destroy)

            # Create the help menu
            self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
            self.help_menu.add_command(label='About', command=self.show_about_dialog)
            self.help_menu.add_command(label='Documentation', command=self.open_documentation)

            # Add the menus to the menu bar
            self.menu_bar.add_cascade(label='File', menu=self.file_menu)
            self.menu_bar.add_cascade(label='Help', menu=self.help_menu)

        # Set the menu bar
        self.root.configure(menu=self.menu_bar)

    def disable_menu_items(self) -> None:
        """Disables the menu items that should be disabled."""
        # Check if we are on macOS
        if self.root.tk.call('tk', 'windowingsystem') == constants.MACOS_SYSTEM:
            # Disable the menu items that should be disabled
            self.apple_menu.entryconfig('About', state=tk.DISABLED)
            self.apple_menu.entryconfig('Documentation', state=tk.DISABLED)
        else:
            # Disable the menu items that should be disabled
            self.menu_bar.entryconfig('File', state=tk.DISABLED)
            self.menu_bar.entryconfig('Help', state=tk.DISABLED)

    def enable_menu_items(self, _) -> None:
        """Enables the menu items that should be enabled."""
        # Check if we are on macOS
        if self.root.tk.call('tk', 'windowingsystem') == constants.MACOS_SYSTEM:
            # Enable the menu items that should be enabled
            self.apple_menu.entryconfig('About', state=tk.NORMAL)
            self.apple_menu.entryconfig('Documentation', state=tk.NORMAL)
        else:
            # Enable the menu items that should be enabled
            self.menu_bar.entryconfig('File', state=tk.NORMAL)
            self.menu_bar.entryconfig('Help', state=tk.NORMAL)

    def show_about_dialog(self) -> None:
        """Shows the about dialog."""
        # Open a simple dialog box with the about information
        messagebox.showinfo('About', f'{constants.APPLICATION_NAME}\n\nVersion {constants.VERSION}')

    def open_documentation(self) -> None:
        """Opens the documentation."""
        # Log that the documentation is being opened
        logging.debug('Opening documentation')

        # Get the path to the documentation
        docs_path = constants.DOCS_PATH.absolute().as_posix()

        # Log the documentation path
        logging.debug(f'Documentation path: {docs_path}')

        # Open the documentation
        webbrowser.open(f'file://{docs_path}', new=2, autoraise=True)

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
                        # Show an error message
                        messagebox.showerror('Error', 'The Output File cannot be the same as the Current File or New File\n\nPlease select a different Output Filename')

                        # Disable the set mapping button
                        self.set_mappping_button.configure(state=tk.DISABLED)
            else:
                # Show an error message
                messagebox.showerror('Error', 'The Current File and New File cannot be the same\n\nPlease select different files')

                # Disable the output file button
                self.output_file_button.configure(state=tk.DISABLED)
        else:
            # Disable the output file button
            self.output_file_button.configure(state=tk.DISABLED)

            # Disable the set mapping button
            self.set_mappping_button.configure(state=tk.DISABLED)

    def select_current_file(self) -> None:
        """Selects the current file."""
        # Get the filename
        filename = filedialog.askopenfilename(initialdir=constants.DATABASE_PATH, title='Select Current File', filetypes=(('Text Files', '*.txt'), ('All Files', '*.*')))

        # Check if a filename was selected
        if filename:
            # Check the dialect of the current file
            with open(filename, newline='', encoding='utf8') as csvfile:
                try:
                    # Try to determine the dialect of the current file
                    dialect = csv.Sniffer().sniff(csvfile.read(constants.SNIFFER_READ_SIZE))

                    # Set the current file delimiter
                    self.current_file_delimiter = dialect.delimiter
                except csv.Error:
                    # Log that the dialect of the current file could not be determined
                    logging.error(f'The dialect of the Current File {filename} could not be determined')

                    # Display a message box
                    messagebox.showerror('Error', 'The dialect of the Current File could not be determined.\n\nPlease select a different file.')

                    # Clear the filename
                    filename = ''
                except UnicodeDecodeError:
                    # Log that the current file does not look like a valid text file
                    logging.error(f'{filename} does not look like a valid text file')

                    # Display a message box
                    messagebox.showerror('Error', 'The Current File does not look like a valid text file\n\nPlease select a different file.')

                    # Clear the filename
                    filename = ''
                else:
                    # Check that the delimiter is a tab
                    if self.current_file_delimiter != constants.DEFAULT_CURRENT_FILE_DELIMITER:
                        # Log that the delimiter of the current file is not a tab
                        logging.error(f'The delimiter of the Current File {filename} is not a tab')

                        # Display a message box
                        messagebox.showerror('Error', 'The delimiter of the Current File is not a tab.\n\nPlease select a different file.')

                        # Clear the filename
                        filename = ''
                    # Check the field names in the current file match the field names in the default mapping
                    elif not self.check_field_names(filename):
                        # Display a message box
                        messagebox.showerror('Error', 'The field names in the Current File do not match the field names in the default mapping.\n\nPlease select a different file.')

                        # Log that the field names in the current file do not match the field names in the default mapping
                        logging.error(f'The field names in the current file {filename} do not match the field names in the default mapping')

                        # Clear the filename
                        filename = ''

            # Set the current file path
            self.current_file_path = Path(filename)

            # Set the current file text
            self.current_file_text.set(self.current_file_path.name)

            # Check if the buttons should be enabled or disabled
            self.check_enable_buttons()

    def check_field_names(self, filename: str) -> bool:
        """Checks the field names in the current file match the field names in the default mapping.

        Args:
            filename: The filename of the current file.

        Returns:
            True if the field names match, False otherwise.
        """
        # Open the current file
        with open(filename, 'r', encoding='utf-8', newline='') as current_file:
            # Create a dictionary reader
            reader = csv.DictReader(current_file, delimiter=self.current_file_delimiter)

            # Get the field names
            field_names = reader.fieldnames

            if field_names is None:
                # Return False
                return False

            for default_field_name in constants.ORIGINAL_IRCA_MAPPING.keys():
                # Check if the default field name is not in the field names
                if default_field_name not in field_names:
                    # Return False
                    return False
                
        # Return True
        return True

    def select_new_file(self) -> None:
        """Selects the new file."""
        # Get the filename
        filename = filedialog.askopenfilename(initialdir=constants.DATABASE_PATH, title='Select New File', filetypes=(('CSV Files', '*.csv'), ('All Files', '*.*')))

        # Check if a filename was selected
        if filename:
            # Check the dialect of the current file
            with open(filename, newline='', encoding='utf8') as csvfile:
                try:
                    # Try to determine the dialect of the current file
                    dialect = csv.Sniffer().sniff(csvfile.read(constants.SNIFFER_READ_SIZE))

                    # Set the current file delimiter
                    self.new_file_delimiter = dialect.delimiter
                except csv.Error:
                    # Log that the dialect of the current file could not be determined
                    logging.error(f'The dialect of the New File {filename} could not be determined')

                    # Display a message box
                    messagebox.showerror('Error', 'The dialect of the New File could not be determined.\n\nPlease select a different file.')

                    # Clear the filename
                    filename = ''
                except UnicodeDecodeError:
                    # Log that the new file does not look like a valid text file
                    logging.error(f'{filename} does not look like a valid text file')

                    # Display a message box
                    messagebox.showerror('Error', 'The New File does not look like a valid text file.\n\nPlease select a different file.')

                    # Clear the filename
                    filename = ''

            # Set the new file path
            self.new_file_path = Path(filename)

            # Set the new file text
            self.new_file_text.set(self.new_file_path.name)

            # Check if the buttons should be enabled or disabled
            self.check_enable_buttons()

    def select_output_file(self) -> None:
        """Selects the output file."""
        # Get the filename
        filename = filedialog.asksaveasfilename(initialfile='IRCA.txt', defaultextension='.txt', initialdir=constants.DATABASE_PATH, title='Select Output File', filetypes=(('Text Files', '*.txt'), ('All Files', '*.*')))

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
        self.mapping_dialog.show(self.new_file_path, self.new_file_delimiter)

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
            # Disable the menu items
            self.disable_menu_items()

            # Show the progress dialog
            ProgressDialog(
                self.root,
                self.current_file_path,
                self.current_file_delimiter,
                self.new_file_path,
                self.new_file_delimiter,
                self.output_file_path,
                self.mapping_dialog.mapping
            )
        else:
            # Display a message box
            messagebox.showerror('Error', 'No mapping has been set.')

            # Log that no mapping has been set
            logging.error('No mapping has been set')

    def reset_to_defaults(self) -> None:
        """Resets the current file and mapping to the defaults."""
        ResetToDefaultsDialog(self.root)
