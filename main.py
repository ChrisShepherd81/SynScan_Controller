import sys
import serial.tools.list_ports

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QStringListModel
from PySide2.QtQml import QQmlApplicationEngine

from ViewModel import ViewModel
from SynScanProtocol import SynScanController
from TestController import TestController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    com_ports = QStringListModel(([comport.device for comport in serial.tools.list_ports.comports()]))
    controller = SynScanController()
    #controller = TestController("COM4")
    view_model = ViewModel(controller)

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("comPortsModel", com_ports)
    engine.rootContext().setContextProperty("viewModel", view_model)
    engine.load('MainView.qml')

    app.exec_()
    controller.close()


