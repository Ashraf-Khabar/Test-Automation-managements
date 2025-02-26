import os
from PyQt6.QtWidgets import QFileDialog, QListWidgetItem
from PyQt6.QtCore import Qt

class FileManager:
    def __init__(self, parent):
        self.parent = parent
        self.test_directory = ""
        self.output_directory = ""

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self.parent, "Sélectionner un dossier")
        if dir_path:
            self.test_directory = dir_path
            self.parent.label.setText(f"Sélectionné : {dir_path}")
            self.output_directory = os.path.join(dir_path, "Results")
            os.makedirs(self.output_directory, exist_ok=True)
            self.load_tests()

    def select_output_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self.parent, "Sélectionner un dossier de résultats")
        if dir_path:
            self.output_directory = dir_path
            self.parent.fileLabel.setText(f"Résultats enregistrés dans : {dir_path}")

    def load_tests(self):
        self.parent.testList.clear()
        if self.test_directory:
            for file in os.listdir(self.test_directory):
                if file.endswith(".robot"):
                    item = QListWidgetItem(file)
                    item.setCheckState(Qt.CheckState.Unchecked)
                    self.parent.testList.addItem(item)
