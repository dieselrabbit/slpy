import sys
import time
import json
import socket
import argparse
from slgateway.discovery import discovery
from slgateway.login import gateway_login
from slgateway.request import request_gateway, request_pool_config, \
                                request_pool_status, request_pool_button_press
from slgateway.const import mapping

class slgateway:
    def __init__(self, verbose=False, ip=None, port=None):
        self.__ip = ip
        self.__port = port
        self.__connected = False
        self.__data = {}
        

        # Try to discover gateway
        if (not self.__ip):
            self.__ip, self.__port, self.__type,\
            self.__subtype, self.__name, okchk = discovery(verbose)

        if (self.__ip):
            pass
            if (self._connect()):
                self._get_config()
                self._get_status()
                self._disconnect()


    def update(self):
        if ((self.is_connected or self._connect()) and self.__data):
            self._get_status()
            self._disconnect()

    def get_data(self):
        return self.__data

    def set_circuit(self, circuitID, circuitState):
        if (self.__connected or self._connect()):
            return request_pool_button_press(self.__socket, 
                                             circuitID, 
                                             circuitState)

    def is_connected(self):
        return self.__connected


    def _connect(self):
        self.__socket = gateway_login(self.__ip, self.__port)
        if (self.__socket):
            self.__version = ""
            self.__version = request_gateway(self.__socket)
            if (self.__version):
                self.__connected = True
                return True
        return False

    def _disconnect(self):
        if (self.__socket):
            self.__socket.close()
        self.__connected = False

    def _get_config(self):
        if (self.__connected or self._connect()):
            request_pool_config(self.__socket, self.__data)

    def _get_status(self):
        if (self.__connected or self._connect()):
            request_pool_status(self.__socket, self.__data)



if __name__ == "__main__":
    verbose = False
    host = None
    port = None
    parser = argparse.ArgumentParser(
        description="Interface for Pentair Screenlogic gateway")
    parser.add_argument('-v','--verbose', action='store_true')
    parser.add_argument('-i','--ip')
    parser.add_argument('-p','--port')
    parser.add_argument('-g','--get', metavar="circuit", type=int)
    parser.add_argument('-s','--set', nargs=2, metavar=("circuit", "state"))
    args = parser.parse_args()

    gateway = slgateway(args.verbose, args.ip, args.port)
    if ('config' not in gateway.get_data()):
        sys.exit(1)

    if (args.get):
        print(
            mapping.ON_OFF[
                int(gateway.get_data()['circuits'][int(args.get)]['value'])
                ]
            )
        sys.exit()
    elif (args.set):
        state = 0
        if (len(args.set) > 1 and 
            (args.set[1] == '1' or args.set[1].lower() == 'on')):
            state = 1
        if (gateway.set_circuit(int(args.set[0]), state)):
            gateway.update()
            print(
                mapping.ON_OFF[
                    int(gateway.get_data()['circuits']
                        [int(args.set[0])]['value'])
                    ]
                )
            sys.exit()
        else:
            sys.exit(1)
    else:
        print(json.dumps(gateway.get_data(), indent=2))
        sys.exit()
