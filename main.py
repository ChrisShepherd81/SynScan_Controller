import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt, QCoreApplication
from PySide2.QtQml import QQmlApplicationEngine

from ViewModel import ViewModel
from SynScanProtocol import SynScanController
from TestController import TestController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    #controller = SynScanController("COM4")
    controller = TestController("COM4")
    view_model = ViewModel(controller)
    engine = QQmlApplicationEngine('view.qml')
    engine.rootContext().setContextProperty("viewModel", view_model)

    app.exec_()
    controller.close()


