__author__ = 'msarahan'

from PyQt4.QtGui import QApplication, QMainWindow

import widgets.options
from Absolute_Integrator import peak_finding

import sys

app = QApplication(sys.argv)
dialog = QMainWindow()
dialog.setCentralWidget(widgets.options.AIModuleWidget(peak_finding))
dialog.show()
app.exec_()


