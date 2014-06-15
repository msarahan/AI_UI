import sys

from PyQt4.QtGui import QApplication, QMainWindow, QVBoxLayout
from matplotlib.backends.backend_qt4agg import FigureCanvasAgg, NavigationToolbar2QTAgg

from widgets.progress_bar import AIProgressBar

class AIMainWindow(QMainWindow):
    def __init__(self):
        layout = QVBoxLayout()
        self.figure = FigureCanvasAgg()
        self.navigation = NavigationToolbar2QTAgg
        self.progress = AIProgressBar
        layout.addWidget(self.figure)
        layout.addWidget(self.navigation)
        layout.addWidget(self.progress)
        self.setCentralWidget(layout)

    def start_process(self):

app = QApplication(sys.argv)
app.exec_()