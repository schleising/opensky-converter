# Main Window

This is the main window of the application. It is used to select the files to be merged, the output file, the mapping and start the conversion process.

The user can also reset the default Aircraft DB File and the default mapping by selecting the [Reset to Defaults](reset_to_defaults_dialog.md) button.

[![Main Window](../Design/Main%20Window.png)](../flowcharts/main_window.md)

Click image to see process flowchart

!!! info "File Names"
    - Current File is the file that is currently in use
    - New File is the file that is being merged into the Current File
    - Output File is the file that will be created

## Workflow

1. Select the Current File
2. Select the New File

    !!! info
        Once both files are selected the Output File button will be enabled
    !!! warning
        - The Current File must be a tab separated file in the IRCA format (This can be the supplied `Original IRCA File.txt` file or a file created by the application)
        - The application will attempt to detect the format (dialect) of the New File, it does not have to be in the IRCA format. The headings from this file will be used to populate the dropdowns in the [Mapping Dialog](mapping_dialog.md)

        The application will not allow the user to continue if either file is not in the correct format

3. Select the Output Filename

    !!! info
        Once all files are selected the Set Mapping button will be enabled
    !!! warning
        The three files must be different, the application will not allow the user to continue if any files are the same

4. Select the Set Mapping button to open the [Mapping Dialog](mapping_dialog.md)

    !!! info
        - If the mapping was accepted the Convert button will be enabled
        - If the mapping was cancelled the Convert button will be disabled

5. Select Convert to open the [Progress Dialog](progress_dialog.md) and start the conversion process

    !!! info
        The Output File will be a tab separated file in the IRCA format, this file can be used as the Current File in the next merge

6. Select Close to close the application

!!! info
    Select Reset to Defaults to open the [Reset to Defaults Dialog](reset_to_defaults_dialog.md)