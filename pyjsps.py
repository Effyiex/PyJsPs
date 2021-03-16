
import asyncio
import websockets
import ssl
import pathlib

HOST = "127.0.0.1";

class JsPacket:

    def __init__(self, label, args=[], sender=None):
        self.label = label
        self.args = args
        self.sender = sender

    def parse(self):
        mapped = self.label
        for arg in self.args:
            mapped += '\n' + arg
        return mapped

class JsSocket:

    def __init__(self, port, handler, cert=None):
        if cert != None:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            certificate = pathlib.Path(__file__).with_name(cert)
            ssl_context.load_cert_chain(certificate)
            self.server = websockets.serve(self.handshake, HOST, port, ssl=ssl_context)
        else:
            self.server = websockets.serve(self.handshake, HOST, port)
        self.handler = handler
        self.prefix = "[JsSocket]: "

    async def handshake(self, client, address):
        data = await client.recv()
        mapped = data.split('\n')
        label = mapped[0]
        args = []
        for i in range(len(mapped) - 1): args.append(mapped[i + 1])
        packet = self.handler(JsPacket(label, args))
        await client.send(packet.parse())

    def listen_forever(self):
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()
