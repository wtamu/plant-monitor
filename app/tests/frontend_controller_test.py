import unittest
from app.data import ArduinoDAO
import time
from app.controllers import FrontEndController, ArduinoController

class FrontEndControllerTest(unittest.TestCase):
    def setUp(self):
        self._arduinoDAO = ArduinoDAO("Arduino Endpoint")
        self._arduinoCtrl = ArduinoController(self._arduinoDAO)
        self._frontEndCtrl = FrontEndController(self._arduinoCtrl)
        self._sensorModel = self._arduinoCtrl.getSensorDataModel()

    def testEmitArduinoSensorStream(self):
        if not self._frontEndCtrl.isAlive():
            print("\n -- testing arduino stream emit thread -- \n")
            self._frontEndCtrl.start()
            while True:
                print("\nmodel updated from thread:")
                print(str(self._sensorModel))
                time.sleep(1)


if __name__=='__main__':
    frontEndCtrlTest = FrontEndControllerTest()
    frontEndCtrlTest.setUp()
    frontEndCtrlTest.testEmitArduinoSensorStream()



