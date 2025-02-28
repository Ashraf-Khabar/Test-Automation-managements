import os
from PyQt6.QtWidgets import QFileDialog

class FileManager:
    def __init__(self, parent):
        self.parent = parent

    def select_directory(self):
        """Ouvre une boîte de dialogue pour sélectionner un dossier."""
        dir_path = QFileDialog.getExistingDirectory(self.parent, "Sélectionner un dossier")
        return dir_path

    def select_output_directory(self):
        """Ouvre une boîte de dialogue pour sélectionner un dossier de sortie."""
        dir_path = QFileDialog.getExistingDirectory(self.parent, "Sélectionner un dossier de résultats")
        return dir_path
