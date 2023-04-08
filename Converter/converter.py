import csv
import logging
from pathlib import Path
from typing import Dict, Tuple
from datetime import datetime, timedelta

from UI.constants import MODE_S_ADDRESS_KEY, UI_REFRESH_TIME, NO_MAPPING_STRING

class Converter:
    def __init__(self, current_file_path: Path, new_file_path: Path, output_file_path: Path, mapping: Dict[str, str]) -> None:
        """Merges the New File into the Current File and outputs the result to the Output File.

        Args:
            current_file_path (Path): The existing aircraft database file.
            new_file_path (Path): The file containing new data to be merged into the existing database.
            output_file_path (Path): The file to output the merged data to.
            mapping (Dict[str, str]): The mapping of the new file's fieldnames to the current file's fieldnames.
        """
        # Store the file paths
        self.current_file_path = current_file_path
        self.new_file_path = new_file_path
        self.output_file_path = output_file_path

        # Store the mapping
        self.mapping = mapping

        # Initialise an empty dictionary to store the current file's data
        self.current_file_data: Dict[str, Dict[str, str]] = {}

        # Initialise the file pointers
        self.current_file = None
        self.new_file = None
        self.output_file = None

    def initialise_current_file(self) -> None:
        # Get the number of lines in the original file
        with open(self.current_file_path, 'r') as current_file:
            self.current_file_lines = len(current_file.readlines())

        # Open the current file
        self.current_file = open(self.current_file_path, 'r', encoding='utf-8', newline='')

        # Create a reader for the current file
        self.current_file_reader = csv.DictReader(self.current_file, delimiter=';')

        # Initialise the number of lines read to 0
        self.lines_read = 0

    def read_current_file(self) -> Tuple[float, bool]:
        """Reads the current file."""

        # Get the start time
        start_time = datetime.now()

        # Run for 100 milliseconds
        while datetime.now() - start_time < timedelta(milliseconds=UI_REFRESH_TIME):
            # Check if the file is closed
            if self.current_file is None or self.current_file.closed:
                break

            # Try to read the next line
            try:
                # Get the next row
                row = next(self.current_file_reader)

                # Add the row to the dictionary
                if MODE_S_ADDRESS_KEY in row:
                    self.current_file_data[row[MODE_S_ADDRESS_KEY]] = row

            except StopIteration:
                # Close the current file
                self.current_file.close()

                # Break out of the loop
                break

            except csv.Error:
                # Log the error and ignore this line
                logging.error('Error reading line %s of %s', self.lines_read, self.current_file_path)

            # Increment the number of lines read
            self.lines_read += 1

        # Return the number of lines read
        return (self.lines_read / self.current_file_lines) * 100, True if self.current_file is None else not self.current_file.closed
    
    def initialise_new_file(self) -> None:
        # Get the number of lines in the new file
        with open(self.new_file_path, 'r') as new_file:
            self.new_file_lines = len(new_file.readlines())

        # Open the new file
        self.new_file = open(self.new_file_path, 'r', encoding='utf-8', newline='')

        # Create a reader for the new file
        self.new_file_reader = csv.DictReader(self.new_file)

        # Initialise the number of lines read to 0
        self.lines_read = 0

    def merge_new_file(self) -> Tuple[float, bool]:
        """Merges the new file."""
        # Get the start time
        start_time = datetime.now()

        # Run for 100 milliseconds
        while datetime.now() - start_time < timedelta(milliseconds=UI_REFRESH_TIME):
            # Check if the file is closed
            if self.new_file is None or self.new_file.closed:
                break

            # Try to read the next line
            try:
                # Get the next row
                new_row = next(self.new_file_reader)

                # Ensure the Mode S ID is in uppercase
                new_row[self.mapping[MODE_S_ADDRESS_KEY]] = new_row[self.mapping[MODE_S_ADDRESS_KEY]].upper()

                # Get the Mode S ID
                mode_s_id = new_row[self.mapping[MODE_S_ADDRESS_KEY]]

                # Ensure there is actually a value in the Mode S ID
                if mode_s_id != '':
                    # Check if the row is in the current file
                    if mode_s_id not in self.current_file_data:
                        # Add the row to the current file
                        self.current_file_data[mode_s_id] = {}

                    # Merge the new row into the current row
                    for irca_field, new_field in self.mapping.items():
                        # Check if the field is in the current row
                        if irca_field not in self.current_file_data[mode_s_id]:
                            # Add the field to the current row
                            self.current_file_data[mode_s_id][irca_field] = ''

                        # Check if data from the new row should overwrite the data in the current row
                        if new_field != NO_MAPPING_STRING and new_row[new_field] != '':
                            # Overwrite the data in the current row
                            self.current_file_data[mode_s_id][irca_field] = new_row[new_field]

            except StopIteration:
                # Close the new file
                self.new_file.close()

                # Break out of the loop
                break

            except csv.Error:
                # Ignore this line, log the error
                logging.error(f'Error reading line {self.lines_read} of {self.new_file_path}')

            # Increment the number of lines read
            self.lines_read += 1

        # Return the number of lines read
        return (self.lines_read / self.new_file_lines) * 100, True if self.new_file is None else not self.new_file.closed

    def initialise_output_file(self) -> bool:
        # Open the output file
        self.output_file = open(self.output_file_path, 'w', encoding='utf-8', newline='')

        # Create a writer for the output file
        if self.current_file_reader.fieldnames is not None:
            self.output_file_writer = csv.DictWriter(self.output_file, fieldnames=self.current_file_reader.fieldnames)

            # Write the header
            self.output_file_writer.writeheader()

            # Create a list of the rows to write
            self.current_file_data_iterator = iter(list(self.current_file_data.values()))

            # Initialise the number of lines written to 0
            self.lines_written = 0

            # Return True
            return True
        else:
            # Return False
            return False

    def write_output_file(self) -> Tuple[float, bool]:
        """Writes the output file."""
        # Get the start time
        start_time = datetime.now()

        # Run for 100 milliseconds
        while datetime.now() - start_time < timedelta(milliseconds=UI_REFRESH_TIME):
            # Check if the file is closed
            if self.output_file is None or self.output_file.closed:
                break

            # Try to read the next line
            try:
                # Get the next row
                row = next(self.current_file_data_iterator)

            except StopIteration:
                # Close the output file
                self.output_file.close()

                # Break out of the loop
                break

            # Write the line to the output file
            self.output_file_writer.writerow(row)

            # Increment the number of lines written
            self.lines_written += 1

        # Return the number of lines written
        return (self.lines_written / len(self.current_file_data)) * 100, True if self.output_file is None else not self.output_file.closed

    def conversion_cancelled(self) -> None:
        """Called when the user cancels the conversion."""
        # Close the current file
        if self.current_file is not None and not self.current_file.closed:
            self.current_file.close()

        # Close the new file
        if self.new_file is not None and not self.new_file.closed:
            self.new_file.close()

        # Close the output file
        if self.output_file is not None and not self.output_file.closed:
            self.output_file.close()
