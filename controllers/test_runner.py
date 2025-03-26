import os
import subprocess
from robot.api import ExecutionResult
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QListWidget, QListWidgetItem, QHBoxLayout, QCheckBox, QSpinBox)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog

class TestRunner(QWidget):
    def __init__(self):
        super().__init__()
        self.test_directory = ""
        self.output_directory = ""
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        
        self.label = QLabel("Sélectionnez un dossier contenant des fichiers .robot")
        self.layout.addWidget(self.label)
        
        self.selectButton = QPushButton("Sélectionner un dossier de tests")
        self.selectButton.clicked.connect(self.select_directory)
        self.layout.addWidget(self.selectButton)
        
        self.selectAllCheckBox = QCheckBox("Sélectionner tous les tests")
        self.selectAllCheckBox.stateChanged.connect(self.toggle_select_all_tests)
        self.layout.addWidget(self.selectAllCheckBox)

        self.testList = QListWidget()
        self.layout.addWidget(self.testList)

        paramLayout = QHBoxLayout()
        self.processLabel = QLabel("Nombre de subprocess :")
        self.processInput = QSpinBox()
        self.processInput.setValue(2)
        self.processInput.setFixedWidth(50)
        paramLayout.addWidget(self.processLabel)
        paramLayout.addWidget(self.processInput)
        self.layout.addLayout(paramLayout)

        self.resultButton = QPushButton("Choisir le dossier de résultats")
        self.resultButton.clicked.connect(self.select_output_directory)
        self.layout.addWidget(self.resultButton)

        self.runButton = QPushButton("Exécuter les tests sélectionnés")
        self.runButton.clicked.connect(self.run_tests)
        self.layout.addWidget(self.runButton)

        self.resultLabel = QLabel("Résultats des tests :")
        self.layout.addWidget(self.resultLabel)

        self.setLayout(self.layout)
    

    def select_output_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier de résultats")
        if dir_path:
            self.output_directory = dir_path
            self.resultLabel.setText(f"Résultats seront stockés dans : {dir_path}")

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier de tests")
        if dir_path:
            self.test_directory = dir_path
            self.output_directory = os.path.join(dir_path, "Results")
            os.makedirs(self.output_directory, exist_ok=True)
            self.load_tests()

