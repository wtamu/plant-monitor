
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
