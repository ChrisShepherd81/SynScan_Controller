from PySide2.QtCore import QObject, Slot, Property, Signal

from SynScanProtocol import SynScanController, AxisId

class ViewModel(QObject):
    def __init__(self, controller, parent=None):
        super(ViewModel, self).__init__(parent)
        self._controller = controller
        self._location = "unknown"
        self._connected = False

    locationChanged = Signal()
    def getLocation(self):
        if self._connected:
            latitude, longitude = self._controller.getLocation()
            return str(latitude) + ',' + str(longitude)
        return self._location

    def setLocation(self, value):
        self._location = value
        self.locationChanged.emit()

    location = Property(str, getLocation, setLocation, notify = locationChanged)

    @Slot(str)
    def connect(self, port):
        self._controller.connect(port)
        self._connected = True
        self.setLocation("connected")

    @Slot()
    def on_slewStop(self):
        self._controller.slew_fixed(AxisId.ALT_DEC_MOTOR, 0)
        self._controller.slew_fixed(AxisId.AZM_RA_MOTOR, 0)

    @Slot(int)
    def on_slewLeftButton(self, speed):
        self._controller.slew_fixed(AxisId.AZM_RA_MOTOR, -speed)

    @Slot(int)
    def on_slewRightButton(self, speed):
        self._controller.slew_fixed(AxisId.AZM_RA_MOTOR, speed)

    @Slot(int)
    def on_slewUpButton(self, speed):
        self._controller.slew_fixed(AxisId.ALT_DEC_MOTOR, speed)

    @Slot(int)
    def on_slewDownButton(self, speed):
        self._controller.slew_fixed(AxisId.ALT_DEC_MOTOR, -speed)
