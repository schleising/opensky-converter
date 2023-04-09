#!/bin/zsh

# Build the documentation
mkdocs build

# Generate the executable
pyinstaller \
    --onedir \
    --name AircraftDBConverter \
    --windowed \
    --add-data defaults:defaults \
    --add-data site:site \
    --add-binary resources/icon_512x512.png:resources \
    -i resources/icon_512x512.png \
    main.py
