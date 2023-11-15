import time

import dill
from crochet import run_in_reactor, setup
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet.protocol import Protocol

from cad.utils.editor.data import EditorPacket, ExtrudedModel

setup()


class EditorClientProtocol(Protocol):
    def write(self, data: bytes):
        self.transport.write(data)

    def connectionMade(self):
        print("Connection made")

    def dataReceived(self, data):
        print("Server said:", data)


class EditorClient:
    def __init__(self, host="localhost"):
        self.point = TCP4ClientEndpoint(reactor, host, 17348)
        self.greeter = EditorClientProtocol()
        self.ready = False

    def connect(self):
        self._connect()
        while not self.ready:
            time.sleep(0.1)

    @run_in_reactor
    def _connect(self):
        def on_connected(protocol):
            self.ready = True

        d = connectProtocol(self.point, self.greeter)
        d.addCallback(on_connected)

    @run_in_reactor
    def _send_data(self, bytes):
        self.greeter.transport.write(bytes)

    def send_str(self, s):
        self._send_data(s.encode("utf-8"))

    def send_model(self, model):
        packet = EditorPacket("extruded_model", model)
        self._send_data(dill.dumps(packet))


if __name__ == "__main__":
    client = EditorClient()
    client.connect()

    from shapely.geometry import box

    shape = box(0, 0, 10, 10) - box(2, 2, 8, 8)

    model = ExtrudedModel(shape, 5, None)

    client.send_model(model)
