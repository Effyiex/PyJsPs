
from sys import path
path.append('../')

from pyjsps import *

def handle(packet):
    print(packet.label)
    return JsPacket("I got the packet from you :)")

server = JsSocket(7584, handle)
server.listen_forever()
