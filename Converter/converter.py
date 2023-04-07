import csv
from pathlib import Path
from typing import Dict, Tuple
from datetime import datetime, timedelta

REFRESH_TIME = 100 # The time in milliseconds to wait before refreshing the progress bars

class Converter:
    def __init__(self, current_file_path: Path, new_file_path: Path, output_file_path: Path, mapping: Dict[str, str]) -> None:
        """Merges the New File into the Current File and outputs the result to the Output File.

        Args:
            current_filename (Path): The existing aircraft database file.
            new_filename (Path): The file containing new data to be merged into the existing database.
            output_filename (Path): The file to output the merged data to.
            mapping (Dict[str, str]): The mapping of the new file's fieldnames to the current file's fieldnames.
        """
        self.current_file_path = current_file_path
        self.new_file_path = new_file_path
        self.output_file_path = output_file_path
        self.mapping = mapping

        self.current_file_lines = 0

        with open(self.new_file_path, 'r') as new_file:
            self.new_file_lines = len(new_file.readlines())

        # Open the current file
        self.current_file = open(self.current_file_path, 'r', encoding='utf-8', newline='')

        # Create a reader for the current file
        self.current_file_reader = csv.DictReader(self.current_file)

        # Open the new file
        self.new_file = open(self.new_file_path, 'r', encoding='utf-8', newline='')

        # Create a reader for the new file
        self.new_file_reader = csv.DictReader(self.new_file)

        # Open the output file
        self.output_file = open(self.output_file_path, 'w', encoding='utf-8', newline='')

        # Initialise an empty dictionary to store the current file's data
        self.current_file_data: Dict[str, Dict[str, str]] = {}

    def initialise_current_file(self) -> None:
        # Get the number of lines in the original file and the new file
        with open(self.current_file_path, 'r') as current_file:
            self.current_file_lines = len(current_file.readlines())

        # Initialise the number of lines read to 0
        self.lines_read = 0

    def read_current_file(self) -> Tuple[float, bool]:
        """Reads the current file."""

        # Get the start time
        start_time = datetime.now()

        # Run for 100 milliseconds
        while datetime.now() - start_time < timedelta(milliseconds=REFRESH_TIME):
            # Check if the file is closed
            if self.current_file.closed:
                break

            # Try to read the next line
            try:
                # Get the next row
                row = next(self.current_file_reader)

                # Add the row to the dictionary
                if row['icao24'] in row:
                    self.current_file_data[row['icao24']] = row

            except StopIteration:
                # Close the current file
                self.current_file.close()

                # Break out of the loop
                break

            except csv.Error:
                # Ignore this line
                pass

            # Increment the number of lines read
            self.lines_read += 1

        # Return the number of lines read
        return (self.lines_read / self.current_file_lines) * 100, not self.current_file.closed

    def merge_new_file(self) -> None:
        """Merges the new file."""
        pass

    def conversion_cancelled(self) -> None:
        """Called when the user cancels the conversion."""
        # Close the current file
        if not self.current_file.closed:
            self.current_file.close()

        # Close the new file
        if not self.new_file.closed:
            self.new_file.close()

        # Close the output file
        if not self.output_file.closed:
            self.output_file.close()
