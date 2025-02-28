import os
import subprocess
from robot.api import ExecutionResult

class TestRunner:
    def __init__(self):
        self.test_directory = ""
        self.output_directory = ""

    def set_test_directory(self, path):
        self.test_directory = path
        self.output_directory = os.path.join(path, "Results")
        os.makedirs(self.output_directory, exist_ok=True)

    def set_output_directory(self, path):
        self.output_directory = path

    def get_test_files(self):
        """Retourne une liste des fichiers .robot disponibles."""
        return [f for f in os.listdir(self.test_directory) if f.endswith(".robot")]

    def run_tests(self, selected_tests, num_processes):
        """Exécute les tests sélectionnés avec Pabot."""
        if not self.test_directory or not selected_tests:
            return "Veuillez sélectionner un dossier et des tests."

        command = ["pabot", "--processes", str(num_processes), "--outputdir", self.output_directory] + selected_tests
        subprocess.run(command, cwd=self.test_directory, capture_output=True, text=True)

        output_path = os.path.join(self.output_directory, "output.xml")
        result = ExecutionResult(output_path)

        return f"Total: {result.suite.statistics.total} | Passés: {result.suite.statistics.passed} | Échoués: {result.suite.statistics.failed}"

    def open_report(self):
        report_path = os.path.join(self.output_directory, "report.html")
        if os.path.exists(report_path):
            os.system(f'start "" "{report_path}"')

    def open_log(self):
        log_path = os.path.join(self.output_directory, "log.html")
        if os.path.exists(log_path):
            os.system(f'start "" "{log_path}"')
