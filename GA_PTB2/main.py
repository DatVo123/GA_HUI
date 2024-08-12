from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QMessageBox,
    QGroupBox,
    QGridLayout,
)
import sys
from ga import GeneticAlgorithm  # Adjust import if you need other classes or functions


class GeneticAlgorithmGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Genetic Algorithm To Solve Level 2 Equations")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold; text-align: center; color: #00568b;"
        )

        layout.addWidget(title)

        # Main Layout
        main_layout = QHBoxLayout()

        # Additional Parameters Group Box
        additional_parameters_layout = QGridLayout()
        additional_parameters_layout.setSpacing(10)

        additional_parameters_group = QGroupBox("Additional Parameters")
        additional_parameters_group.setLayout(additional_parameters_layout)
        additional_parameters_group.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 10px;
            }
            """
        )

        # Add input fields for 'a', 'b', 'c' with default values and adjusted height
        self.a_input = QLineEdit()
        self.b_input = QLineEdit()
        self.c_input = QLineEdit()

        self.a_input.setFixedHeight(30)
        self.b_input.setFixedHeight(30)
        self.c_input.setFixedHeight(30)

        additional_parameters_layout.addWidget(QLabel("Parameter a:"), 0, 0)
        additional_parameters_layout.addWidget(self.a_input, 0, 1)
        additional_parameters_layout.addWidget(QLabel("Parameter b:"), 0, 2)
        additional_parameters_layout.addWidget(self.b_input, 0, 3)
        additional_parameters_layout.addWidget(QLabel("Parameter c:"), 1, 0)
        additional_parameters_layout.addWidget(self.c_input, 1, 1)

        # Equation Text Area
        self.equation_text = QTextEdit()
        self.equation_text.setReadOnly(True)
        self.equation_text.setStyleSheet("border: 1px solid #00568b; padding: 10px;")
        self.equation_text.setMinimumWidth(250)

        # Arrange Additional Parameters and Equation Text Area
        additional_parameters_container = QVBoxLayout()
        additional_parameters_container.addWidget(additional_parameters_group)
        additional_parameters_container.addWidget(self.equation_text)

        # Genetic Algorithm Parameters Group Box
        parameters_layout = QGridLayout()
        parameters_layout.setSpacing(10)

        parameters_group = QGroupBox("Genetic Algorithm Parameters")
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

        # Add input fields for genetic algorithm parameters with default values and adjusted height
        self.population_size_input = QLineEdit("5")
        self.individual_length_input = QLineEdit("5")
        self.generations_input = QLineEdit("5")
        self.crossover_rate_input = QLineEdit("0.7")
        self.mutation_rate_input = QLineEdit("0.1")

        self.population_size_input.setFixedHeight(30)
        self.individual_length_input.setFixedHeight(30)
        self.generations_input.setFixedHeight(30)
        self.crossover_rate_input.setFixedHeight(30)
        self.mutation_rate_input.setFixedHeight(30)

        parameters_layout.addWidget(QLabel("Population Size:"), 1, 0)
        parameters_layout.addWidget(self.population_size_input, 1, 1)
        parameters_layout.addWidget(QLabel("Individual Length:"), 0, 2)
        parameters_layout.addWidget(self.individual_length_input, 0, 3)
        parameters_layout.addWidget(QLabel("Generations:"), 0, 0)
        parameters_layout.addWidget(self.generations_input, 0, 1)
        parameters_layout.addWidget(QLabel("Crossover Rate:"), 1, 2)
        parameters_layout.addWidget(self.crossover_rate_input, 1, 3)
        parameters_layout.addWidget(QLabel("Mutation Rate:"), 2, 0)
        parameters_layout.addWidget(self.mutation_rate_input, 2, 1)

        # Arrange Parameters Group Box
        parameters_container = QVBoxLayout()
        parameters_container.addWidget(parameters_group)

        # Add containers to main layout
        main_layout.addLayout(additional_parameters_container)
        main_layout.addLayout(parameters_container)

        # Buttons Layout
        button_layout = QHBoxLayout()
        self.run_button = QPushButton("Run")
        self.reset_button = QPushButton("Reset")
        self.save_button = QPushButton("Save Output")

        self.style_buttons(self.run_button)
        self.style_buttons(self.reset_button)
        self.style_buttons(self.save_button)

        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.save_button)

        layout.addLayout(main_layout)
        layout.addLayout(button_layout)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("border: 1px solid #00568b; padding: 10px;")
        layout.addWidget(self.output_text)

        self.setLayout(layout)
        self.setWindowTitle("Genetic Algorithm Interface")
        self.setGeometry(100, 100, 800, 500)

        self.run_button.clicked.connect(self.run_algorithm)
        self.reset_button.clicked.connect(self.reset_fields)
        self.save_button.clicked.connect(self.save_output_to_file)

        # Connect input field changes to update the equation
        self.a_input.textChanged.connect(self.update_equation)
        self.b_input.textChanged.connect(self.update_equation)
        self.c_input.textChanged.connect(self.update_equation)

    def style_buttons(self, button):
        button.setStyleSheet(
            "background-color: #00568b; color: white; font-weight: bold;"
        )

    def update_equation(self):
        try:
            a = float(self.a_input.text())
            b = float(self.b_input.text())
            c = float(self.c_input.text())
            equation = f"x&sup2; "

            if b < 0:
                equation += f"- {-b}x "
            else:
                equation += f"+ {b}x "
            if c < 0:
                equation += f"- {-c} = 0"
            else:
                equation += f"+ {c} = 0"
            self.equation_text.setHtml(equation)
        except ValueError:
            self.equation_text.setPlainText("Invalid input for parameters.")

    def run_algorithm(self):
        try:
            population_size = int(self.population_size_input.text())
            individual_length = int(self.individual_length_input.text())
            generations = int(self.generations_input.text())
            crossover_rate = float(self.crossover_rate_input.text())
            mutation_rate = float(self.mutation_rate_input.text())
            a = float(self.a_input.text())
            b = float(self.b_input.text())
            c = float(self.c_input.text())

            # Create a GeneticAlgorithm instance and run it
            ga = GeneticAlgorithm(
                population_size,
                individual_length,
                a,
                b,
                c,
                crossover_rate,
                mutation_rate,
            )
            output = ga.run(generations)
            self.output_text.setPlainText(output)
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", f"Invalid input: {e}")

    def reset_fields(self):
        self.population_size_input.clear()
        self.individual_length_input.clear()
        self.generations_input.clear()
        self.crossover_rate_input.clear()
        self.mutation_rate_input.clear()
        self.a_input.clear()
        self.b_input.clear()
        self.c_input.clear()
        self.output_text.clear()
        self.equation_text.clear()

    def save_output_to_file(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Output File", "", "Text Files (*.txt);;All Files (*)"
        )

        if file_name:
            try:
                with open(file_name, "w") as file:
                    file.write(self.output_text.toPlainText())
                QMessageBox.information(self, "Success", "Output saved successfully.")

            except Exception as e:
                QMessageBox.warning(self, "Warning", f"An error occurred while saving the file: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeneticAlgorithmGUI()
    window.show()
    sys.exit(app.exec())
