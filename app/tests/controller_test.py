import unittest
from app import dao
from app.controllers import ArduinoController

class ArduinoControllerTest(unittest.TestCase):
    def setUp(self):
        self.arduinoEndpoint = dao.ArduinoDAO("/dev/ttyACM0")
        self.controller = ArduinoController(arduinoDAO=self.arduinoEndpoint)

    @unittest.skip
    def testAverageGenerator(self):
        averager = self.controller.averageGen()
        next(averager)
        testVals = [23, 23434, 45,2 ,424,245,6 ,646,346,25,77,34246,73,6]
        for i in testVals:
            avg = averager.send(i)
            print(avg)

    def testOutStream(self):
        for x in self.controller.readArduino():
            print(f"\nyield value from controller: {x}")


if __name__ == '__main__':
    ctrlTest = ArduinoControllerTest()
    ctrlTest.setUp()
    # ctrlTest.testAverageGenerator()
    ctrlTest.testOutStream()

