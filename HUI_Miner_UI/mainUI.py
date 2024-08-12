import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QFormLayout, QLineEdit, QPushButton, QFileDialog, 
                               QLabel, QTextEdit, QHBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from HUI_Miner_ForUI import HUIMiner  # Import HUI-Miner algorithm from the file

class HUI_Miner_GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HUI-Miner Algorithm")
        self.setGeometry(100, 100, 600, 400)

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
        self.results = ""  # To store results in memory
        self.hui_miner = HUIMiner()  # Create instance of HUIMiner

    def browseDataset(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Dataset File", "", "Text Files (*.txt)")
        if file_name:
            self.dataset_file_label.setText(file_name)  # Update label to show the file path

    def runAlgorithm(self):
        try:
            dataset_file = self.dataset_file_label.text()
            min_utility = float(self.min_utility_input.text())

            if dataset_file == "No file selected":
                QMessageBox.warning(self, "Warning", "Please select a dataset file.")
                return
            if min_utility == None:
                QMessageBox.warning(self, "Warning", "Min Utility can not be null.")
            self.hui_miner.runAlgorithm(dataset_file, min_utility)
            # Display results
            
            self.results = "\n".join(self.hui_miner.results)
            self.results += f"\nJoin count: {self.hui_miner.joinCount} times"
            self.results += f"\nTotal times: {self.hui_miner.times:.2f} s"
            self.results += f"\nTotal memory: {self.hui_miner.memory:2f} MB"
            self.results_text.setPlainText(self.results)

            # Update status label
            elapsed_time = self.hui_miner.times
            memory_usage = self.hui_miner.memory
            self.status_label.setText(f"Time: {elapsed_time:.2f} seconds | Memory: {memory_usage:.2f} MB")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    def saveResults(self):
        if not self.results:
            QMessageBox.warning(self, "Warning", "No results to save.")
            return
        
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Results", "", "Text Files (*.txt)")
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.results)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HUI_Miner_GUI()
    window.show()
    sys.exit(app.exec())
