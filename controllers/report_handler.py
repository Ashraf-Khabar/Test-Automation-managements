from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QWidget
from PyQt6.QtGui import QDesktopServices
import os

class ReportHandler(QWidget):
    def __init__(self, output_directory):
        super().__init__()
        self.output_directory = output_directory
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.reportButton = QPushButton("Ouvrir le rapport")
        self.reportButton.clicked.connect(self.open_report)
        self.layout.addWidget(self.reportButton)

        self.logButton = QPushButton("Ouvrir le log")
        self.logButton.clicked.connect(self.open_log)
        self.layout.addWidget(self.logButton)

        self.setLayout(self.layout)

    def open_report(self):
        report_path = os.path.join(self.output_directory, "report.html")
        if os.path.exists(report_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(report_path))

    def open_log(self):
        log_path = os.path.join(self.output_directory, "log.html")
        if os.path.exists(log_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(log_path))