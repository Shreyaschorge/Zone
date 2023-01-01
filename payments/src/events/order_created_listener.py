from zone_common.events.subjects import Subjects

from zone_common.events.base_listener import Listener
from db import _sessionmaker
from models.order import Order
from .queue_group_name import QueueGroupName


class OrderCreatedListener(Listener):
    subject = Subjects.OrderCreated
    queueGroupName = QueueGroupName.OrderCreatedListeners

    def __init__(self, client):
        super().__init__(client=client)

    async def onMessage(self, data, msg):
        session = _sessionmaker()
        try:
            async with session.begin():
                order = Order(**data)
                session.add(order)
                await msg.ack()

        except Exception as err:
            raise Exception(err)
        finally:
            session.close()
