#!/bin/bash

EXEC_NAME="RobotTestRunner"

if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller n'est pas installé. Installation en cours..."
    pip install --upgrade pyinstaller
fi

echo "Nettoyage des anciens fichiers..."
rm -rf build dist "${EXEC_NAME}.spec"

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    SEP=":"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    SEP=":"
else
    # Windows by WSL
    SEP=";"
fi

echo "Génération de l'exécutable..."
pyinstaller --onefile --add-data "images/Logo.png;images" --add-data "style/style.qss;style" --icon=images/Logo.ico main.py


if [ -f "dist/$EXEC_NAME" ] || [ -f "dist/$EXEC_NAME.exe" ]; then
    echo "L'exécutable a été généré avec succès dans le dossier 'dist/'"
else
    echo "Erreur lors de la génération de l'exécutable"
    exit 1
fi