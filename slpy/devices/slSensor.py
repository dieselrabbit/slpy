from devices.slDevice import slDevice
from slgateway.const import mapping

class slSensor(slDevice):
    def __init__(self, gateway, id, data):
        if('hassType' not in data):
            data['hassType'] = "sensor"
        super().__init__(gateway, id, data)
        if('unit' in data):
            self._unit = data["unit"]
        else:
            self._unit = ""

    @property
    def friendlyState(self):
        if(self._unit):
            return "{} {}".format(self._state, self._unit)
        elif(self._hassType == 'binary_sensor'):
            return mapping.ON_OFF[self._state]
        else:
            return self._state

    @property
    def unit(self):
        return self._unit

