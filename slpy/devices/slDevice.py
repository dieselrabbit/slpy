class slDevice:
    def __init__(self, gateway, id, data):
        self._gateway = gateway
        self._id = id
        self._name = data["name"]
        self._state = data["value"]
        self._hassType = data["hassType"]

    def update(self, data):
        self._state = data["value"]

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def hassType(self):
        return self._hassType
