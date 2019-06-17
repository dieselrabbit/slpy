import sys
import time
import json
from multiprocessing import Lock
from slgateway.slgateway import slgateway
from devices.slSwitch import *
from devices.slSensor import *


class screenlogicpy:
    def __init__(self,  verbose=False, gateway_ip=None, gateway_port=None, update_interval_min=30):
        self.__last_update = 0
        self.__update_interval = update_interval_min
        self.__lock = Lock()
        self.__devices = {}
        self.__data = {}

        self.__gateway = slgateway(gateway_ip, gateway_port)

        if(self.__gateway.connect()):
            if(verbose):
                print("Connection success!")
            self.__gateway.get_config(self.__data)
            self.__gateway.get_status(self.__data)
            self.__gateway.disconnect()
            self._updateDevices()
        else:
            if(verbose):
                print("Connection failed!")

    def _updateDevices(self):
        self._updateSwitches()
        self._updateSensors()

    def _updateSwitches(self):
        for k, v in self.__data['circuits'].items():
            if('hassType' in v):
                if(k in self.__devices):
                    self.__devices[k].update(v)
                else:
                    self.__devices[k] = slSwitch(self, k, v)

    def _updateSensors(self):
        for k, v in self.__data['sensors'].items():
            if('hassType' in v):
                if(k in self.__devices):
                    self.__devices[k].update(v)
                else:
                    self.__devices[k] = slSensor(self, k, v)
        for i in self.__data['bodies']:
            for k, v in self.__data['bodies'][i].items():
                if('hassType' in v):
                    kI = "{}_{}".format(k, i)
                    if(kI in self.__devices):
                        self.__devices[kI].update(v)
                    else:
                        self.__devices[kI] = slSensor(self, kI, v)
        for k, v in self.__data['chemistry'].items():
            if('hassType' in v):
                if(k in self.__devices):
                    self.__devices[k].update(v)
                else:
                    self.__devices[k] = slSensor(self, k, v)

    def getFriendly(self):
        self._updateDevices()
        for k, d in self.__devices.items():
            print("{} - {}: {}".format(k, d.name, d.friendlyState))


if __name__ == "__main__":
    screenlogicbridge = screenlogicpy(True)
    if(len(sys.argv) > 1):
        if(sys.argv[1] == 'get'):
            if(len(sys.argv) == 3):
                print(screenlogicbridge.getCircuit(int(sys.argv[2])))
        elif(sys.argv[1] == 'set'):
            if(len(sys.argv) == 4):
                print(screenlogicbridge.setCircuit(int(sys.argv[2]), int(sys.argv[3])))
        elif(sys.argv[1] == 'json'):
            print(screenlogicbridge.getJson())
        else:
            print("Unknown option!")
    else:
        print(screenlogicbridge.getFriendly())
