# OpenSky Converter

## User Guide

### Main Window
Click Image to see flowchart

[![Main Window](Design/Main%20Window.png)](main_window.md)

!!! info "File Names"
    - Current File is the file that is currently in use
    - New File is the file that is being merged into the Current File
    - Output File is the file that will be created

1. Select the Current File
2. Select the New File
3. Select the Output File
    - Once all files are selected the Set Mapping button will be enabled
4. Select the Set Mapping button to open the Mapping Dialog

### Mapping Dialog
Click image to see flowchart

[![Mapping Dialog](Design/Mapping%20Dialog.png)](mapping_dialog.md)

5. Map the fields from the New File to the Current File
6. The currently selected mapping can be saved as the default mapping
7. Selecting Accept Mapping will close the dialog and enable the Convert button
    - Selecting Cancel will close the dialog keeping the Convert button disabled
8. Select Convert to open the Progress Dialog and start the conversion process

### Progress Dialog
Click image to see flowchart

[![Progress Dialog](Design/Progress%20Dialog.png)](conversion_process.md)

While conversion is in progress selecting cancel at any time will stop the conversion process and close the Progress Dialog

### Reset to Defaults Dialog
Click image to see flowchart

[![Reset to Defaults](Design/Reset%20to%20Default%20Dialog.png)](reset_to_defaults.md)

Selecting Reset to Defaults will open the Reset to Defaults Dialog

- Choose whether to reset the Aircraft DB File, the Default Mapping, or both
    - Selecting Reset will close the dialog and reset the selected items
    - Selecting Cancel will close the dialog without resetting anything
