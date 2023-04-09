## Unzip Files
Unzip the files to any folder which you have write access to and run the `AircraftDBConverter.exe` file.

## First Run
The first time you run the application it will create a folder called `AircraftDBConverter` in the currently logged in user's home folder.

This folder will contain two other folders, `database` and `defaults`,

- The `database` folder will contain the Aircraft DB File `Original IRCA File.txt`
- The `defaults` folder will contain the default mapping file `default_mapping.json`

It will also contain the log file `aircraft-db-converter-log.txt`.

!!! warning
    These files should not be modified by the user, doing so may cause the application to fail.
    
    If the files have become corrupted or are missing, they can be restored using the [Reset to Defaults Dialog](reset_to_defaults_dialog.md).

Once the application has started you will see the [Main Window](main_window.md).