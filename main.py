import logging

import tkinter as tk

from UI import MainWindow

import constants

if __name__ == '__main__':
    # Set up the base path if it doesn't exist
    constants.HOME_PATH.mkdir(parents=True, exist_ok=True)

    # Set up logging
    logging.basicConfig(level=logging.INFO, filename=constants.LOG_PATH, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    # Log that the program has started
    logging.debug('Application Started')

    # Create the root window
    root = tk.Tk()

    # Create the main window
    MainWindow(root)

    # Start the main loop
    root.mainloop()
