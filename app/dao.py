import functools
import serial

def singleton(cls):
    instances = dict()
    @functools.wraps(cls)
    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton



@singleton
class ArduinoDAO(object):
    ''' A single instance of this class is needed to access the arduino via USB port,
        and stream its serial output.
    '''
    def __init__(self, path):
        self._val = path
        self._ser = serial.Serial(self._val)
        self._outBytes = None

    def openPort(self):
        self._ser.open()
        return self._ser.is_open

    def closePort(self):
        self._ser.close()
        return not self._ser.is_open

    def serialOut(self):
        while self._ser.is_open:
            self.update()
            yield self._outBytes.decode("utf-8", "ignore")

    def update(self):
        self._outBytes = self._ser.readline()

    def serialIn(self, *args):
        for n in args:
            self._ser.write(n)

    def getValue(self):
        return self._val


@singleton
class UserDAO(object):
    def __init__(self, val):
        self._val = val

    def getValue(self):
        return self._val
