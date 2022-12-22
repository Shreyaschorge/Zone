import json
from zone_common.events.subjects import Subjects

from zone_common.events.base_listener import Listener
from db import _sessionmaker
from models.product import Product
from .queue_group_name import QueueGroupName


class ProductCreatedListner(Listener):
    subject = Subjects.ProductCreated
    queueGroupName = QueueGroupName.ProductCreatedListener

    def __init__(self, client):
        super().__init__(client=client)

    async def onMessage(self, data, msg):
        session = _sessionmaker()
        try:
            async with session.begin():
                product = Product(**data)
                session.add(product)
                await msg.ack()

        except Exception as err:
            raise Exception(err)
        finally:
            session.close()
