from PySide2.QtCore import QObject, Slot, Property, Signal

from SynScanProtocol import SynScanController, AxisId

import threading
import time

class ViewModel(QObject):
    def __init__(self, controller, parent=None):
        super(ViewModel, self).__init__(parent)
        self._controller = controller
        self._connected = False
        self._positionUpdaterThread = None

    locationChanged = Signal()
    def getLocation(self):
        if self._connected:
            latitude, longitude = self._controller.getLocation()
            return str(latitude) + ',' + str(longitude)
        return "disconnected"

    def updateLocation(self):
        self.locationChanged.emit()

    location = Property(str, getLocation, notify = locationChanged)

    positionChanged = Signal()
    def getPosition(self):
        if self._connected:
            ra, dec = self._controller.getPosition()
            return "RA: " + str(ra) + ", DEC: " + str(dec)
        return "disconnected"

    def updatePosition(self):
        self.positionChanged.emit()

    position = Property(str, getPosition, notify = positionChanged)

    def positionUpdater(self):
        while(self._connected):
            self.updatePosition()
            time.sleep(1)

    connectionStateChanged = Signal()
    @Slot(str)
    def connect(self, port):
        if not self._connected:
            self._controller.connect(port)
            self._connected = True
            self.connectionStateChanged.emit()

        self.updateLocation()
        self.updatePosition()
        #self._positionUpdaterThread = threading.Thread(target=self.positionUpdater)
        #self._positionUpdaterThread.start()

    def getConnectionState(self):
        return self._connected

    connected = Property(bool, getConnectionState, notify = connectionStateChanged)

    @Slot()
    def disconnect(self):
        if self._connected:
            self._controller.close()
            self._connected = False
            self.connectionStateChanged.emit()
        self.updateLocation()
        self.updatePosition()


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
