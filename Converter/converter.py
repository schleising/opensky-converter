"""Merges the New File into the Current File and outputs the result to the Output File.

Classes:
    Converter: Merges the New File into the Current File and outputs the result to the Output File.
"""

import csv
import logging
from pathlib import Path
from typing import Dict, Tuple
from datetime import datetime, timedelta

import constants

class Converter:
    """Merges the New File into the Current File and outputs the result to the Output File.

    Args:
        current_file_path (Path): The existing aircraft database file.
        current_file_delimiter (str): The delimiter of the existing database file.
        new_file_path (Path): The file containing new data to be merged into the existing database.
        new_file_delimiter (str): The delimiter of the new file.
        output_file_path (Path): The file to output the merged data to.
        mapping (Dict[str, str]): The mapping of the new file's fieldnames to the current file's fieldnames.
    """
    def __init__(
            self,
            current_file_path: Path,
            current_file_delimiter: str,
            new_file_path: Path,
            new_file_delimiter: str,
            output_file_path: Path,
            mapping: Dict[str, str]
        ) -> None:
        # Store the file paths
        self.current_file_path = current_file_path
        self.current_file_delimiter = current_file_delimiter
        self.new_file_path = new_file_path
        self.new_file_delimiter = new_file_delimiter
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
        """Initialises the current file."""
        # Get the number of lines in the original file
        with open(self.current_file_path, 'r', encoding='utf8') as current_file:
            self.current_file_lines = len(current_file.readlines())

        # Open the current file
        self.current_file = open(self.current_file_path, 'r', encoding='utf-8', newline='')

        # Create a reader for the current file
        self.current_file_reader = csv.DictReader(self.current_file, delimiter=self.current_file_delimiter)

        # Initialise the number of lines read to 0
        self.lines_read = 0

    def read_current_file(self) -> Tuple[float, bool]:
        """Reads the current file.
        
        Returns:
            Tuple[float, bool]: The percentage of the current file read and whether the current file has been fully read.
            
        Notes:
            The current file is read into a dictionary. The key is the Mode S ID and the value is the row.
        """
        # Get the start time
        start_time = datetime.now()

        # Run for 100 milliseconds
        while datetime.now() - start_time < timedelta(milliseconds=constants.UI_REFRESH_TIME):
            # Check if the file is closed
            if self.current_file is None or self.current_file.closed:
                break

            # Try to read the next line
            try:
                # Get the next row
                row = next(self.current_file_reader)

                # Add the row to the dictionary
                if constants.MODE_S_ADDRESS_KEY in row:
                    self.current_file_data[row[constants.MODE_S_ADDRESS_KEY]] = row

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
        """Initialises the new file."""
        # Get the number of lines in the new file
        with open(self.new_file_path, 'r', encoding='utf8') as new_file:
            self.new_file_lines = len(new_file.readlines())

        # Open the new file
        self.new_file = open(self.new_file_path, 'r', encoding='utf-8', newline='')

        # Create a reader for the new file
        self.new_file_reader = csv.DictReader(self.new_file, delimiter=self.new_file_delimiter)

        # Initialise the number of lines read to 0
        self.lines_read = 0

    def merge_new_file(self) -> Tuple[float, bool]:
        """Merges the new file.
        
        Returns:
            Tuple[float, bool]: The percentage of the new file read and whether the new file has been fully read.

        Notes:
            The new file is merged into the current file. If the Mode S ID is not in the current file, the row is added to the current file. If the Mode S ID is in the current file, the row is updated with the new data.

            The Mode S ID is converted to uppercase before being used as a key.

            The Mode S ID is not in the mapping, an error is logged and the row is skipped.

            If the Mode S ID is not in the new file, an error is logged and the row is skipped.

            If the Mode S ID is not in the current file, the row is added to the current file.

            If the Mode S ID is in the current file, the row is updated with the new data.
        """
        # Get the start time
        start_time = datetime.now()

        # Run for 100 milliseconds
        while datetime.now() - start_time < timedelta(milliseconds=constants.UI_REFRESH_TIME):
            # Check if the file is closed
            if self.new_file is None or self.new_file.closed:
                break

            # Try to read the next line
            try:
                # Get the next row
                new_row = next(self.new_file_reader)

                # Ensure the Mode S ID is in uppercase
                new_row[self.mapping[constants.MODE_S_ADDRESS_KEY]] = new_row[self.mapping[constants.MODE_S_ADDRESS_KEY]].upper()

                # Get the Mode S ID
                mode_s_id = new_row[self.mapping[constants.MODE_S_ADDRESS_KEY]]

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
                        if new_field != constants.NO_MAPPING_STRING and new_row[new_field] != '':
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

    def initialise_output_file(self) -> None:
        """Initialises the output file."""
        # Open the output file
        self.output_file = open(self.output_file_path, 'w', encoding='utf-8', newline='')

        # Create the writer
        self.output_file_writer = csv.DictWriter(self.output_file, fieldnames=constants.ORIGINAL_IRCA_MAPPING.keys(), delimiter=constants.DEFAULT_OUTPUT_FILE_DELIMITER)

        # Write the header
        self.output_file_writer.writeheader()

        # Create a list of the rows to write
        self.current_file_data_iterator = iter(list(self.current_file_data.values()))

        # Initialise the number of lines written to 0
        self.lines_written = 0

    def write_output_file(self) -> Tuple[float, bool]:
        """Writes the output file.
        
        Returns:
            Tuple[float, bool]: The percentage of the output file written and whether the output file has been fully written.
            
            Notes:
                The output file is written to the output file path. The output file is written in the same format as the original IRCA file.
                
                The output file is written in chunks of 100 milliseconds. This is to ensure the UI is responsive.
                
                If the output file is closed, the function returns.
                
                If the output file is not closed, the next line is read from the output file. If the end of the file is reached, the output file is closed and the function returns.
                
                If the end of the file is not reached, the line is written to the output file and the number of lines written is incremented.
                
                The percentage of the output file written is calculated by dividing the number of lines written by the total number of lines in the output file.
                
                The function returns the percentage of the output file written and whether the output file has been fully written.
                
                The output file is fully written if the output file is closed.
                """
        # Get the start time
        start_time = datetime.now()

        # Run for 100 milliseconds
        while datetime.now() - start_time < timedelta(milliseconds=constants.UI_REFRESH_TIME):
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
