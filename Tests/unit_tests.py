import unittest
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from main import RobotTestRunner

app = QApplication([])  

class TestRobotTestRunner(unittest.TestCase):
    
    def setUp(self):
        """Set up the test instance before each test"""
        self.window = RobotTestRunner()

    def test_ui_elements_exist(self):
        """Ensure all important UI elements exist"""
        self.assertIsNotNone(self.window.selectButton)
        self.assertIsNotNone(self.window.testList)
        self.assertIsNotNone(self.window.runButton)
        self.assertIsNotNone(self.window.resultLabel)

    def test_toggle_select_all_tests(self):
        """Test the 'Select All Tests' checkbox behavior"""
        self.window.testList.addItem("test1.robot")
        self.window.testList.addItem("test2.robot")

        self.window.selectAllCheckBox.setChecked(True)
        for i in range(self.window.testList.count()):
            self.assertEqual(self.window.testList.item(i).checkState(), Qt.CheckState.Checked)

        self.window.selectAllCheckBox.setChecked(False)
        for i in range(self.window.testList.count()):
            self.assertEqual(self.window.testList.item(i).checkState(), Qt.CheckState.Unchecked)

    def test_select_directory(self):
        """Test setting the test directory"""
        test_dir = os.path.abspath("test_directory")
        self.window.test_directory = test_dir
        self.assertEqual(self.window.test_directory, test_dir)

    def test_run_tests_without_selection(self):
        """Test running tests when no tests are selected"""
        self.window.test_directory = "mock_directory"
        self.window.output_directory = "mock_results"  

        self.window.run_tests()
        self.assertIn("Veuillez sélectionner au moins un test", self.window.resultLabel.text())

    def test_set_output_directory(self):
        """Test setting the output directory"""
        output_dir = os.path.abspath("results")
        self.window.output_directory = output_dir
        self.assertEqual(self.window.output_directory, output_dir)

    def test_run_tests_without_directory(self):
        """Test running tests when no test directory is set"""
        self.window.run_tests()
        self.assertIn("Veuillez sélectionner un dossier", self.window.resultLabel.text())

    def tearDown(self):
        """Cleanup after each test"""
        self.window.close()


if __name__ == "__main__":
    unittest.main()