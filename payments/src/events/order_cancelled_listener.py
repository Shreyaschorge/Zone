from zone_common.events.base_listener import Listener
from zone_common.events.subjects import Subjects
from zone_common.exceptions.not_found_exception import NotFoundException
from zone_common.events.order_status import OrderStatus
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.future import select

from db import _sessionmaker
from models.order import Order
from .queue_group_name import QueueGroupName


class OrderCancelledListener(Listener):
    subject = Subjects.OrderCancelled
    queueGroupName = QueueGroupName.OrderCancelledListeners

    def __init__(self, client):
        super().__init__(client=client)

    async def onMessage(self, data, msg):
        session = _sessionmaker()
        q = select(Order).where(
            and_(Order.uuid == data["uuid"], Order.version_id == data["version_id"] - 1))
        try:
            try:
                res = await session.execute(q)
                existing_order = res.scalars().one()
            except NoResultFound as err:
                raise NotFoundException()

            existing_order.status = OrderStatus.Cancelled
            session.add(existing_order)
            await session.commit()
            await msg.ack()
        except Exception as err:
            raise Exception(err)
        finally:
            session.close()
