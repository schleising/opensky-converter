REM Description: Build the application for distribution

REM Build the docs
mkdocs build

REM Build the application
pyinstaller ^
    --onedir ^
    --name AircraftDBConverter ^
    --windowed ^
    --add-data defaults:defaults ^
    --add-data site:site ^
    --add-binary resources/icon_512x512.png:resources ^
    -i resources/icon_512x512.png ^
    main.py
