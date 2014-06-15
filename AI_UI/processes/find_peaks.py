__author__ = 'msarahan'

from base import ProcessBase
from Absolute_Integrator import peak_finding


class PeakFindingProcess(ProcessBase):
    def __init__(self):
        super(PeakFindingProcess, self).__init__(peak_finding)

    def run(self, **kw):
        return peak_finding.peak_find(**kw)