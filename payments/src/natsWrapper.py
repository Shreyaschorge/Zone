import asyncio as aio
import nats
import signal
import sys

from nats.aio.client import Client as NATS
from constants import APP_NAME


def die():
    sys.exit(1)


class NatsWrapper:
    __client: NATS = None

    @property
    def client(self) -> NATS:
        if not self.__client:
            raise Exception("Can't connect to NATS")
        return self.__client

    async def error_cb(self, e):
        print(f"NATS Error:[{APP_NAME}]: ", e)

    async def closed_cb(self):
        print("Connection to NATS is closed.")
        await aio.sleep(0.2)
        aio.get_running_loop().stop()

    async def reconnected_cb(self):
        print(f"Got reconnected to NATS.")

    async def connect(self, url):

        options = {
            "error_cb": self.error_cb,
            "closed_cb": self.closed_cb,
            "reconnected_cb": self.reconnected_cb,
            "name": APP_NAME
        }

        try:
            self.__client = await nats.connect(url, **options)
            print("Connected to NATS.")
        except Exception as e:
            print(e)
            die()

        def signal_handler():
            if self.__client.is_closed:
                return
            print("Disconnecting...")
            aio.get_running_loop().create_task(self.__client.close())

        for sig in ('SIGINT', 'SIGTERM'):
            aio.get_running_loop().add_signal_handler(
                getattr(signal, sig), signal_handler)


natsWrapper = NatsWrapper()
