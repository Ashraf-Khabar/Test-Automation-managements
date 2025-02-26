import os
import subprocess
from robot.api import ExecutionResult
from PyQt6.QtCore import Qt

class TestRunner:
    def __init__(self, parent):
        self.parent = parent

    def run_tests(self):
        if not self.parent.file_manager.test_directory:
            self.parent.resultLabel.setText("Veuillez sélectionner un dossier.")
            return

        if not self.parent.file_manager.output_directory:
            self.parent.resultLabel.setText("Veuillez sélectionner un emplacement pour les résultats.")
            return

        selected_tests = [
            os.path.join(self.parent.file_manager.test_directory, self.parent.testList.item(i).text())
            for i in range(self.parent.testList.count())
            if self.parent.testList.item(i).checkState() == Qt.CheckState.Checked
        ]

        if not selected_tests:
            self.parent.resultLabel.setText("Veuillez sélectionner au moins un test.")
            return

        num_processes = self.parent.processInput.text()

        command = ["pabot", "--processes", num_processes, "--outputdir", self.parent.file_manager.output_directory] + selected_tests
        subprocess.run(command, cwd=self.parent.file_manager.test_directory, capture_output=True, text=True)

        output_path = os.path.join(self.parent.file_manager.output_directory, "output.xml")
        result = ExecutionResult(output_path)

        self.parent.resultLabel.setText(f"Total: {result.suite.statistics.total} | Passés: {result.suite.statistics.passed} | Échoués: {result.suite.statistics.failed}")
