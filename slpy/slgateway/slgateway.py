from slgateway.discovery import discover
from slgateway.login import gateway_login
from slgateway.request import *

class slgateway:
    def __init__(self, ip=None, port=None, verbose=False):
        self.__ip = ip
        self.__port = port
        self.__connected = False

        # Try to discover gateway
        if(not self.__ip):
            self.__ip, self.__port, self.__type, self.__subtype, \
            self.__name, okchk = discover(verbose)


    def is_connected(self):
        return self.__connected

    def connect(self):
        self.__socket = gateway_login(self.__ip, self.__port)
        if(self.__socket):
            self.__version = ""
            self.__version = request_gateway(self.__socket)
            if(self.__version):
                self.__connected = True
                return True
        return False

    def disconnect(self):
        self.__socket.close()
        self.__connected = False

    def get_config(self, data):
        if(self.__connected or self.connect()):
            request_pool_config(self.__socket, data)

    def get_status(self, data):
        if(self.__connected or self.connect()):
            request_pool_status(self.__socket, data)

    def set_circuit(self, circuitID, circuitState):
        if(self.__connected or self.connect()):
            return request_pool_button_press(self.__socket, circuitID, circuitState)













    
