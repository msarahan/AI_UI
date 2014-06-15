__author__ = 'msarahan'

from PyQt4.QtGui import QProgressBar
from Absolute_Integrator.UI_Interface import progress_bar

class AIProgressBar(QProgressBar, progress_bar):
    def __init__(self, parent):
        super(AIProgressBar, self).__init__(parent)

    def set_title(self, title):
        """
        This class has no direct way of showing the title - store it locally anyway
        """
        pass

    def set_position(self, position):
        """
        Sets the current thing the progress bar is on
        """
        self.setValue(position)

    def set_end(self, end):
        """
        Sets the total number of things for the progress bar to count to
        """
        self.setMaximum(end)