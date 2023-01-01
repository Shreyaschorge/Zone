from zone_common.events.base_listener import Listener
from zone_common.events.subjects import Subjects
from zone_common.exceptions.not_found_exception import NotFoundException
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.future import select

from db import _sessionmaker
from models.product import Product
from .queue_group_name import QueueGroupName


class ProductUpdatedListner(Listener):
    subject = Subjects.ProductUpdated
    queueGroupName = QueueGroupName.ProductUpdatedListeners

    def __init__(self, client):
        super().__init__(client=client)

    async def onMessage(self, data, msg):
        session = _sessionmaker()
        try:
            q = select(Product).where(
                and_(Product.uuid == data["uuid"], Product.version_id == data["version_id"] - 1))
            try:
                result = await session.execute(q)
                existing_product = result.scalars().one()
            except NoResultFound as err:
                raise NotFoundException()
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
