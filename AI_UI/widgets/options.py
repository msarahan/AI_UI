__author__ = 'msarahan'

from PyQt4.QtGui import QWidget, QGridLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QComboBox, QVBoxLayout, QSpacerItem
import functools


"""
This file maps an options dictionary presented by the AI library into a series
of input widgets.  These are embedded in a widget that can be in turn embedded into other widgets or a window.  It's
probably best not to use this directly, but rather to use the AIModuleWidget below, which handles creation of these
options widgets based on which method is currently selected.
"""
class AIOptionsWidget(QWidget):
    def __init__(self, options, parent=None):
        super(AIOptionsWidget, self).__init__(parent)
        grid = QGridLayout()
        self.widgets = dict()
        has_auto = False
        for row, option in enumerate(options):
            # offset of 1 reserves space for the heading
            row += 1
            # create the appropriate widget
            widget = AIOptionsWidget.get_widget(options[option])
            if widget is not None:
                self.widgets[option] = dict()
                # create the label for the thing
                grid.addWidget(QLabel(option), row, 0)
                grid.addWidget(widget, row, 1)
                self.widgets[option]["value"] = widget
                self.widgets[option]["type"] = options[option]["type"]
                # create the tooltip with the description of purpose
                if "purpose" in options[option]:
                    self.widgets[option]["value"].setToolTip(options[option]["purpose"])
                # add additional checkbox for auto option if present
                if "has_auto" in options[option]:
                    # Create the auto checkbox if appropriate
                    checkbox = QCheckBox()
                    if "default" in options[option] and options[option]["default"] == "auto":
                        checkbox.setChecked(True)
                        widget.setText("0")
                    # disable the entry widget if the auto checkbox is checked
                    widget.setEnabled(not checkbox.isChecked())
                    # disable the entry is the auto checkbox is checked
                    checkbox.stateChanged.connect(functools.partial(AIOptionsWidget.toggle_auto_widget, widget, checkbox.isChecked))
                    grid.addWidget(checkbox, row, 2)
                    self.widgets[option]["auto"] = checkbox
                    has_auto=True
        grid.addWidget(QLabel("Option"), 0, 0)
        grid.addWidget(QLabel("Value"), 0, 1)
        if has_auto:
            grid.addWidget(QLabel("Auto"), 0, 2)
        button = QPushButton("output")
        button.clicked.connect(self.get_options_dict)
        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addStretch(1)
        vbox.addWidget(button)
        self.setLayout(vbox)

    @staticmethod
    def toggle_auto_widget(widget, enabled):
        widget.setEnabled(not enabled())

    @staticmethod
    def get_widget(option_dict):
        if "type" not in option_dict:
            return None
            raise ValueError("option dict needs to include a 'type' key so that I know what widget to create!")
        option_type = str(option_dict["type"])
        if option_type == "bool":
            widget = QCheckBox()
            # set the default value, if any
            if "default" in option_dict:
                widget.setChecked(bool(option_dict["default"]))
        else:
            widget = QLineEdit()
            # set the default value, if any
            if "default" in option_dict:
                widget.setText(str(option_dict["default"]))
        return widget

    def get_options_dict(self):
        options = dict()
        for option, _dict in self.widgets.iteritems():
            if "auto" in _dict and _dict["auto"].isChecked():
                options[option] = "auto"
            else:
                if _dict["type"] == "bool":
                    value = _dict["value"].isChecked()
                else:
                    value = _dict["value"].text()
                value = _dict["type"] + "(" + str(value) + ")"
                options[option] = eval(value)
        print options
        return options

"""
This class encapsulates the group of methods for a given processing step.  It lists all available methods in a combobox,
then presents the options for the selected method.  When dispatching a step to run, call the get_options_dict method
to obtain the set of parameters to pass to the run function.
"""
class AIModuleWidget(QWidget):
    def __init__(self, module, parent=None):
        super(AIModuleWidget, self).__init__(parent)
        self.module = module
        methods_combobox = QComboBox()
        methods_combobox.addItems(module.list_methods())
        methods_combobox.currentIndexChanged.connect(functools.partial(self.change_method, methods_combobox.currentText))
        self.layout = QVBoxLayout()
        self.layout.addWidget(methods_combobox)
        self._options = None
        self.change_method(module.get_default_method)
        self.setLayout(self.layout)

    def change_method(self, method):
        if self._options is not None:
            self._options.setParent(None)
        self._options = AIOptionsWidget(self.module.list_options(str(method())))
        self.layout.addWidget(self._options)

    def get_options_dict(self):
        return self._options.get_options_dict()