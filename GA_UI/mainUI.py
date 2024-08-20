import os
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QLabel,
    QFileDialog,
    QMessageBox,
    QGridLayout,
    QSplitter,
    QProgressDialog,
    QGroupBox,
)
from PyQt6.QtGui import QFont, QKeySequence
from PyQt6.QtCore import Qt

from worker import Worker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Genetic Algorithm App")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout using QVBoxLayout
        self.layout = QVBoxLayout(self.central_widget)

        # Title label
        title_label = QLabel("Apply Genetic Algorithm To Find HUI")
        title_label.setFont(QFont("Roboto", 20, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title_label)

        # Group box for header buttons
        header_group = QGroupBox("Actions")
        header_group_layout = QHBoxLayout()
        header_group.setLayout(header_group_layout)
        self.layout.addWidget(header_group)

        # Open file button
        self.open_file_button = QPushButton("Open File")
        self.open_file_button.setFixedWidth(80)
        self.open_file_button.setStyleSheet(
            """
            QPushButton {
                background-color: #00568b; color: white
            }
            QPushButton:hover {
                background-color: #003f5c;
            }
            """
        )
        self.open_file_button.clicked.connect(self.open_file_dialog)
        header_group_layout.addWidget(self.open_file_button)
        self.open_file_button.setShortcut(QKeySequence("Ctrl+O"))
        self.open_file_button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Label for file path
        self.file_path_label = QLabel("File Path: ")
        header_group_layout.addWidget(self.file_path_label)

        # Run algorithm button
        self.run_algorithm_button = QPushButton("Run Algorithm")
        self.run_algorithm_button.setFixedWidth(100)
        self.run_algorithm_button.setStyleSheet(
            """
            QPushButton {
                background-color: #c4d8e2; color: black
            }
            QPushButton:hover {
                background-color: #a4c8d2;
            }
            """
        )
        self.run_algorithm_button.clicked.connect(self.run_genetic_algorithm)
        header_group_layout.addWidget(self.run_algorithm_button)
        self.run_algorithm_button.setShortcut(QKeySequence(Qt.Key.Key_Return))
        self.run_algorithm_button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Save output button
        self.save_output_button = QPushButton("Save Output")
        self.save_output_button.setFixedWidth(80)
        self.save_output_button.setStyleSheet(
            """
            QPushButton {
                background-color: #c4d8e2; color: black
            }
            QPushButton:hover {
                background-color: #a4c8d2;
            }
            """
        )
        self.save_output_button.clicked.connect(self.save_output_to_file)
        header_group_layout.addWidget(self.save_output_button)
        self.save_output_button.setShortcut(QKeySequence("Ctrl+S"))
        self.save_output_button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setFixedWidth(80)
        self.refresh_button.setStyleSheet(
            """
            QPushButton {
                background-color: #f0e68c; color: black
            }
            QPushButton:hover {
                background-color: #d0c458;
            }
            """
        )
        self.refresh_button.clicked.connect(self.refresh_fields)
        header_group_layout.addWidget(self.refresh_button)
        self.refresh_button.setShortcut(QKeySequence("Ctrl+R"))
        self.refresh_button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Splitter to divide vertically
        splitter = QSplitter(Qt.Orientation.Vertical)
        self.layout.addWidget(splitter)

        param_and_running_splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(param_and_running_splitter)

        parameters_layout = QGridLayout()
        parameters_layout.setSpacing(10)  # Adjust the spacing between elements

        # Create a group box for parameters
        parameters_group = QGroupBox("Parameters")
        parameters_group.setLayout(parameters_layout)
        parameters_group.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 10px;
            }
            """
        )

        # Min utility
        min_utility_label = QLabel("Min Utility")
        self.min_utility_textbox = QLineEdit()
        self.min_utility_textbox.setPlaceholderText("Min Utility Value")
        parameters_layout.addWidget(min_utility_label, 0, 0)
        parameters_layout.addWidget(self.min_utility_textbox, 1, 0)
        # Generations
        generations_label = QLabel("Generations")
        self.generations_textbox = QLineEdit()
        self.generations_textbox.setPlaceholderText("Generations Value")
        self.generations_textbox.setText('20')
        parameters_layout.addWidget(generations_label, 0, 1)
        parameters_layout.addWidget(self.generations_textbox, 1, 1)

        # Population size
        population_size_label = QLabel("Population Size")
        self.population_size_textbox = QLineEdit()
        self.population_size_textbox.setText('100')
        self.population_size_textbox.setPlaceholderText("Population Size Value")
        parameters_layout.addWidget(population_size_label, 2, 0)
        parameters_layout.addWidget(self.population_size_textbox, 3, 0)

        # Crossover probability
        crossover_prob_label = QLabel("Crossover Probability")
        self.crossover_prob_textbox = QLineEdit()
        self.crossover_prob_textbox.setText('0.8')
        self.crossover_prob_textbox.setPlaceholderText("Crossover Probability Value")
        parameters_layout.addWidget(crossover_prob_label, 2, 1)
        parameters_layout.addWidget(self.crossover_prob_textbox, 3, 1)

        # Mutation probability
        mutation_prob_label = QLabel("Mutation Probability")
        self.mutation_prob_textbox = QLineEdit()
        self.mutation_prob_textbox.setText('0.1')
        self.mutation_prob_textbox.setPlaceholderText("Mutation Probability Value")
        parameters_layout.addWidget(mutation_prob_label, 4, 0)
        parameters_layout.addWidget(self.mutation_prob_textbox, 5, 0)

        # Add parameters group to left side of param_and_running_splitter
        widget_params = QWidget()
        params_layout = QVBoxLayout(widget_params)
        params_layout.addWidget(parameters_group)
        param_and_running_splitter.addWidget(widget_params)

        # Running info display
        self.running_info_textbox = QTextEdit()
        self.running_info_textbox.setPlaceholderText("Running Information")
        self.running_info_textbox.setFont(QFont("Courier", 10))
        param_and_running_splitter.addWidget(self.running_info_textbox)
        param_and_running_splitter.setSizes([self.width() // 2, self.width() // 2])

        # Output display
        self.output_textbox = QTextEdit()
        self.output_textbox.setPlaceholderText("Output Information")
        self.output_textbox.setFont(QFont("Courier", 10))
        splitter.addWidget(self.output_textbox)

        self.dataset_path = ""
        self.min_utility_textbox.setFocus()

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Dataset File")
        if file_path:
            self.dataset_path = file_path
            self.file_path_label.setText(f"Selected Database: {os.path.splitext(os.path.basename(self.dataset_path))[0]}")
            QMessageBox.information(
                self, "File Selected", f"Selected Database: {os.path.splitext(os.path.basename(self.dataset_path))[0]}"
            )
            self.min_utility_textbox.setFocus()

    def run_genetic_algorithm(self):
        try:
            if not self.dataset_path:
                raise ValueError(
                    "Dataset path is not set. Please select a dataset file."
                )

            self.reset_algorithm()
            min_utility = int(self.min_utility_textbox.text())
            generations = int(self.generations_textbox.text())
            population_size = int(self.population_size_textbox.text())
            crossover_prob = float(self.crossover_prob_textbox.text())
            mutation_prob = float(self.mutation_prob_textbox.text())

            # Validate crossover and mutation probabilities
            if not (0 < crossover_prob <= 1):
                raise ValueError(
                    "Crossover Probability must be greater than 0 and less than or equal to 1."
                )
            if not (0 < mutation_prob <= 1):
                raise ValueError(
                    "Mutation Probability must be greater than 0 and less than or equal to 1."
                )
            #Progress Dialog
            self.progress_dialog = QProgressDialog(
                    "Running Genetic Algorithm...", "Cancel", 0, 0, self)
            self.progress_dialog.setWindowTitle("Genetic Algorithm Progress")
            self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
            self.progress_dialog.setMinimumDuration(0)
            self.progress_dialog.canceled.connect(self.cancel_algorithm)
            
            #Call Worker
            self.worker = Worker(self.dataset_path, min_utility, generations, population_size, crossover_prob, mutation_prob)
            self.worker.progress_update.connect(self.update_progress_dialog)
            self.worker.finished.connect(self.genetic_algorithm_finished)
            self.worker.start()

            self.progress_dialog.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def reset_algorithm(self):
        if hasattr(self, "worker") and isinstance(self.worker, Worker):
            self.worker.cancel_execution()
            self.worker.wait()
            self.worker.reset_status()

    def cancel_algorithm(self):
        if hasattr(self, "worker") and isinstance(self.worker, Worker):
            self.worker.finished.disconnect(self.genetic_algorithm_finished)
            self.display_output(self.worker.ga)
            self.worker.cancel_execution()

    def genetic_algorithm_finished(self, result):
        if isinstance(result, Exception):
            QMessageBox.critical(self, "Error", f"An error occurred: {str(result)}")
        else:
            ga = result
            self.display_output(ga)
            self.worker.reset_status()
            if not self.worker.cancel_requested:
                QMessageBox.information(self, "Success", "Genetic algorithm executed successfully.")
        self.progress_dialog.close()

    def update_progress_dialog(self, text):
        self.progress_dialog.setLabelText(text)
        self.running_info_textbox.append(text)

    def display_output(self, ga):
        output_text = f"Total High-utility item-sets found: {len(ga.hui_sets)}\n--------------------------------------\n"
        for bits, fitness in ga.hui_sets:
            if fitness >= int(self.min_utility_textbox.text()):
                items = [i + 1 for i in range(len(bits)) if bits[i]]
                items_str = " ".join(map(str, items))
                output_text += f"{items_str} #UTIL: {fitness}\n"
        self.output_textbox.setText(output_text)
    def save_output_to_file(self):
        output_text = self.output_textbox.toPlainText()
        if output_text:
            file_dialog = QFileDialog()
            output_path, _ = file_dialog.getSaveFileName(
                self, "Save Output As", "", "Text Files (*.txt)"
            )
            if output_path:
                self.worker.ga.save_files(output_path)
                QMessageBox.information(self, "Success", "Output saved successfully.")
                self.refresh_fields()
        else:
            QMessageBox.warning(self, "Warning", "No output to save.")

    def refresh_fields(self):
        try:
            self.min_utility_textbox.clear()
            self.population_size_textbox.clear()
            self.generations_textbox.clear()
            self.crossover_prob_textbox.clear()
            self.mutation_prob_textbox.clear()
            self.output_textbox.clear()
            self.running_info_textbox.clear()
            self.dataset_path = ""
            self.file_path_label.clear()
            QMessageBox.information(self, "Refreshed", "All fields have been cleared.")
            self.min_utility_textbox.setFocus()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
