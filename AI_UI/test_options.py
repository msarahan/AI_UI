__author__ = 'msarahan'

from PyQt4.QtGui import QApplication

import widgets.options
from Absolute_Integrator.peak_finding import ranger

import sys

app = QApplication(sys.argv)
dialog = widgets.options.AIOptionsDialog(ranger.options)
dialog.show()
app.exec_()


