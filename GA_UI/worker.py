from PyQt6.QtCore import QThread, pyqtSignal
from gaForUI import GeneticAlgorithm


class Worker(QThread):
    progress_update = pyqtSignal(str)
    finished = pyqtSignal(object)

    def __init__(self, dataset_path, min_utility, generations, population_size, crossover_prob, mutation_prob):
        super().__init__()
        self.ga = GeneticAlgorithm(dataset_path, min_utility, generations, population_size, crossover_prob,mutation_prob)
        self.cancel_requested = False

    def run(self):
        try:
            self.ga.progress_update.connect(self.progress_update.emit)
            self.ga.execute()
            if self.cancel_requested:
                self.finished.emit(None)
                self.reset_status()
            else:
                self.finished.emit(self.ga)
        except Exception as e:
            self.finished.emit(None)

    def cancel_execution(self):
        self.cancel_requested = True
        self.ga.cancel_requested = True

    def reset_status(self):
        self.cancel_requested = False
        