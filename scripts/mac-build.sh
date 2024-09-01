#!/bin/bash

# Pfade
ICON_PATH="../app/image/MineMetrics.icns"
SCRIPT_PATH="../app/main.py"
DIST_PATH="../dist"
BUILD_PATH="../build"
SPEC_PATH="../spec"
PKG_PATH="../pkg"  # Pfad, wo das .pkg gespeichert werden soll
APP_NAME="MineMetrics"    # Name der App
VERSION="1.0.0 Beta"           # Version der App

# Entferne vorherige Builds
rm -rf "$DIST_PATH"
rm -rf "$BUILD_PATH"
rm -rf "$SPEC_PATH"
rm -rf "$PKG_PATH"

# Erstelle das neue Build
pyinstaller --onefile --windowed --icon="$ICON_PATH" --distpath "$DIST_PATH" --workpath "$BUILD_PATH" --specpath "$SPEC_PATH" "$SCRIPT_PATH"

# Erstelle den Ordner für die .pkg Datei
mkdir -p "$PKG_PATH"

# Erstelle ein .app-Bundle, falls PyInstaller nur eine ausführbare Datei erstellt
#APP_BUNDLE="$DIST_PATH/main.app"
#mkdir -p "$APP_BUNDLE/Contents/MacOS"
#mv "$DIST_PATH/$APP_NAME" "$APP_BUNDLE/Contents/MacOS/"

# Erstellen Sie das .pkg Installationspaket, das in den Applications-Ordner installiert
#pkgbuild --root "$DIST_PATH" --identifier "com.umutac.$APP_NAME" --version "$VERSION" --install-location "/Applications" "$PKG_PATH/$APP_NAME-$VERSION.pkg"