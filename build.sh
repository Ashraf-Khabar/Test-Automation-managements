#!/bin/bash

EXEC_NAME="RobotTestRunner"

if ! command -v pyinstaller &> /dev/null; then
    pip install --upgrade pyinstaller
fi

echo "Nettoyage des anciens fichiers..."
rm -rf build dist "${EXEC_NAME}.spec"

if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Linux"
    SEP=":"
else
    echo "Windows"
    SEP=";"
fi

# pyinstaller --noconfirm --onefile --windowed --name "$EXEC_NAME" --add-data "$(pwd)/style/style.qss${SEP}style/" --add-data "$(pwd)/images/logo.png${SEP}images/" main.py

pyinstaller --noconfirm --onefile --windowed --name RobotTestRunner --add-data "./style/style.qss${SEP}style" --add-data "./images/*${SEP}images" --icon=images/Logo_exe_grand.ico main.py

if [ -f "dist/$EXEC_NAME" ] || [ -f "dist/$EXEC_NAME.exe" ]; then
    echo "L'exécutable a été généré avec succès dans le dossier 'dist/'"
else
    echo "Erreur lors de la génération de l'exécutable"
    exit 1
fi
