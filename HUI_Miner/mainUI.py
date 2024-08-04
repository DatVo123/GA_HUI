import sys
import tempfile
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QFormLayout, QLineEdit, QPushButton, QFileDialog, 
                               QLabel, QTextEdit, QHBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from HUI_Miner_ForUI import HUIMiner  # Import thuật toán HUI-Miner từ tệp hui_miner.py

class HUI_Miner_GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HUI-Miner Algorithm")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon("icon.png"))  # Thay thế bằng icon của bạn nếu có

        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # Title
        self.title = QLabel("HUI-Miner Algorithm")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 22px; font-weight: bold; color: #00568b;")
        self.layout.addWidget(self.title)

        # Container widget for buttons
        self.button_container = QWidget()
        self.button_layout = QHBoxLayout()
        self.button_container.setLayout(self.button_layout)
        self.layout.addWidget(self.button_container)

        # Buttons for actions
        self.run_button = QPushButton("Run Algorithm")
        self.run_button.setStyleSheet("background-color: #00568b; color: white; font-weight: bold; padding: 5px;")
        self.run_button.setFixedSize(120, 30)
        self.run_button.clicked.connect(self.runAlgorithm)
        
        self.save_button = QPushButton("Save Results")
        self.save_button.setStyleSheet("background-color: #00568b; color: white; font-weight: bold; padding: 5px;")
        self.save_button.setFixedSize(120, 30)
        self.save_button.clicked.connect(self.saveResults)

        # Adding buttons to the button layout
        self.button_layout.addWidget(self.run_button)
        self.button_layout.addWidget(self.save_button)

        # Form layout for inputs
        self.form_layout = QFormLayout()
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.layout.addLayout(self.form_layout)

        # Dataset file path (label only) and Browse button
        self.dataset_label = QLabel("Dataset File:")
        self.dataset_file_label = QLabel("No file selected")  # Placeholder text
        self.dataset_button = QPushButton("Browse")
        self.dataset_button.clicked.connect(self.browseDataset)
        self.form_layout.addRow(self.dataset_label, self.dataset_file_label)
        self.form_layout.addWidget(self.dataset_button)

        # Minimum utility input field
        self.min_utility_input = QLineEdit()
        self.min_utility_input.setPlaceholderText("Enter minimum utility")
        self.form_layout.addRow(QLabel("Minimum Utility:"), self.min_utility_input)

        # Text area for results
        self.results_text = QTextEdit()
        self.results_text.setPlaceholderText("Results will be displayed here...")
        self.results_text.setReadOnly(True)
        self.layout.addWidget(self.results_text)

        # Status label
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; color: #00568b;")
        self.layout.addWidget(self.status_label)

        # Initialize variables
        self.results_file = ""

    def browseDataset(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Dataset File", "", "Text Files (*.txt)")
        if file_name:
            self.dataset_file_label.setText(file_name)  # Update label to show the file path

    def runAlgorithm(self):
        dataset_file = self.dataset_file_label.text()
        min_utility = self.min_utility_input.text()

        if not dataset_file or not min_utility:
            QMessageBox.warning(self, "Input Error", "Please provide both dataset file and minimum utility.")
            return
        
        try:
            min_utility = int(min_utility)
            self.status_label.setText("Algorithm is running...")
            self.results_text.clear()  # Clear previous results
            
            # Create a temporary output file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", dir=tempfile.gettempdir())
            temp_file.close()
            
            # Run the HUI-Miner algorithm
            hui_miner = HUIMiner()
            hui_miner.runAlgorithm(dataset_file, temp_file.name, min_utility)
            
            # Read results from the temporary file
            with open(temp_file.name, 'r') as file:
                results = file.read()

            self.results_text.setPlainText(results)
            self.results_file = temp_file.name
            self.status_label.setText("Algorithm completed successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            self.status_label.setText("Error occurred.")

    def saveResults(self):
        if not self.results_file:
            QMessageBox.warning(self, "No Results", "No results to save.")
            return
        
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Results", "", "Text Files (*.txt)")
        if file_name:
            try:
                os.rename(self.results_file, file_name)
                self.results_file = ""
                self.status_label.setText(f"Results saved to {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while saving results: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HUI_Miner_GUI()
    window.show()
    sys.exit(app.exec())
