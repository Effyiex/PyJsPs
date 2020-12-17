
import asyncio;
import websockets

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

    def __init__(self, port, handler):
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
