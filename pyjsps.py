
import asyncio
import websockets
import ssl, os
import pathlib

HOST = "127.0.0.1";

info_splitter = '\n'

class JsPacket:

    def __init__(self, label, args=[], sender=None):
        self.label = label
        self.args = args
        self.sender = sender

    def parse(self):
        mapped = self.label
        for arg in self.args:
            mapped += info_splitter + arg
        return mapped

class JsSocket:

    def __init__(self, port, handler, cert=None):
        self.ssl_context = None
        self.port = port
        if cert != None:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ssl_context.load_cert_chain(pathlib.Path(os.getcwd() + f"/{cert}/cert.pem"), keyfile=(os.getcwd() + f"/{cert}/key.pem"))
        self.handler = handler
        self.prefix = "[JsSocket]: "

    async def handshake(self, client, address):
        data = await client.recv()
        mapped = data.split(info_splitter)
        label = mapped[0]
        args = []
        for i in range(len(mapped) - 1): args.append(mapped[i + 1])
        packet = self.handler(JsPacket(label, args))
        await client.send(packet.parse())

    def listen_forever(self, loop=None):
        if loop is None: loop = asyncio.get_event_loop()
        else: asyncio.set_event_loop(loop)
        if self.ssl_context is not None:
            self.server = websockets.serve(self.handshake, HOST, self.port, ssl=self.ssl_context)
        else:
            self.server = websockets.serve(self.handshake, HOST, self.port)
        loop.run_until_complete(self.server)
        loop.run_forever()
