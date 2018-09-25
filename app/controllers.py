import json
from threading import Thread


class ArduinoController(object):
    def __init__(self, arduinoDAO, userDAO=None):
        self._arduinoDAO = arduinoDAO
        self._usrDAO = userDAO
        self._sensorData = SensorOutputModel()
        self._sensorJson = None
        # a list of generators for running averages
        self._avgGenList = [ self.averageGen() for x in range(0, 5) ]
        for g in self._avgGenList: next(g)

    def openArduinoConnection(self):
        self._arduinoDAO.openPort()

    def closeArduinoConnection(self):
        self._arduinoDAO.closePort()

    def readArduino(self):
        ''' update sensor data with incoming json from arduino.'''
        for x in self._arduinoDAO.serialOut():
            try:
                self._sensorJson = json.loads(x)
                self.__updateSensorData(self._sensorJson)
                yield self._sensorData
            except json.decoder.JSONDecodeError:
                pass

    def averageGen(self):
        '''generates a running average '''
        total, avg, count = 0, 0, 0
        while True:
            val = yield avg
            total += val
            count += 1
            avg = total / count

    def getAvgTemp(self, scale=None):
        if scale:
            scale = scale.lower()
            if scale == 'c':
                return self._sensorData.temperature['c']
            if scale == 'f':
                return self._sensorData.temperature['f']
            if scale == 'k':
                return self._sensorData.temperature['k']

    def getAvgIllum(self):
        return self._sensorData.illuminance

    def getAvgSoilMoisture(self):
        return self._sensorData.soilMoisture

    def getSensorDataModel(self):
        return self._sensorData

    def getSensorJson(self):
        return self._sensorJson

    def __updateSensorData(self, data):
        self._sensorData.temperature['c'] = round(self._avgGenList[0].send(data['temperature']['c']), 2)
        self._sensorData.temperature['f'] = round(self._avgGenList[1].send(data['temperature']['f']), 2)
        self._sensorData.temperature['k'] = round(self._avgGenList[2].send(data['temperature']['k']), 2)
        self._sensorData.illuminance = round(self._avgGenList[3].send(data['light_level']), 2)
        self._sensorData.soilMoisture = round(self._avgGenList[4].send(data['soil_moisture']), 2)


class SensorOutputModel(object):
    def __init__(self):
        self.temperature = { 'c': None, 'f': None, 'k': None }
        self.soilMoisture = None
        self.illuminance = None

    def __str__(self):
        ctemp = self.temperature['c']
        ftemp = self.temperature['f']
        ktemp = self.temperature['k']
        return f'\nTemperature \n{ctemp} ºC \n{ftemp} ºF \n{ktemp} ºK ' \
                f'\nlight: {self.illuminance} \nsoil moisture: {self.soilMoisture}'


class FrontEndController(Thread):
    def __init__(self, arduinoCtrl, threadStop, appContext=None):
        self.delay = 1
        self._arduinoController = arduinoCtrl
        self._appContext = appContext
        self._thread_stop_event = threadStop
        super(FrontEndController, self).__init__()

    def emitArduinoSensorStream(self):
        # while not self._thread_stop_event.isSet():
        for n in self._arduinoController.readArduino():
            print("in thread\n "+str(n))
            self._appContext.emit('new_data', {'data': str(n)}, namespace='/test')

    def run(self):
        self.emitArduinoSensorStream()
