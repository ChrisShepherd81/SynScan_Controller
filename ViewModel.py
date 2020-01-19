import sys
from PySide2.QtCore import QObject, Slot, qDebug

from SynScanProtocol import SynScanController, AxisId

class ViewModel(QObject):
    def __init__(self, controller):
        QObject.__init__(self, None)
        self.controller = controller

    @Slot()
    def on_slewStop(self):
        qDebug("on_slewStop()")
        self.controller.slew_fixed(AxisId.ALT_DEC_MOTOR, 0)
        self.controller.slew_fixed(AxisId.AZM_RA_MOTOR, 0)

    @Slot(int)
    def on_slewLeftButton(self, speed):
        qDebug("on_slewLeftButton(speed=" + str(speed) +")")
        self.controller.slew_fixed(AxisId.AZM_RA_MOTOR, -speed)

    @Slot(int)
    def on_slewRightButton(self, speed):
        qDebug("on_slewRightButton(speed=" + str(speed) +")")
        self.controller.slew_fixed(AxisId.AZM_RA_MOTOR, speed)

    @Slot(int)
    def on_slewUpButton(self, speed):
        qDebug("on_slewUpButton(speed=" + str(speed) +")")
        self.controller.slew_fixed(AxisId.ALT_DEC_MOTOR, speed)

    @Slot(int)
    def on_slewDownButton(self, speed):
        qDebug("on_slewDownButton(speed=" + str(speed) +")")
        self.controller.slew_fixed(AxisId.ALT_DEC_MOTOR, -speed)
