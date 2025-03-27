import sys
import os
import subprocess
import shutil
from robot.api import ExecutionResult
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
                             QLabel, QListWidget, QListWidgetItem, QHBoxLayout, QFrame, QCheckBox)
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QSpinBox
from PyQt6 import QtCore
from PyQt6.QtGui import QMovie

class RobotTestRunner(QWidget):
    def __init__(self):
        super().__init__()
        self.version_label = "© Robot Runner v 1.5.0"
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

        QTimer.singleShot(2500, self.hide_logo)

    def hide_logo(self):
        if self.logo_label:
            self.logo_label.hide()

    def initUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(1100, 650)
        self.setStyleSheet("border-radius: 10px")
        
        self.layout = QVBoxLayout()
        
        self.titleBar = QHBoxLayout()
        self.titleBarWidget = QFrame()
        self.titleBarWidget.setObjectName("titleBar")
        self.titleBarLayout = QHBoxLayout(self.titleBarWidget)
        self.titleBarLayout.setContentsMargins(0, 0, 0, 0)
        
        self.titleLabel = QLabel("Robot Framework Test Runner")
        self.titleLabel.setStyleSheet("font-weight: bold; padding-left: 5px;")

        self.titleBarLayout.addWidget(self.titleLabel)
        self.titleBarLayout.addStretch()
        
        self.minimizeButton = QPushButton("_")
        self.closeButton = QPushButton("X")
        
        self.minimizeButton.setFixedSize(30, 30)
        self.closeButton.setFixedSize(30, 30)
        
        self.minimizeButton.clicked.connect(self.showMinimized)
        self.closeButton.clicked.connect(self.close)
        
        self.titleBarLayout.addWidget(self.minimizeButton)
        self.titleBarLayout.addWidget(self.closeButton)
        
        self.titleBar.addWidget(self.titleBarWidget)
        self.layout.addLayout(self.titleBar)
        
        self.label = QLabel("Select a folder containing .robot files")
        self.layout.addWidget(self.label)
        
        self.selectButton = QPushButton("Select Folder")
        self.selectButton.clicked.connect(self.select_directory)
        self.layout.addWidget(self.selectButton)

        self.layoutHorizantal = QHBoxLayout()

        self.selectAllCheckBox = QCheckBox("Select all tests")
        self.selectAllCheckBox.stateChanged.connect(self.toggle_select_all_tests)
        self.layoutHorizantal.addWidget(self.selectAllCheckBox)

        self.refreshLayout = QHBoxLayout()

        self.refreshButton = QPushButton("Refresh tests")
        self.refreshButton.setFixedSize(QtCore.QSize(100, 40))
        self.refreshButton.clicked.connect(self.load_tests)
        self.refreshLayout.addWidget(self.refreshButton)

        self.loadingLabel = QLabel()
        self.loadingLabel.setFixedSize(30, 30) 
        self.loadingLabel.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        self.refreshLayout.addWidget(self.loadingLabel)

        self.layoutHorizantal.addLayout(self.refreshLayout)
        self.layout.addItem(self.layoutHorizantal)

        self.testList = QListWidget()
        self.layout.addWidget(self.testList)
        
        paramLayout = QHBoxLayout()
        
        self.processLabel = QLabel("Number of subprocesses :")
        self.processInput = QSpinBox()
        self.processInput.setValue(2)
        self.processInput.setFixedWidth(50)
        self.processInput.setMinimum(1)
        self.processInput.setMaximum(50)
        paramLayout.addWidget(self.processLabel)
        paramLayout.addWidget(self.processInput)
        self.layout.addLayout(paramLayout)
        
        self.fileLabel = QLabel("Select result storage location :")
        self.fileButton = QPushButton("Choisir dossier")
        self.fileButton.clicked.connect(self.select_output_directory)
        
        self.clearButton = QPushButton("Clear results")
        self.clearButton.clicked.connect(self.clear_results_directory)

        fileLayout = QHBoxLayout()
        fileLayout.addWidget(self.fileButton)
        fileLayout.addWidget(self.clearButton)

        self.layout.addWidget(self.fileLabel)
        self.layout.addLayout(fileLayout)        


        self.runButton = QPushButton("Run selected tests")
        self.runButton.clicked.connect(self.run_tests)
        self.layout.addWidget(self.runButton)
        
        self.resultLabel = QLabel("Test Results :")
        self.layout.addWidget(self.resultLabel)
        
        self.reportButton = QPushButton("Open Report")
        self.reportButton.clicked.connect(self.open_report)
        self.layout.addWidget(self.reportButton)
        
        self.logButton = QPushButton("Open Log")
        self.logButton.clicked.connect(self.open_log)
        self.layout.addWidget(self.logButton)

        self.version_layout = QVBoxLayout()
        self.version = QLabel(f"{self.version_label}")
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
            
            os.path.join(dir_path, "Results")
            os.makedirs(os.path.join(dir_path, "Results"), exist_ok=True)

            self.testList.clear() 
            self.load_tests()
        else:
            self.show_cross()
            self.label.setStyleSheet("color: #ad402a")
    
    def select_output_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier de résultats")
        if dir_path:
            self.output_directory = dir_path
            self.fileLabel.setText(f"Résultats enregistrés dans : {dir_path}")
            self.fileLabel.setStyleSheet("color: green")
    
    def show_cross(self):
        cross_icon_path = self.resource_path("images/cross.png")
        cross_pixmap = QPixmap(cross_icon_path).scaled(20, 20, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.loadingLabel.setPixmap(cross_pixmap)
        self.loadingLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def populate_tests(self):
        self.loading_movie.stop()
        self.loadingLabel.clear()

        if self.test_directory:

            test_files = [file for file in os.listdir(self.test_directory) if file.endswith(".robot")]

            if not test_files:
                self.show_cross()
                self.label.setStyleSheet("color: #ad402a")
            else:
                for file in test_files:
                    item = QListWidgetItem(file)
                    item.setCheckState(Qt.CheckState.Unchecked)
                    self.testList.addItem(item)

                self.label.setStyleSheet("color: green")
                check_icon_path = self.resource_path("images/check.png")
                check_pixmap = QPixmap(check_icon_path).scaled(27, 27, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
                self.loadingLabel.setPixmap(check_pixmap)
                self.loadingLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def load_tests(self):
        self.testList.clear()
        self.loadingLabel.show()
        loading_gif_path = self.resource_path("images/loading.gif")
        self.loading_movie = QMovie(loading_gif_path)
        self.loading_movie.setScaledSize(QtCore.QSize(45, 45))
        self.loadingLabel.setMovie(self.loading_movie)
        self.loading_movie.start()
        QtCore.QTimer.singleShot(1500, self.populate_tests)

    def toggle_select_all_tests(self, state):
        check_state = Qt.CheckState.Checked if state == QtCore.Qt.CheckState.Checked.value else Qt.CheckState.Unchecked
        for i in range(self.testList.count()):
            self.testList.item(i).setCheckState(check_state)
    
    def run_tests(self):
        if not self.test_directory:
            self.resultLabel.setStyleSheet("color: none")
            self.resultLabel.setText("Please select a folder.")
            self.resultLabel.setStyleSheet("color: #ad402a")
            return
        
        if not self.output_directory:
            self.resultLabel.setStyleSheet("color: none")
            self.resultLabel.setText("Please select a location for the results.")
            self.resultLabel.setStyleSheet("color: #ad402a") 
            return 
        
        selected_tests = [os.path.join(self.test_directory, self.testList.item(i).text())
                         for i in range(self.testList.count())
                         if self.testList.item(i).checkState() == Qt.CheckState.Checked]
        
        if not selected_tests:
            self.resultLabel.setStyleSheet("color: none")
            self.resultLabel.setText("Please select at least one test.")
            self.resultLabel.setStyleSheet("color: #ad402a")
            return
        
        num_processes = self.processInput.text()
        repport_title = "Robot Runner - Tests Autos"

        if num_processes == 1:
            command = ["robot", "-d", self.output_directory] + selected_tests            
            output_path = os.path.join(self.output_directory, "output.xml")
        else :
            command = ["pabot", "--processes", num_processes, "--outputdir", self.output_directory, "--reporttitle", repport_title] + selected_tests
            subprocess.run(command, cwd=self.test_directory, capture_output=True, text=True)
        
        
        output_path = os.path.join(self.output_directory, "output.xml")
        result = ExecutionResult(output_path)
         
        if result.suite.statistics.failed >= 1:
            self.resultLabel.setStyleSheet("color: none")
            self.resultLabel.setText(f"TOTAL: {result.suite.statistics.total} | PASS: {result.suite.statistics.passed} | FAIL: {result.suite.statistics.failed}")
            self.resultLabel.setStyleSheet("color: #ad402a")
        else:
            self.resultLabel.setStyleSheet("color: none")
            self.resultLabel.setText(f"TOTAL: {result.suite.statistics.total} | PASS: {result.suite.statistics.passed} | FAIL: {result.suite.statistics.failed}")
            self.resultLabel.setStyleSheet("color: green")

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
    
    def clear_results_directory(self):
        if self.output_directory and os.path.exists(self.output_directory):
            for file in os.listdir(self.output_directory):
                file_path = os.path.join(self.output_directory, file)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    self.resultLabel.setText(f"Deletion error : {str(e)}")
                    self.resultLabel.setStyleSheet("color: #ad402a")
                    return
            
            self.resultLabel.setText("The Results folder has been emptied")
            self.resultLabel.setStyleSheet("color: green")
        else:
            self.resultLabel.setText("No Results folder found")
            self.resultLabel.setStyleSheet("color: #ad402a")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RobotTestRunner()
    window.show()
    sys.exit(app.exec())