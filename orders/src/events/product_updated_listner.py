import json
from zone_common.events.subjects import Subjects
from zone_common.exceptions.not_found_exception import NotFoundException
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound

from zone_common.events.base_listener import Listener
from db import _sessionmaker
from models.product import Product
from .queue_group_name import queueGroupName


class ProductUpdatedListner(Listener):
    subject = Subjects.ProductUpdated
    queueGroupName = queueGroupName

    def __init__(self, client):
        super().__init__(client=client)

    async def onMessage(self, data, msg):
        session = _sessionmaker()
        q = select(Product).where(and_(Product.uuid == data["uuid"], Product.version_id == data["version_id"] - 1))
        try:
            result = await session.execute(q)
            existing_product = result.scalars().one()     
        except NoResultFound as err:
            raise NotFoundException()

        try:
            existing_product.title = data["title"]
            existing_product.description = data["description"]
            existing_product.price = data["price"]
            session.add(existing_product)
            await session.commit()
            await msg.ack()

        except Exception as err:
            raise Exception(err)
        finally:
            session.close()