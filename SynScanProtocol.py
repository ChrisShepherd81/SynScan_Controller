import serial, datetime
from enum import Enum

class UsageError(Exception):
    pass

class ProtocolError(Exception):
    pass

class PassthroughError(Exception):
    pass

class Model(Enum):
    gps_series  =  1
    i_series    =  3
    i_series_se =  4
    cge         =  5
    advanced_gt =  6
    slt         =  7
    cpc         =  9
    gt          = 10
    se45        = 11
    se68        = 12
    lcm         = 15

class Command(Enum):
    # All  commands start with a single ASCII character.
    GET_POSITION_RA_DEC           = 'E' # 1.2+
    GET_POSITION_RA_DEC_PRECISE   = 'e' # 1.6+
    GET_POSITION_AZM_ALT          = 'Z' # 1.2+
    GET_POSITION_AZM_ALT_PRECISE  = 'z' # 2.2+
    GOTO_POSITION_RA_DEC          = 'R' # 1.2+
    GOTO_POSITION_RA_DEC_PRECISE  = 'r' # 1.6+
    GOTO_POSITION_AZM_ALT         = 'B' # 1.2+
    GOTO_POSITION_AZM_ALT_PRECISE = 'b' # 2.2+
    SYNC                          = 'S' # 4.10+
    SYNC_PRECISE                  = 's' # 4.10+
    GET_TRACKING_MODE             = 't' # 2.3+
    SET_TRACKING_MODE             = 'T' # 1.6+
    GET_LOCATION                  = 'w' # 2.3+
    SET_LOCATION                  = 'W' # 2.3+
    GET_TIME                      = 'h' # 2.3+
    SET_TIME                      = 'H' # 2.3+
    GET_VERSION                   = 'V' # 1.2+
    GET_MODEL                     = 'm' # 2.2+
    ECHO                          = 'K' # 1.2+
    GET_ALIGNMENT_COMPLETE        = 'J' # 1.2+
    GET_GOTO_IN_PROGRESS          = 'L' # 1.2+
    CANCEL_GOTO                   = 'M' # 1.2+
    PASSTHROUGH                   = 'P' # 1.6+ this includes slewing commands, 'get device version' commands, GPS commands, and RTC commands

class PassthroughCommand(Enum):
    MOTOR_SLEW_POSITIVE_VARIABLE_RATE =   6
    MOTOR_SLEW_NEGATIVE_VARIABLE_RATE =   7
    MOTOR_SLEW_POSITIVE_FIXED_RATE    =  36
    MOTOR_SLEW_NEGATIVE_FIXED_RATE    =  37
    GET_DEVICE_VERSION                = 254

class CoordinateMode(Enum):
    RA_DEC  = 1 # Right Ascension / Declination
    AZM_ALT = 2 # Azimuth/Altitude

class TrackingMode(Enum):
    OFF      = 0
    ALT_AZ   = 1
    EQ_NORTH = 2
    EQ_SOUTH = 3

class AxisId(Enum):
    AZM_RA_MOTOR  = 16
    ALT_DEC_MOTOR = 17


class SynScanController:

    def __init__(self):
        self._device = None

    def connect(self, port):
        if isinstance(port, str):
            device = serial.Serial(
                    port             = port,
                    baudrate         = 9600,
                    bytesize         = serial.EIGHTBITS,
                    parity           = serial.PARITY_NONE,
                    stopbits         = serial.STOPBITS_ONE,
                    timeout          = 3.500,
                    xonxoff          = 0,
                    rtscts           = False,
                    writeTimeout     = None,
                    dsrdtr           = False,
                    interCharTimeout = None
                )
            self._device = device
        else:
            raise UsageError("")

    @property
    def device(self):
        return self._device

    def close(self):
        if self._device != None:
            return self._device.close()

    def _write_binary(self, request):
        return self._device.write(request)

    @staticmethod
    def _to_bytes(arg):

        if isinstance(arg, Command) or isinstance(arg, TrackingMode) or isinstance(arg, AxisId) or isinstance (arg, PassthroughCommand):
           arg = arg.value

        if isinstance(arg, int):
            arg = bytes([arg])

        if isinstance(arg, str):
            arg = bytes(arg, "ascii")

        if not isinstance(arg, bytes):
            arg = b''.join(SynScanController._to_bytes(e) for e in arg)

        return arg

    def _write(self, *args):
        msg = SynScanController._to_bytes(args)
        # print("message to be written:", msg)
        return self._write_binary(msg)

    def _read_binary(self, expected_response_length, check_and_remove_trailing_hash = True):

        if not (isinstance(expected_response_length, int) and expected_response_length > 0):
            raise UsageError("_read_binary() failed: incorrect value for parameter 'expected_response_length': {}".format(repr(expected_response_length)))

        if not isinstance(check_and_remove_trailing_hash, bool):
            raise UsageError("_read_binary() failed: incorrect value for parameter 'check_and_remove_trailing_hash': {}".format(repr(check_and_remove_trailing_hash)))

        response = self._device.read(expected_response_length)

        if len(response) != expected_response_length:
            raise ProtocolError("read_binary() failed: actual response length ({}) not equal to expected response length ({})".format(len(response), expected_response_length))

        if check_and_remove_trailing_hash:
            if not response.endswith(b'#'):
                print(response)
                raise ProtocolError("read_binary() failed: response does not end with hash character (ASCII 35)")
            # remove the trailing hash character.
            response = response[:-1]

        return response

    def _read_ascii(self, expected_response_length, check_and_remove_trailing_hash = True):
        response = self._read_binary(expected_response_length, check_and_remove_trailing_hash)
        response = response.decode("ascii")
        return response

    # Public API starts here

    def getPosition(self, coordinateMode = CoordinateMode.RA_DEC, highPrecisionFlag = False):

        if highPrecisionFlag:
            command = Command.GET_POSITION_AZM_ALT_PRECISE if (coordinateMode == CoordinateMode.AZM_ALT) else Command.GET_POSITION_RA_DEC_PRECISE
            expected_response_length = 8 + 1 + 8 + 1
            denominator = 0x100000000
        else:
            command = Command.GET_POSITION_AZM_ALT if (coordinateMode == CoordinateMode.AZM_ALT) else Command.GET_POSITION_RA_DEC
            expected_response_length = 4 + 1 + 4 + 1
            denominator = 0x10000

        self._write(command)

        response = self._read_ascii(expected_response_length = expected_response_length, check_and_remove_trailing_hash = True)
        response = response.split(",")
        if not (len(response) == 2):
            raise ProtocolError("getPosition() failed: unexpected response ({})".format(response))

        response = (360.0 * int(response[0], 16) / float(denominator), 360.0 * int(response[1], 16) / float(denominator))
        return response

    def gotoPosition(self, firstCoordinate, secondCoordinate, coordinateMode = CoordinateMode.AZM_ALT, highPrecisionFlag = True):

        # Initiate a "GoTo" command.

        if highPrecisionFlag:
            command = Command.GOTO_POSITION_AZM_ALT_PRECISE if (coordinateMode == CoordinateMode.AZM_ALT) else Command.GOTO_POSITION_RA_DEC_PRECISE
            firstCoordinate  = round(firstCoordinate  / 360.0 * 0x100000000)
            secondCoordinate = round(secondCoordinate / 360.0 * 0x100000000)
            coordinates = "{:08x},{:08x}".format(firstCoordinate, secondCoordinate)
        else:
            command = Command.GOTO_POSITION_AZM_ALT if (coordinateMode == CoordinateMode.AZM_ALT) else Command.GOTO_POSITION_RA_DEC
            firstCoordinate  = round(firstCoordinate  / 360.0 * 0x10000)
            secondCoordinate = round(secondCoordinate / 360.0 * 0x10000)
            coordinates = "{:04x},{:04x}".format(firstCoordinate, secondCoordinate)

        self._write(command, coordinates)

        # Response is a single hash ('#') character. Drop it.
        response = self._read_binary(expected_response_length = 0 + 1, check_and_remove_trailing_hash = True)

        return None

    def sync(self, firstCoordinate, secondCoordinate, highPrecisionFlag = True):

        # sync always works in RA/DEC coordinates

        if highPrecisionFlag:
            command = Command.SYNC_PRECISE
            firstCoordinate  = round(firstCoordinate  / 360.0 * 0x100000000)
            secondCoordinate = round(secondCoordinate / 360.0 * 0x100000000)
            coordinates = "{}{:08x},{:08x}".format(firstCoordinate, secondCoordinate)
        else:
            command = Command.SYNC
            firstCoordinate  = round(firstCoordinate  / 360.0 * 0x10000)
            secondCoordinate = round(secondCoordinate / 360.0 * 0x10000)
            coordinates = "{}{:04x},{:04x}".format(firstCoordinate, secondCoordinate)

        self._write(command, coordinates)

        # Response is a single hash ('#') character. Drop it.
        response = self._read_binary(expected_response_length = 0 + 1, check_and_remove_trailing_hash = True)

        return None

    def getTrackingMode(self):

        command = Command.GET_TRACKING_MODE
        self._write(command)

        response = self._read_binary(expected_response_length = 1 + 1, check_and_remove_trailing_hash = True)

        tracking_mode = response[0]

        return tracking_mode

    def setTrackingMode(self, tracking_mode):

        if not isinstance(tracking_mode, TrackingMode):
            raise UsageError("_read_binary() failed: incorrect value for parameter 'tracking_mode': {}".format(repr(tracking_mode)))

        command = Command.GET_TRACKING_MODE

        self._write(command, tracking_mode)

        # Response is a single hash ('#') character. Drop it.
        response = self._read_binary(expected_response_length = 0 + 1, check_and_remove_trailing_hash = True)

        return None

    def getLocation(self):

        command = Command.GET_LOCATION
        self._write(command)

        response = self._read_binary(expected_response_length = 8 + 1, check_and_remove_trailing_hash = True)

        latitude_degrees = response[0]
        latitude_minutes = response[1]
        latitude_seconds = response[2]
        latitude_sign    = response[3] # 0 == north, 1 == south

        longitude_degrees = response[4]
        longitude_minutes = response[5]
        longitude_seconds = response[6]
        longitude_sign    = response[7] # 0 == east, 1 == west

        latitude_seconds = latitude_degrees * 3600 + latitude_minutes * 60 + latitude_seconds
        if latitude_sign != 0:
            latitude_seconds = -latitude_seconds

        longitude_seconds = longitude_degrees * 3600 + longitude_minutes * 60 + longitude_seconds
        if longitude_sign != 0:
            longitude_seconds = -longitude_seconds

        latitude = latitude_seconds / 3600.0
        longitude = longitude_seconds / 3600.0

        return (latitude, longitude)

    def setLocation(self, latitude, longitude):

        # Fix latitude

        latitude_seconds = round(latitude * 3600)
        if latitude_seconds >= 0:
            latitude_sign = 0
        else:
            latitude_sign = 1
            latitude_seconds = -latitude_seconds

        # Fix longitude

        longitude_seconds = round(longitude * 3600)
        if longitude_seconds >= 0:
            longitude_sign = 0
        else:
            longitude_sign = 1
            longitude_seconds = -longitude_seconds

        # Reduce to Degrees/Minutes/Seconds

        latitude_degrees = latitude_seconds // 3600 ; latitude_seconds %= 3600
        latitude_minutes = latitude_seconds // 60   ; latitude_seconds %= 60

        longitude_degrees = longitude_seconds // 3600 ; longitude_seconds %= 3600
        longitude_minutes = longitude_seconds // 60   ; longitude_seconds %= 60

        # Synthesize "W" request

        request = [
                Command.SET_LOCATION,
                latitude_degrees, latitude_minutes, latitude_seconds, latitude_sign,
                longitude_degrees, longitude_minutes, longitude_seconds, longitude_sign
            ]

        self._write(request)

        # Response is a single hash ('#') character. Drop it.
        response = self._read_binary(expected_response_length = 0 + 1, check_and_remove_trailing_hash = True)

        return None

    def getTime(self):

        request = Command.GET_TIME
        self._write(request)

        response = self._read_binary(expected_response_length = 8 + 1, check_and_remove_trailing_hash = True)

        hour   = response[0] # 24 hour clock
        minute = response[1]
        second = response[2]
        month  = response[3] # jan == 1, dec == 12
        day    = response[4] # 1 .. 31
        year   = response[5] # year minus 2000
        zone   = response[6] # 2-complement of timezone (hour offset from UTC)
        dst    = response[7] # 1 to enable DST, 0 for standard time.

        year += 2000

        if zone >= 128: # take care of negative zone offsets
            zone -= 256

        zone = datetime.timedelta(hours = zone)

        dst = (dst != 0)

        print(year, month, day, hour, minute, second)

        tzinfo = datetime.timezone(zone) # simple timezone with offset relative to UTC
        timestamp = datetime.datetime(year, month, day, hour, minute, second, 0, tzinfo)

        return (timestamp, dst)

    def setTime(self, timestamp, dst):

        hour   = timestamp.hour
        minute = timestamp.minute
        second = timestamp.second
        month  = timestamp.month
        day    = timestamp.day
        year   = timestamp.year - 2000

        zone = round(timestamp.utcoffset() / datetime.timedelta(hours = 1))
        if zone < 0:
            zone += 256

        request = [Command.SET_TIME, hour, minute, second, month, day, year, zone, dst]
        self._write(request)

        # Response is a single hash ('#') character. Drop it.
        response = self._read_binary(expected_response_length = 0 + 1, check_and_remove_trailing_hash = True)

        return None

    def getVersion(self):
        request = Command.GET_VERSION
        self._write(request)
        response = self._read_binary(expected_response_length = 2 + 1, check_and_remove_trailing_hash = True)
        response = (response[0], response[1])
        return response



    def getModel(self):
        request = Command.GET_MODEL
        self._write(request)
        response = self._read_binary(expected_response_length = 1 + 1, check_and_remove_trailing_hash = True)
        response = response[0]
        return response



    def echo(self, c):
        if not isinstance(c, int) and (0 <= c <= 255):
            raise UsageError("echo() failed: incorrect 'c' parameter")
        request = [Command.ECHO, c]
        self._write(request)
        response = self._read_binary(expected_response_length = 1 + 1, check_and_remove_trailing_hash = True)
        response = response[0]
        if not(response == c):
            raise ProtocolError("echo() failed: unexpected response ({})".format(repr(response)))
        return None

    def getAlignmentComplete(self):
        request = [Command.GET_ALIGNMENT_COMPLETE]
        self._write(request)
        response = self._read_binary(expected_response_length = 1 + 1, check_and_remove_trailing_hash = True)
        response = response[0]
        if not response in [0, 1]:
            raise ProtocolError("getAlignmentComplete() failed: unexpected response ({})".format(repr(response)))
        response = (response == 1) # convert to bool
        return response


    def getGotoInProgress(self):
        request = [Command.GET_GOTO_IN_PROGRESS]
        self._write(request)
        response = self._read_ascii(expected_response_length = 1 + 1, check_and_remove_trailing_hash = True)
        response = response[0]
        # Response should be ASCII '0' or '1'
        if not response in ['0', '1']:
            raise ProtocolError("getGotoInProgress() failed: unexpected response ({})".format(repr(response)))
        response = (response == '1') # convert to bool
        return response


    def cancelGoto(self):
        request = [Command.CANCEL_GOTO]
        self._write(request)
        response = self._read_binary(expected_response_length = 0 + 1, check_and_remove_trailing_hash = True)
        return None


    # The commands below are low-level 'pass-through' commands that are handled by the specified
    # sub-devices connected to the hand controller via the 6-pin RJ-12 port.

    def passthrough(self, axisId, command, expected_response_bytes):

        if not isinstance(axisId, AxisId):
            raise UsageError("incorrect value for parameter 'axisId': {}".format(repr(axisId)))

        if not (isinstance(expected_response_bytes, int) and expected_response_bytes >= 0):
            raise UsageError("passthrough() failed: incorrect value for parameter 'expected_response_bytes': {}".format(repr(expected_response_bytes)))

        command_bytes = SynScanController._to_bytes(command)

        if not (1 <= len(command_bytes) <= 4):
            raise UsageError("expected between 1 and 4 command bytes for passthrough command (received {})".format(len(command)))

        padding = bytes(4 - len(command_bytes))

        request = [Command.PASSTHROUGH, len(command_bytes), axisId, command_bytes, padding, expected_response_bytes]

        self._write(request)

        # Receive response.
        try:
            response = self._read_binary(expected_response_length = expected_response_bytes + 1, check_and_remove_trailing_hash = True)
        except ProtocolError as exception:
            # read away extra hash
            extra_hash = self._device.read(1)
            if extra_hash != b"#":
                raise ProtocolError("extra hash not found") from exception

            raise PassthroughError("No valid response from device {}".format(AxisId.name))

        return response

    def slew_fixed(self, axisId, rate):
        if axisId not in [AxisId.AZM_RA_MOTOR, AxisId.ALT_DEC_MOTOR]:
            raise UsageError("slew command only supported for motors.")
        if not (isinstance(rate, int) and -9 <= rate <= +9):
            raise UsageError("slew_fixed() failed: incorrect value for parameter 'rate': {}".format(repr(rate)))

        if rate >= 0:
            command = PassthroughCommand.MOTOR_SLEW_POSITIVE_FIXED_RATE
        else:
            command = PassthroughCommand.MOTOR_SLEW_NEGATIVE_FIXED_RATE
            rate = -rate

        self.passthrough(axisId, [command, rate], expected_response_bytes = 0)

    def slew_variable(self, AxisId, rate):
        if AxisId not in [AxisId.AZM_RA_MOTOR, AxisId.ALT_DEC_MOTOR]:
            raise UsageError("slew command only supported for motors.")

        # rate is assumed to be in in degrees / second
        rate = round(rate * 3600.0 * 4)

        if rate >= 0:
            command = PassthroughCommand.MOTOR_SLEW_POSITIVE_VARIABLE_RATE
        else:
            command = PassthroughCommand.MOTOR_SLEW_NEGATIVE_VARIABLE_RATE
            rate = -rate

        if not (0 <= rate <= 65535):
            raise UsageError("variable rate out of range.")

        self.passthrough(AxisId, [command, rate // 256, rate % 256], expected_response_bytes = 0)

    def getDeviceVersion(self, AxisId):

        (versionMajor, versionMinor) = self.passthrough(AxisId, command = PassthroughCommand.GET_DEVICE_VERSION, expected_response_bytes = 2)

        return (versionMajor, versionMinor)

