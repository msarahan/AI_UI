__author__ = 'msarahan'

from PyQt4.QtGui import QDialog, QGridLayout, QLabel, QLineEdit, QCheckBox, QPushButton
import functools

"""
This file maps an options dictionary presented by the AI library into a series
of input widgets.  These are embedded in a dialog that can be in turn embedded into a window.
"""

class AIOptionsDialog(QDialog):
    def __init__(self, options, parent=None):
        super(AIOptionsDialog, self).__init__(parent)
        grid = QGridLayout()
        self.widgets = dict()
        has_auto = False
        for row, option in enumerate(options):
            # offset of 1 reserves space for the heading
            row += 1
            # create the appropriate widget
            widget = AIOptionsDialog.get_widget(options[option])
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
                    checkbox.stateChanged.connect(functools.partial(AIOptionsDialog.toggle_auto_widget, widget, checkbox.isChecked))
                    grid.addWidget(checkbox, row, 2)
                    self.widgets[option]["auto"] = checkbox
                    has_auto=True
        grid.addWidget(QLabel("Option"), 0, 0)
        grid.addWidget(QLabel("Value"), 0, 1)
        if has_auto:
            grid.addWidget(QLabel("Auto"), 0, 2)
        button = QPushButton("output")
        button.clicked.connect(self.get_options_dict)
        grid.addWidget(button, row+1, 1)
        self.setLayout(grid)

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
