__author__ = 'msarahan'

class ProcessBase(object):
    def __init__(self, module):
        super(ProcessBase, self).__init__()
        self.module = module

    def run(self, **kw):
        return self.module.run(**kw)