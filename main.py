import sys
import os
import subprocess
from robot.api import ExecutionResult
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
                            QLabel, QListWidget, QListWidgetItem, QHBoxLayout, QFrame, QCheckBox)
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QSpinBox
from PyQt6 import QtCore

class RobotTestRunner(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.drag_position = QPoint()
        self.logo_label = None
        self.show_logo()

    def resource_path(self, relative_path):
        """Récupérer le chemin d'accès aux ressources (image, fichiers) dans l'exécutable."""
        try:
            base_path = sys._MEIPASS
        except Exception:

            base_path = os.path.dirname(__file__)
        return os.path.join(base_path, relative_path)

    def show_logo(self):
        self.logo_label = QLabel(self)
        
        logo_path = self.resource_path("images/Logo.png")
        
        logo_pixmap = QPixmap(logo_path)
        self.logo_label.setPixmap(logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.logo_label.setGeometry(self.rect()) 
        self.logo_label.show()

        QTimer.singleShot(4000, self.hide_logo)

    def hide_logo(self):
        if self.logo_label:
            self.logo_label.hide()

    def initUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(900, 550)
        
        self.layout = QVBoxLayout()
        
        self.titleBar = QHBoxLayout()
        self.titleBarWidget = QFrame()
        self.titleBarWidget.setObjectName("titleBar")
        self.titleBarLayout = QHBoxLayout(self.titleBarWidget)
        self.titleBarLayout.setContentsMargins(0, 0, 0, 0)
        
        self.titleLabel = QLabel("Robot Framework Test Runner")
        self.titleLabel.setStyleSheet("font-weight: bold; padding-left: 10px;")
        self.titleBarLayout.addWidget(self.titleLabel)
        self.titleBarLayout.addStretch()
        
        self.minimizeButton = QPushButton("-")
        self.closeButton = QPushButton("X")
        
        self.minimizeButton.setFixedSize(30, 30)
        self.closeButton.setFixedSize(30, 30)
        
        self.minimizeButton.clicked.connect(self.showMinimized)
        self.closeButton.clicked.connect(self.close)
        
        self.titleBarLayout.addWidget(self.minimizeButton)
        self.titleBarLayout.addWidget(self.closeButton)
        
        self.titleBar.addWidget(self.titleBarWidget)
        self.layout.addLayout(self.titleBar)
        
        self.label = QLabel("Sélectionnez un dossier contenant des fichiers .robot")
        self.layout.addWidget(self.label)
        
        self.selectButton = QPushButton("Sélectionner un dossier")
        self.selectButton.clicked.connect(self.select_directory)
        self.layout.addWidget(self.selectButton)

        # Modif
        self.layoutHorizantal = QHBoxLayout()
        self.selectAllCheckBox = QCheckBox("Sélectionner tous les tests")
        self.selectAllCheckBox.stateChanged.connect(self.toggle_select_all_tests)
        self.layoutHorizantal.addWidget(self.selectAllCheckBox)

        self.refreshButton = QPushButton("Refresh tests")
        self.refreshButton.setFixedSize(QtCore.QSize(100, 40))
        self.refreshButton.clicked.connect(self.load_tests)
        self.layoutHorizantal.addWidget(self.refreshButton)
        
        self.layout.addItem(self.layoutHorizantal)
        # modif
        
        self.testList = QListWidget()
        self.layout.addWidget(self.testList)
        
        paramLayout = QHBoxLayout()
        
        self.processLabel = QLabel("Nombre de subprocess :")
        self.processInput = QSpinBox()
        self.processInput.setValue(2)
        self.processInput.setFixedWidth(50)
        self.processInput.setMinimum(2)
        self.processInput.setMaximum(50)
        paramLayout.addWidget(self.processLabel)
        paramLayout.addWidget(self.processInput)
        
        self.fileLabel = QLabel("Sélectionner emplacement des résultats :")
        self.fileButton = QPushButton("Choisir dossier")
        self.fileButton.clicked.connect(self.select_output_directory)
        self.layout.addWidget(self.fileLabel)
        self.layout.addWidget(self.fileButton)
        
        self.layout.addLayout(paramLayout)
        
        self.runButton = QPushButton("Exécuter les tests sélectionnés")
        self.runButton.clicked.connect(self.run_tests)
        self.layout.addWidget(self.runButton)
        
        self.resultLabel = QLabel("Résultats des tests :")
        self.layout.addWidget(self.resultLabel)
        
        self.reportButton = QPushButton("Ouvrir le rapport")
        self.reportButton.clicked.connect(self.open_report)
        self.layout.addWidget(self.reportButton)
        
        self.logButton = QPushButton("Ouvrir le log")
        self.logButton.clicked.connect(self.open_log)
        self.layout.addWidget(self.logButton)

        self.version_layout = QVBoxLayout()
        self.version = QLabel("Robot Runner v 1.0.0")
        self.version_layout.addWidget(self.version)
        self.layout.addLayout(self.version_layout)
        
        self.setLayout(self.layout)
        self.setWindowTitle("Robot Framework Test Runner")
        
        self.apply_styles()
        self.test_directory = ""
        self.output_directory = ""
    
    def apply_styles(self):
        style_file = self.resource_path("style/style.qss")
        
        if os.path.exists(style_file):
            with open(style_file, "r") as file:
                self.setStyleSheet(file.read())
    
    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier")
        if dir_path:
            self.test_directory = dir_path
            self.label.setText(f"Sélectionné : {dir_path}")
            self.output_directory = os.path.join(dir_path, "Results")
            os.makedirs(self.output_directory, exist_ok=True)
            self.load_tests()
    
    def select_output_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier de résultats")
        if dir_path:
            self.output_directory = dir_path
            self.fileLabel.setText(f"Résultats enregistrés dans : {dir_path}")
    
    def load_tests(self):
        self.testList.clear()
        if self.test_directory:
            for file in os.listdir(self.test_directory):
                if file.endswith(".robot"):
                    item = QListWidgetItem(file)
                    item.setCheckState(Qt.CheckState.Unchecked)
                    self.testList.addItem(item)
    
    def toggle_select_all_tests(self, state):
        check_state = Qt.CheckState.Checked if state == QtCore.Qt.CheckState.Checked.value else Qt.CheckState.Unchecked

        for i in range(self.testList.count()):
            self.testList.item(i).setCheckState(check_state)
    
    def run_tests(self):
        if not self.test_directory:
            self.resultLabel.setText("Veuillez sélectionner un dossier.")
            return
        
        if not self.output_directory:
            self.resultLabel.setText("Veuillez sélectionner un emplacement pour les résultats.")
            return
        
        selected_tests = [os.path.join(self.test_directory, self.testList.item(i).text())
                          for i in range(self.testList.count())
                          if self.testList.item(i).checkState() == Qt.CheckState.Checked]
        
        if not selected_tests:
            self.resultLabel.setText("Veuillez sélectionner au moins un test.")
            return
        
        num_processes = self.processInput.text()
        
        command = ["pabot", "--processes", num_processes, "--outputdir", self.output_directory] + selected_tests
        process = subprocess.run(command, cwd=self.test_directory, capture_output=True, text=True)
        
        output_path = os.path.join(self.output_directory, "output.xml")
        result = ExecutionResult(output_path)
        
        self.resultLabel.setText(f"Total: {result.suite.statistics.total} | Passés: {result.suite.statistics.passed} | Échoués: {result.suite.statistics.failed}")
    
    def open_report(self):
        report_path = os.path.join(self.output_directory, "report.html")
        if os.path.exists(report_path):
            os.system(f'start "" "{report_path}"')
    
    def open_log(self):
        log_path = os.path.join(self.output_directory, "log.html")
        if os.path.exists(log_path):
            os.system(f'start "" "{log_path}"')
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RobotTestRunner()
    window.show()
    sys.exit(app.exec())