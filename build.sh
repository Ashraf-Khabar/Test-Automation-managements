#!/bin/bash

EXEC_NAME="RobotTestRunner"

if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller n'est pas installé. Installation en cours..."
    pip install pyinstaller
fi

rm -rf build dist ${EXEC_NAME}.spec

pyinstaller --noconfirm --onefile --windowed \
    --name "$EXEC_NAME" \
    --add-data "style/style.qss:style" \
    --add-data "image copy.png:." \
    main.py 