# This Python file uses the following encoding: utf-8
from PySide2 import QtCore
from PySide2 import QtWidgets

class TestController:
    def __init__(self, com_port):
        pass

    def close(self):
        pass

    def slew_fixed(axisId, speed):
        print("Slew axis " + str(axisId) + " with speed " + str(speed))

