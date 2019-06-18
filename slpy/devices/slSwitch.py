from devices.slDevice import slDevice
from slgateway.const import mapping

class slSwitch(slDevice):
    def __init__(self, gateway, id, data):
        if('hassType' not in data):
            data['hassType'] = "switch"
        super().__init__(gateway, id, data)

    def toggle(self):
        if(self._state == 0):
            newState = 1
        else:
            newState = 0
        
        if(self.__gateway.setCircuit(self._id, newState)):
            print("{} set to {}".format(self._name, self.friendlyState))
        else:
            print("Setting of circuit failed!")

    @property
    def isOn(self):
        if(self._state == 1):
            return True
        else:
            return False

    @property
    def friendlyState(self):
        return mapping.ON_OFF[self._state]
