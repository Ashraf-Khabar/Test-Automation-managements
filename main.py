import sys
import os
import subprocess
from robot.api import ExecutionResult
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt

class RobotTestRunner(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.layout = QVBoxLayout()
        
        self.label = QLabel("Select a directory containing .robot files")
        self.layout.addWidget(self.label)
        
        self.selectButton = QPushButton("Select Directory")
        self.selectButton.clicked.connect(self.select_directory)
        self.layout.addWidget(self.selectButton)
        
        self.testList = QListWidget()
        self.layout.addWidget(self.testList)
        
        self.runButton = QPushButton("Run Selected Tests")
        self.runButton.clicked.connect(self.run_tests)
        self.layout.addWidget(self.runButton)
        
        self.resultLabel = QLabel("Test Results: ")
        self.layout.addWidget(self.resultLabel)
        
        self.reportButton = QPushButton("Open Report")
        self.reportButton.clicked.connect(self.open_report)
        self.layout.addWidget(self.reportButton)
        
        self.logButton = QPushButton("Open Log")
        self.logButton.clicked.connect(self.open_log)
        self.layout.addWidget(self.logButton)
        
        self.setLayout(self.layout)
        self.setWindowTitle("Robot Framework Test Runner")
        self.setGeometry(200, 200, 500, 400)
        
        self.apply_styles()  # Applique le style externe
        self.test_directory = ""

    def apply_styles(self):
        """Charge le fichier QSS et applique le style."""
        style_file = os.path.abspath("style.qss")  # Utilise un chemin absolu

        if os.path.exists(style_file):
            with open(style_file, "r") as file:
                qss = file.read()
                self.setStyleSheet(qss)
                print("Style chargé avec succès !")
        else:
            print(f"ERREUR : '{style_file}' non trouvé !")

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            self.test_directory = dir_path
            self.label.setText(f"Selected: {dir_path}")
            self.load_tests()
    
    def load_tests(self):
        self.testList.clear()
        if self.test_directory:
            for file in os.listdir(self.test_directory):
                if file.endswith(".robot"):
                    item = QListWidgetItem(file)
                    item.setCheckState(Qt.CheckState.Unchecked)
                    self.testList.addItem(item)

    def run_tests(self):
        if not self.test_directory:
            self.resultLabel.setText("Please select a directory first.")
            return
        
        selected_tests = [os.path.join(self.test_directory, self.testList.item(i).text()) for i in range(self.testList.count()) if self.testList.item(i).checkState() == Qt.CheckState.Checked]
        
        if not selected_tests:
            self.resultLabel.setText("Please select at least one test.")
            return
        
        command = ["pabot", "--outputdir", self.test_directory] + selected_tests
        process = subprocess.run(command, cwd=self.test_directory, capture_output=True, text=True)
        
        output = process.stdout
        error_output = process.stderr
        
        output_path = os.path.join(self.test_directory, "output.xml")
        result = ExecutionResult(output_path)
        print(f"Total Tests: {result.suite.statistics.total}")
        print(f"Passed Tests: {result.suite.statistics.passed}")
        print(f"Failed Tests: {result.suite.statistics.failed}")
        
        self.resultLabel.setText(f"Total Tests: {result.suite.statistics.total} | Tests Passed: {result.suite.statistics.passed} | Tests Failed: {result.suite.statistics.failed}")
        
        if error_output:
            self.resultLabel.setText(self.resultLabel.text() + "\nErrors:\n" + error_output)

    def open_report(self):
        report_path = os.path.join(self.test_directory, "report.html")
        if os.path.exists(report_path):
            os.system(f'start "" "{report_path}"')

    def open_log(self):
        log_path = os.path.join(self.test_directory, "log.html")
        if os.path.exists(log_path):
            os.system(f'start "" "{log_path}"')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RobotTestRunner()
    window.show()
    sys.exit(app.exec())
